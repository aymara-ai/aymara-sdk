import asyncio
import mimetypes
import os
from typing import Callable, Coroutine, Dict, List, Optional, Union

import httpx

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client.api.score_runs import (
    get_image_presigned_urls,
)
from aymara_ai.generated.aymara_api_client.models import ImageUploadRequestInSchema
from aymara_ai.types import ImageStudentAnswerInput


class UploadMixin(AymaraAIProtocol):
    def upload_images(
        self,
        test_uuid: str,
        student_answers: List[ImageStudentAnswerInput],
        batch_size: int = 10,
        progress_callback: Callable[[int], None] = None,
    ) -> Dict[str, str]:
        """
        Upload images using presigned URLs synchronously.

        :param test_uuid: UUID of the test
        :param student_answers: List of student answers containing image paths
        :param batch_size: Number of images to upload in parallel
        :param progress_callback: Optional callback function to report upload progress
        :return: Dictionary mapping question UUIDs to uploaded keys
        """
        return self._upload_images(
            test_uuid,
            student_answers,
            batch_size,
            is_async=False,
            progress_callback=progress_callback,
        )

    async def upload_images_async(
        self,
        test_uuid: str,
        student_answers: List[ImageStudentAnswerInput],
        batch_size: int = 10,
        progress_callback: Callable[[int], None] = None,
    ) -> Dict[str, str]:
        """
        Upload images using presigned URLs asynchronously.

        :param test_uuid: UUID of the test
        :param student_answers: List of student answers containing image paths
        :param batch_size: Number of images to upload in parallel
        :param progress_callback: Optional callback function to report upload progress
        :return: Dictionary mapping question UUIDs to uploaded keys
        """
        return await self._upload_images(
            test_uuid,
            student_answers,
            batch_size,
            is_async=True,
            progress_callback=progress_callback,
        )

    def _upload_images(
        self,
        test_uuid: str,
        student_answers: List[ImageStudentAnswerInput],
        batch_size: int,
        is_async: bool,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> Union[Dict[str, str], Coroutine[None, None, Dict[str, str]]]:
        if is_async:
            return self._upload_images_async_impl(
                test_uuid, student_answers, batch_size, progress_callback
            )
        else:
            return self._upload_images_sync_impl(
                test_uuid, student_answers, batch_size, progress_callback
            )

    def _upload_images_sync_impl(
        self,
        test_uuid: str,
        student_answers: List[ImageStudentAnswerInput],
        batch_size: int,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> Dict[str, str]:
        # Get presigned URLs
        response = get_image_presigned_urls.sync_detailed(
            client=self.client,
            body=ImageUploadRequestInSchema(
                test_uuid=test_uuid,
                answers=[
                    a for a in student_answers if a.answer_image_path
                ],  # Only request URLs for non-None paths
            ),
        )

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        presigned_urls = response.parsed.to_dict()
        uploaded_keys = {
            answer.question_uuid: None
            for answer in student_answers
            if not answer.answer_image_path
        }  # Initialize with None for skipped uploads
        uploaded_count = len(uploaded_keys)  # Start count with skipped uploads

        # Upload images in batches
        for i in range(0, len(student_answers), batch_size):
            batch = {
                answer.question_uuid: answer.answer_image_path
                for answer in student_answers[i : i + batch_size]
                if answer.answer_image_path  # Only include non-None paths
            }
            for uuid, path in batch.items():
                url = presigned_urls[uuid]

                if not os.path.exists(path):
                    raise ValueError(f"Image path does not exist: {path}")

                with open(path, "rb") as f:
                    mime_type = mimetypes.guess_type(path)[0]
                    if not mime_type or not mime_type.startswith("image/"):
                        continue

                    headers = {"Content-Type": mime_type}
                    response = httpx.put(url, content=f.read(), headers=headers)
                    if response.status_code != 200:
                        continue

                    uploaded_keys[uuid] = url.split("?")[0].split("/")[-1]
                    uploaded_count += 1
                    if progress_callback:
                        progress_callback(uploaded_count)

        return uploaded_keys

    async def _upload_images_async_impl(
        self,
        test_uuid: str,
        student_answers: List[ImageStudentAnswerInput],
        batch_size: int,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> Dict[str, str]:
        # Get presigned URLs
        response = await get_image_presigned_urls.asyncio_detailed(
            client=self.client,
            body=ImageUploadRequestInSchema(
                test_uuid=test_uuid,
                answers=[
                    a for a in student_answers if a.answer_image_path
                ],  # Only request URLs for non-None paths
            ),
        )

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        presigned_urls = response.parsed.to_dict()
        uploaded_keys = {
            answer.question_uuid: None
            for answer in student_answers
            if not answer.answer_image_path
        }  # Initialize with None for skipped uploads
        uploaded_count = len(uploaded_keys)  # Start count with skipped uploads
        if progress_callback:
            progress_callback(uploaded_count)
        max_retries = 3
        timeout = httpx.Timeout(
            timeout=30.0, write=10.0
        )  # 30s total timeout, 10s write timeout

        # Upload images in batches
        async with httpx.AsyncClient(timeout=timeout) as client:
            for i in range(0, len(student_answers), batch_size):
                batch = {
                    answer.question_uuid: answer.answer_image_path
                    for answer in student_answers[i : i + batch_size]
                    if answer.answer_image_path  # Only include non-None paths
                }
                tasks = []
                batch_keys = []
                batch_urls = []
                batch_contents = []

                for uuid, path in batch.items():
                    url = presigned_urls[uuid]
                    mime_type = mimetypes.guess_type(path)[0]
                    if not mime_type or not mime_type.startswith("image/"):
                        continue

                    if not os.path.exists(path):
                        raise ValueError(f"Image path does not exist: {path}")

                    with open(path, "rb") as f:
                        file_content = f.read()
                        headers = {"Content-Type": mime_type}
                        tasks.append(
                            client.put(url, content=file_content, headers=headers)
                        )
                        batch_keys.append(uuid)
                        batch_urls.append(url)
                        batch_contents.append((file_content, headers))

                if tasks:
                    # Try uploading with retries
                    for attempt in range(max_retries):
                        try:
                            responses = await asyncio.gather(
                                *tasks, return_exceptions=True
                            )

                            # Handle responses and retry failed uploads
                            retry_tasks = []
                            retry_keys = []
                            retry_urls = []

                            for idx, (response, uuid, url) in enumerate(
                                zip(responses, batch_keys, batch_urls)
                            ):
                                if isinstance(response, Exception):
                                    if (
                                        attempt < max_retries - 1
                                    ):  # Don't retry on last attempt
                                        retry_tasks.append(
                                            client.put(
                                                url,
                                                content=batch_contents[idx][0],
                                                headers=batch_contents[idx][1],
                                            )
                                        )
                                        retry_keys.append(uuid)
                                        retry_urls.append(url)
                                elif response.status_code == 200:
                                    uploaded_keys[uuid] = url.split("?")[0].split("/")[
                                        -1
                                    ]
                                    uploaded_count += 1
                                    if progress_callback:
                                        progress_callback(uploaded_count)

                            # If there are no more retries needed, break
                            if not retry_tasks:
                                break

                            # Update tasks for next retry attempt
                            tasks = retry_tasks
                            batch_keys = retry_keys
                            batch_urls = retry_urls

                        except Exception as e:
                            if attempt == max_retries - 1:
                                self.logger.error(
                                    f"Failed to upload images after {max_retries} attempts: {str(e)}"
                                )
                                raise

                            # Add delay between retries
                            if attempt < max_retries - 1 and retry_tasks:
                                await asyncio.sleep(
                                    1 * (attempt + 1)
                                )  # Exponential backoff

        return uploaded_keys

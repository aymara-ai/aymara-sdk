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
from aymara_ai.types import StudentAnswerInput


class UploadMixin(AymaraAIProtocol):
    def upload_images(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswerInput],
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
        student_answers: List[StudentAnswerInput],
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
        student_answers: List[StudentAnswerInput],
        batch_size: int,
        is_async: bool,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> Union[Dict[str, str], Coroutine[None, None, Dict[str, str]]]:
        # Validate inputs

        for answer in student_answers:
            if not answer.answer_image_path:
                raise ValueError(
                    f"Image path is required for question {answer.question_uuid}"
                )

            if not os.path.exists(answer.answer_image_path):
                raise ValueError(
                    f"Image path does not exist: {answer.answer_image_path}"
                )

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
        student_answers: List[StudentAnswerInput],
        batch_size: int,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> Dict[str, str]:
        # Get presigned URLs
        response = get_image_presigned_urls.sync_detailed(
            client=self.client,
            body=ImageUploadRequestInSchema(
                test_uuid=test_uuid,
                answers=student_answers,
            ),
        )

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        presigned_urls = response.parsed.to_dict()
        uploaded_keys = {}
        uploaded_count = 0

        # Upload images in batches
        for i in range(0, len(student_answers), batch_size):
            batch = {
                answer.question_uuid: answer.answer_image_path
                for answer in student_answers[i : i + batch_size]
            }

            for uuid, path in batch.items():
                url = presigned_urls[uuid]
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
        student_answers: List[StudentAnswerInput],
        batch_size: int,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> Dict[str, str]:
        # Get presigned URLs
        response = await get_image_presigned_urls.asyncio_detailed(
            client=self.client,
            body=ImageUploadRequestInSchema(
                test_uuid=test_uuid,
                answers=student_answers,
            ),
        )

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        presigned_urls = response.parsed.to_dict()
        uploaded_keys = {}
        uploaded_count = 0

        # Upload images in batches
        async with httpx.AsyncClient() as client:
            for i in range(0, len(student_answers), batch_size):
                batch = {
                    answer.question_uuid: answer.answer_image_path
                    for answer in student_answers[i : i + batch_size]
                }
                tasks = []
                batch_keys = []
                batch_urls = []

                for uuid, path in batch.items():
                    url = presigned_urls[uuid]
                    mime_type = mimetypes.guess_type(path)[0]
                    if not mime_type or not mime_type.startswith("image/"):
                        continue

                    with open(path, "rb") as f:
                        file_content = f.read()
                        headers = {"Content-Type": mime_type}
                        tasks.append(
                            client.put(url, content=file_content, headers=headers)
                        )

                        batch_keys.append(uuid)
                        batch_urls.append(url)

                if tasks:
                    responses = await asyncio.gather(*tasks)
                    for response, uuid, url in zip(responses, batch_keys, batch_urls):
                        if response.status_code == 200:
                            uploaded_keys[uuid] = url.split("?")[0].split("/")[-1]
                            uploaded_count += 1
                            if progress_callback:
                                progress_callback(uploaded_count)
        return uploaded_keys

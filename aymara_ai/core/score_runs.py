import asyncio
import os
import time
from typing import Coroutine, List, Optional, Union

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.core.uploads import UploadMixin
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.score_runs import (
    create_score_run,
    delete_score_run,
    get_score_run,
    get_score_run_answers,
    list_score_runs,
)
from aymara_ai.generated.aymara_api_client.api.tests import get_test
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import (
    BaseStudentAnswerInput,
    ImageStudentAnswerInput,
    ListScoreRunResponse,
    ScoreRunResponse,
    ScoringExample,
    Status,
    TextStudentAnswerInput,
)
from aymara_ai.utils.constants import (
    DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS,
    DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS,
    DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
    MAX_EXAMPLES_LENGTH,
    POLLING_INTERVAL,
)


class ScoreRunMixin(UploadMixin, AymaraAIProtocol):
    """
    Mixin class that provides score run functionality.
    Inherits from UploadMixin to get image upload capabilities.
    """

    # Score Test Methods
    def score_test(
        self,
        test_uuid: str,
        student_answers: List[BaseStudentAnswerInput],
        scoring_examples: Optional[List[ScoringExample]] = None,
        max_wait_time_secs: Optional[int] = None,
        is_sandbox: Optional[bool] = False,
    ) -> ScoreRunResponse:
        return self._score_test(
            test_uuid=test_uuid,
            student_answers=student_answers,
            is_async=False,
            max_wait_time_secs=max_wait_time_secs,
            scoring_examples=scoring_examples,
            is_sandbox=is_sandbox,
        )

    score_test.__doc__ = f"""
        Score a test synchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of BaseStudentAnswerInput objects containing student responses.
        :type student_answers: List[BaseStudentAnswerInput]
        :param scoring_examples: Optional list of examples to guide the scoring process.
        :type scoring_examples: Optional[List[ScoringExample]]
        :param max_wait_time_secs: Maximum wait time for test scoring, defaults to {DEFAULT_SAFETY_MAX_WAIT_TIME_SECS}, {DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS}, and {DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS} seconds for safety, jailbreak, and accuracy tests, respectively.
        :type max_wait_time_secs: int, optional
        :return: Score response.
        :rtype: ScoreRunResponse
        """

    async def score_test_async(
        self,
        test_uuid: str,
        student_answers: List[BaseStudentAnswerInput],
        scoring_examples: Optional[List[ScoringExample]] = None,
        max_wait_time_secs: Optional[int] = None,
        is_sandbox: Optional[bool] = False,
    ) -> ScoreRunResponse:
        return await self._score_test(
            test_uuid=test_uuid,
            student_answers=student_answers,
            is_async=True,
            max_wait_time_secs=max_wait_time_secs,
            scoring_examples=scoring_examples,
            is_sandbox=is_sandbox,
        )

    score_test_async.__doc__ = f"""
        Score a test asynchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of BaseStudentAnswerInput objects containing student responses.
        :type student_answers: List[BaseStudentAnswerInput]
        :param scoring_examples: Optional list of examples to guide the scoring process.
        :type scoring_examples: Optional[List[ScoringExample]]
        :param max_wait_time_secs: Maximum wait time for test scoring, defaults to {DEFAULT_SAFETY_MAX_WAIT_TIME_SECS}, {DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS}, and {DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS} seconds for safety, jailbreak, and accuracy tests, respectively.
        :type max_wait_time_secs: optional, int
        :return: Score response.
        :rtype: ScoreRunResponse
        """

    def _score_test(
        self,
        test_uuid: str,
        student_answers: List[BaseStudentAnswerInput],
        is_async: bool,
        max_wait_time_secs: Optional[int] = None,
        scoring_examples: Optional[List[ScoringExample]] = None,
        is_sandbox: Optional[bool] = False,
    ) -> Union[ScoreRunResponse, Coroutine[ScoreRunResponse, None, None]]:
        self._validate_student_answers(student_answers)

        if scoring_examples is not None:
            self._validate_scoring_examples(scoring_examples)

        score_data = models.ScoreRunInSchema(
            test_uuid=test_uuid,
            answers=[
                BaseStudentAnswerInput.to_answer_in_schema(student_answer)
                for student_answer in student_answers
            ],
            score_run_examples=[
                example.to_scoring_example_in_schema() for example in scoring_examples
            ]
            if scoring_examples
            else None,
        )

        if is_async:
            return self._create_and_wait_for_score_impl_async(
                score_data, max_wait_time_secs, is_sandbox
            )
        else:
            return self._create_and_wait_for_score_impl_sync(
                score_data, max_wait_time_secs, is_sandbox
            )

    # Get Score Run Methods
    def get_score_run(self, score_run_uuid: str) -> ScoreRunResponse:
        """
        Get the current status of a score run synchronously, and answers if it is completed.

        :param score_run_uuid: UUID of the score run.
        :type score_run_uuid: str
        :return: Score run response.
        :rtype: ScoreRunResponse
        """
        return self._get_score_run(score_run_uuid, is_async=False)

    async def get_score_run_async(self, score_run_uuid: str) -> ScoreRunResponse:
        """
        Get the current status of a score run asynchronously, and answers if it is completed.

        :param score_run_uuid: UUID of the score run.
        :type score_run_uuid: str
        :return: Score run response.
        :rtype: ScoreRunResponse
        """
        return await self._get_score_run(score_run_uuid, is_async=True)

    def _get_score_run(
        self, score_run_uuid: str, is_async: bool
    ) -> Union[ScoreRunResponse, Coroutine[ScoreRunResponse, None, None]]:
        if is_async:
            return self._get_score_run_async_impl(score_run_uuid)
        else:
            return self._get_score_run_sync_impl(score_run_uuid)

    def _get_score_run_sync_impl(self, score_run_uuid: str) -> ScoreRunResponse:
        response = get_score_run.sync_detailed(
            client=self.client, score_run_uuid=score_run_uuid
        )

        if response.status_code == 404:
            raise ValueError(f"Score run with UUID {score_run_uuid} not found")

        score_response = response.parsed
        answers = None
        if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = self._get_all_score_run_answers_sync(score_run_uuid)

        return ScoreRunResponse.from_score_run_out_schema_and_answers(
            score_response, answers
        )

    async def _get_score_run_async_impl(self, score_run_uuid: str) -> ScoreRunResponse:
        response = await get_score_run.asyncio_detailed(
            client=self.client, score_run_uuid=score_run_uuid
        )

        if response.status_code == 404:
            raise ValueError(f"Score run with UUID {score_run_uuid} not found")

        score_response = response.parsed
        answers = None
        if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = await self._get_all_score_run_answers_async(score_run_uuid)

        return ScoreRunResponse.from_score_run_out_schema_and_answers(
            score_response, answers
        )

    # List Score Runs Methods
    def list_score_runs(self, test_uuid: Optional[str] = None) -> ListScoreRunResponse:
        """
        List all score runs synchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: Optional[str]
        :return: List of score run responses.
        :rtype: ListScoreRunResponse
        """
        score_runs = self._list_score_runs(is_async=False, test_uuid=test_uuid)
        return ListScoreRunResponse(score_runs)

    async def list_score_runs_async(
        self, test_uuid: Optional[str] = None
    ) -> ListScoreRunResponse:
        """
        List all score runs asynchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: Optional[str]
        :return: List of score run responses.
        :rtype: ListScoreRunResponse
        """
        score_runs = await self._list_score_runs(is_async=True, test_uuid=test_uuid)

        return ListScoreRunResponse(score_runs)

    def _list_score_runs(
        self,
        is_async: bool,
        test_uuid: Optional[str] = None,
    ) -> Union[List[ScoreRunResponse], Coroutine[List[ScoreRunResponse], None, None]]:
        if is_async:
            return self._list_score_runs_async_impl(test_uuid)
        else:
            return self._list_score_runs_sync_impl(test_uuid)

    def _list_score_runs_sync_impl(
        self, test_uuid: Optional[str] = None
    ) -> List[ScoreRunResponse]:
        all_score_runs = []
        offset = 0
        while True:
            response = list_score_runs.sync_detailed(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            paged_response = response.parsed
            all_score_runs.extend(paged_response.items)
            if len(all_score_runs) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            ScoreRunResponse.from_score_run_out_schema_and_answers(
                score_run,
            )
            for score_run in all_score_runs
        ]

    async def _list_score_runs_async_impl(
        self, test_uuid: Optional[str] = None
    ) -> List[ScoreRunResponse]:
        all_score_runs: List[ScoreRunResponse] = []
        offset = 0
        while True:
            response = await list_score_runs.asyncio_detailed(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            paged_response = response.parsed
            all_score_runs.extend(paged_response.items)
            if len(all_score_runs) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            ScoreRunResponse.from_score_run_out_schema_and_answers(
                score_run,
            )
            for score_run in all_score_runs
        ]

    # Helper Methods
    def _create_and_wait_for_score_impl_sync(
        self,
        score_data: models.ScoreRunInSchema,
        max_wait_time_secs: Optional[int] = None,
        is_sandbox: Optional[bool] = False,
    ) -> ScoreRunResponse:
        start_time = time.time()

        test = get_test.sync_detailed(
            client=self.client, test_uuid=score_data.test_uuid
        )

        if max_wait_time_secs is None:
            if (
                test.parsed.test_type == TestType.SAFETY
                or test.parsed.test_type == TestType.IMAGE_SAFETY
            ):
                max_wait_time_secs = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS
            elif test.parsed.test_type == TestType.JAILBREAK:
                max_wait_time_secs = DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS
            elif test.parsed.test_type == TestType.ACCURACY:
                max_wait_time_secs = DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS

        # Create progress bar once at the start
        with self.logger.progress_bar(
            test.parsed.test_name,
            "pending",  # Will be updated with real UUID after creation
            Status.UPLOADING
            if any(a.answer_image_path for a in score_data.answers)
            else Status.PENDING,
            upload_total=len([a for a in score_data.answers if a.answer_image_path]),
        ) as pbar:
            if test.parsed.test_type == TestType.IMAGE_SAFETY:
                uploaded_keys = self.upload_images(
                    score_data.test_uuid,
                    score_data.answers,
                    progress_callback=lambda n: pbar.update_upload_progress(n),
                )

                for answer in score_data.answers:
                    if (
                        answer.answer_image_path
                        and answer.question_uuid in uploaded_keys
                    ):
                        answer.answer_image_path = uploaded_keys[answer.question_uuid]

            response = create_score_run.sync_detailed(
                client=self.client, body=score_data, is_sandbox=is_sandbox
            )

            if response.status_code == 404:
                raise ValueError("Failed to create score run")
            elif response.status_code == 422:
                message = response.parsed.detail
                raise ValueError(message)

            score_response = response.parsed
            score_run_uuid = response.parsed.score_run_uuid
            pbar.update_uuid(score_run_uuid)

            remaining_score_runs = score_response.remaining_score_runs
            if remaining_score_runs is not None:
                score_run_plural = (
                    "score run" if remaining_score_runs == 1 else "score runs"
                )
                self.logger.warning(
                    f"You have {remaining_score_runs} {score_run_plural} remaining. To upgrade, visit https://aymara.ai/upgrade."
                )

            # Continue with polling loop
            while True:
                response = get_score_run.sync_detailed(
                    client=self.client, score_run_uuid=score_run_uuid
                )

                if response.status_code == 404:
                    raise ValueError(f"Score run with UUID {score_run_uuid} not found")

                score_response = response.parsed

                self.logger.update_progress_bar(
                    score_run_uuid,
                    Status.from_api_status(score_response.score_run_status),
                )

                elapsed_time = time.time() - start_time

                if elapsed_time > max_wait_time_secs:
                    score_response.score_run_status = models.ScoreRunStatus.FAILED
                    self.logger.update_progress_bar(score_run_uuid, Status.FAILED)
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Score run creation timed out."
                    )
                if score_response.score_run_status == models.ScoreRunStatus.FAILED:
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Internal server error. Please try again."
                    )

                if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
                    answers = self._get_all_score_run_answers_sync(score_run_uuid)
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, answers
                    )

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_score_impl_async(
        self,
        score_data: models.ScoreRunInSchema,
        max_wait_time_secs: Optional[int] = None,
        is_sandbox: Optional[bool] = False,
    ) -> ScoreRunResponse:
        start_time = time.time()

        # Generate a unique temporary UUID for the progress bar
        temp_uuid = f"pending_{id(score_data)}"  # Use object id to make unique

        # Get test info first
        test = await get_test.asyncio_detailed(
            client=self.client, test_uuid=score_data.test_uuid
        )

        if max_wait_time_secs is None:
            if (
                test.parsed.test_type == TestType.SAFETY
                or test.parsed.test_type == TestType.IMAGE_SAFETY
            ):
                max_wait_time_secs = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS
            elif test.parsed.test_type == TestType.JAILBREAK:
                max_wait_time_secs = DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS
            elif test.parsed.test_type == TestType.ACCURACY:
                max_wait_time_secs = DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS

        # Create progress bar once at the start
        with self.logger.progress_bar(
            test.parsed.test_name,
            temp_uuid,  # Will be updated with real UUID after creation
            Status.UPLOADING
            if any(a.answer_image_path for a in score_data.answers)
            else Status.PENDING,
            upload_total=len([a for a in score_data.answers]),
        ) as pbar:
            if test.parsed.test_type == TestType.IMAGE_SAFETY:
                uploaded_keys = await self.upload_images_async(
                    score_data.test_uuid,
                    score_data.answers,
                    progress_callback=lambda n: pbar.update_upload_progress(n),
                )

                for answer in score_data.answers:
                    if (
                        answer.answer_image_path
                        and answer.question_uuid in uploaded_keys
                    ):
                        answer.answer_image_path = uploaded_keys[answer.question_uuid]

            response = await create_score_run.asyncio_detailed(
                client=self.client, body=score_data, is_sandbox=is_sandbox
            )

            if response.status_code == 404:
                raise ValueError("Failed to create score run")
            elif response.status_code == 422:
                message = response.parsed.detail
                raise ValueError(message)

            score_response = response.parsed
            score_run_uuid = response.parsed.score_run_uuid
            pbar.update_uuid(score_run_uuid)

            remaining_score_runs = score_response.remaining_score_runs
            if remaining_score_runs is not None:
                score_run_plural = (
                    "score run" if remaining_score_runs == 1 else "score runs"
                )
                self.logger.warning(
                    f"You have {remaining_score_runs} {score_run_plural} remaining. To upgrade, visit https://aymara.ai/upgrade."
                )

            # Continue with polling loop
            while True:
                response = await get_score_run.asyncio_detailed(
                    client=self.client, score_run_uuid=score_run_uuid
                )

                if response.status_code == 404:
                    raise ValueError(f"Score run with UUID {score_run_uuid} not found")

                score_response = response.parsed

                self.logger.update_progress_bar(
                    score_run_uuid,
                    Status.from_api_status(score_response.score_run_status),
                )

                elapsed_time = time.time() - start_time

                if elapsed_time > max_wait_time_secs:
                    score_response.score_run_status = models.ScoreRunStatus.FAILED
                    self.logger.update_progress_bar(score_run_uuid, Status.FAILED)
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Score run creation timed out."
                    )
                if score_response.score_run_status == models.ScoreRunStatus.FAILED:
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Internal server error. Please try again."
                    )

                if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
                    answers = await self._get_all_score_run_answers_async(
                        score_run_uuid
                    )
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, answers
                    )

                await asyncio.sleep(POLLING_INTERVAL)

    def _get_all_score_run_answers_sync(
        self, score_run_uuid: str
    ) -> List[models.AnswerOutSchema]:
        answers = []
        offset = 0
        while True:
            response = get_score_run_answers.sync_detailed(
                client=self.client, score_run_uuid=score_run_uuid, offset=offset
            )

            if response.status_code == 404:
                raise ValueError(f"Score run with UUID {score_run_uuid} not found")
            paged_response = response.parsed
            answers.extend(paged_response.items)
            if len(answers) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return answers

    async def _get_all_score_run_answers_async(
        self, score_run_uuid: str
    ) -> List[models.AnswerOutSchema]:
        answers = []
        offset = 0
        while True:
            response = await get_score_run_answers.asyncio_detailed(
                client=self.client, score_run_uuid=score_run_uuid, offset=offset
            )
            if response.status_code == 404:
                raise ValueError(f"Score run with UUID {score_run_uuid} not found")

            paged_response = response.parsed
            answers.extend(paged_response.items)
            if len(answers) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return answers

    def _validate_student_answers(self, student_answers: List[BaseStudentAnswerInput]):
        if not student_answers:
            raise ValueError("Student answers cannot be empty.")

        if not all(
            isinstance(answer, (TextStudentAnswerInput, ImageStudentAnswerInput))
            for answer in student_answers
        ):
            non_student_answers = [
                answer
                for answer in student_answers
                if not isinstance(
                    answer, (TextStudentAnswerInput, ImageStudentAnswerInput)
                )
            ]
            self.logger.error(f"Invalid answers: {non_student_answers}")
            raise ValueError(
                "All items in student answers must be either TextStudentAnswerInput or ImageStudentAnswerInput."
            )

        if any(
            isinstance(answer, ImageStudentAnswerInput) for answer in student_answers
        ):
            self._validate_image_paths(student_answers)

    def _validate_image_paths(self, student_answers: List[ImageStudentAnswerInput]):
        for answer in student_answers:
            if answer.answer_image_path:
                if not os.path.exists(answer.answer_image_path):
                    self.logger.error(
                        f"Image path does not exist: {answer.answer_image_path}"
                    )
                    raise ValueError(
                        f"Image path does not exist: {answer.answer_image_path}"
                    )

    def _validate_scoring_examples(self, scoring_examples: List[ScoringExample]):
        if len(scoring_examples) > MAX_EXAMPLES_LENGTH:
            raise ValueError(
                f"Scoring examples must be less than {MAX_EXAMPLES_LENGTH}."
            )
        if not all(isinstance(example, ScoringExample) for example in scoring_examples):
            non_scoring_examples = [
                example
                for example in scoring_examples
                if not isinstance(example, ScoringExample)
            ]
            self.logger.error(f"Invalid examples: {non_scoring_examples}")
            raise ValueError("All items in scoring examples must be ScoringExample.")

    def delete_score_run(self, score_run_uuid: str) -> None:
        """
        Delete a score run synchronously.

        :param score_run_uuid: UUID of the score run.
        :type score_run_uuid: str
        """
        response = delete_score_run.sync_detailed(
            client=self.client, score_run_uuid=score_run_uuid
        )

        if response.status_code == 404:
            raise ValueError(f"Score run with UUID {score_run_uuid} not found")
        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

    async def delete_score_run_async(self, score_run_uuid: str) -> None:
        """
        Delete a score run asynchronously.

        :param score_run_uuid: UUID of the score run.
        :type score_run_uuid: str
        """
        response = await delete_score_run.asyncio_detailed(
            client=self.client, score_run_uuid=score_run_uuid
        )

        if response.status_code == 404:
            raise ValueError(f"Score run with UUID {score_run_uuid} not found")
        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

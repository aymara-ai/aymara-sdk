import asyncio
import time
from typing import Coroutine, List, Optional, Union

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.score_runs import (
    create_score_run,
    delete_score_run,
    get_score_run,
    get_score_run_answers,
    list_score_runs,
)
from aymara_ai.types import (
    ListScoreRunResponse,
    ScoreRunResponse,
    Status,
    StudentAnswerInput,
)
from aymara_ai.utils.constants import POLLING_INTERVAL


class ScoreRunMixin(AymaraAIProtocol):
    # Score Test Methods
    def score_test(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswerInput],
    ) -> ScoreRunResponse:
        """
        Score a test synchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of StudentAnswerInput objects containing student responses.
        :type student_answers: List[StudentAnswerInput]
        :return: Score response.
        :rtype: ScoreRunResponse
        """
        return self._score_test(test_uuid, student_answers, is_async=False)

    async def score_test_async(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswerInput],
    ) -> ScoreRunResponse:
        """
        Score a test asynchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of StudentAnswerInput objects containing student responses.
        :type student_answers: List[StudentAnswerInput]
        :return: Score response.
        :rtype: ScoreRunResponse
        """
        return await self._score_test(test_uuid, student_answers, is_async=True)

    def _score_test(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswerInput],
        is_async: bool,
    ) -> Union[ScoreRunResponse, Coroutine[ScoreRunResponse, None, None]]:
        self._validate_student_answers(student_answers)

        score_data = models.ScoreRunInSchema(
            test_uuid=test_uuid,
            answers=[
                StudentAnswerInput.to_answer_in_schema(student_answer)
                for student_answer in student_answers
            ],
        )

        if is_async:
            return self._create_and_wait_for_score_impl_async(score_data)
        else:
            return self._create_and_wait_for_score_impl_sync(score_data)

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
        self, score_data: models.ScoreRunInSchema
    ) -> ScoreRunResponse:
        start_time = time.time()
        response = create_score_run.sync_detailed(client=self.client, body=score_data)

        if response.status_code == 404:
            raise ValueError("Failed to create score run")
        elif response.status_code == 422:
            message = response.parsed.detail
            raise ValueError(message)
        score_response = response.parsed
        score_run_uuid = score_response.score_run_uuid
        test_name = score_response.test.test_name

        remaining_score_runs = score_response.remaining_score_runs

        if remaining_score_runs is not None:
            score_run_plural = (
                "score run" if remaining_score_runs == 1 else "score runs"
            )
            self.logger.warning(
                f"You have {remaining_score_runs} {score_run_plural} remaining. To upgrade, visit https://aymara.ai/upgrade."
            )

        with self.logger.progress_bar(
            test_name,
            score_run_uuid,
            Status.from_api_status(score_response.score_run_status),
        ):
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

                if score_response.score_run_status == models.ScoreRunStatus.FAILED:
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Internal server error. Please try again."
                    )

                if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
                    answers = self._get_all_score_run_answers_sync(score_run_uuid)
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, answers
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time_secs:
                    score_response.score_run_status = models.ScoreRunStatus.FAILED
                    self.logger.update_progress_bar(score_run_uuid, Status.FAILED)
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Score run creation timed out."
                    )

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_score_impl_async(
        self, score_data: models.ScoreRunInSchema
    ) -> ScoreRunResponse:
        start_time = time.time()
        response = await create_score_run.asyncio_detailed(
            client=self.client, body=score_data
        )

        if response.status_code == 404:
            raise ValueError("Failed to create score run")
        elif response.status_code == 422:
            message = response.parsed.detail
            raise ValueError(message)

        score_response = response.parsed
        score_run_uuid = score_response.score_run_uuid
        test_name = score_response.test.test_name

        remaining_score_runs = score_response.remaining_score_runs

        if remaining_score_runs is not None:
            score_run_plural = (
                "score run" if remaining_score_runs == 1 else "score runs"
            )
            self.logger.warning(
                f"You have {remaining_score_runs} {score_run_plural} remaining. To upgrade, visit https://aymara.ai/upgrade."
            )

        with self.logger.progress_bar(
            test_name,
            score_run_uuid,
            Status.from_api_status(score_response.score_run_status),
        ):
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

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time_secs:
                    score_response.score_run_status = models.ScoreRunStatus.FAILED
                    self.logger.update_progress_bar(score_run_uuid, Status.FAILED)
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Score run creation timed out."
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

    def _validate_student_answers(self, student_answers: List[StudentAnswerInput]):
        if not student_answers:
            raise ValueError("Student answers cannot be empty.")
        if not all(
            isinstance(answer, StudentAnswerInput) for answer in student_answers
        ):
            raise ValueError("All items in student answers must be StudentAnswerInput.")

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

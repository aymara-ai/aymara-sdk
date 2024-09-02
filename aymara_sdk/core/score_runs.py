import asyncio
import time
from typing import Coroutine, List, Optional, Union

from aymara_sdk.core.protocols import AymaraAIProtocol
from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.generated.aymara_api_client.api.score_runs import (
    create_score_run,
    get_score_run,
    get_score_run_answers,
    list_score_runs,
)
from aymara_sdk.types.types import (
    ScoreRunResponse,
    Status,
    StudentAnswerInput,
)
from aymara_sdk.utils.constants import POLLING_INTERVAL


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
        score_data = models.ScoreRunSchema(
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
        score_response = get_score_run.sync(
            client=self.client, score_run_uuid=score_run_uuid
        )
        answers = None
        if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = self._get_all_score_run_answers_sync(score_run_uuid)

        return ScoreRunResponse.from_score_run_out_schema_and_answers(
            score_response, answers
        )

    async def _get_score_run_async_impl(self, score_run_uuid: str) -> ScoreRunResponse:
        score_response = await get_score_run.asyncio(
            client=self.client, score_run_uuid=score_run_uuid
        )
        answers = None
        if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = await self._get_all_score_run_answers_async(score_run_uuid)

        return ScoreRunResponse.from_score_run_out_schema_and_answers(
            score_response, answers
        )

    # List Score Runs Methods
    def list_score_runs(
        self, test_uuid: Optional[str] = None
    ) -> List[ScoreRunResponse]:
        """
        List all score runs synchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: Optional[str]
        :return: List of score run responses.
        :rtype: List[ScoreRunResponse]
        """
        return self._list_score_runs(test_uuid, is_async=False)

    async def list_score_runs_async(
        self, test_uuid: Optional[str] = None
    ) -> List[ScoreRunResponse]:
        """
        List all score runs asynchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: Optional[str]
        :return: List of score run responses.
        :rtype: List[ScoreRunResponse]
        """
        return await self._list_score_runs(test_uuid, is_async=True)

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
            score_run_response = list_score_runs.sync(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            all_score_runs.extend(score_run_response.items)
            if len(all_score_runs) >= score_run_response.count:
                break
            offset += len(score_run_response.items)

        return [
            ScoreRunResponse.from_score_run_out_schema_and_answers(score_run)
            for score_run in all_score_runs
        ]

    async def _list_score_runs_async_impl(
        self, test_uuid: Optional[str] = None
    ) -> List[ScoreRunResponse]:
        all_score_runs = []
        offset = 0
        while True:
            score_run_response = await list_score_runs.asyncio(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            all_score_runs.extend(score_run_response.items)
            if len(all_score_runs) >= score_run_response.count:
                break
            offset += len(score_run_response.items)

        return [
            ScoreRunResponse.from_score_run_out_schema_and_answers(score_run)
            for score_run in all_score_runs
        ]

    # Helper Methods
    def _create_and_wait_for_score_impl_sync(
        self, score_data: models.ScoreRunSchema
    ) -> ScoreRunResponse:
        start_time = time.time()
        score_response = create_score_run.sync(client=self.client, body=score_data)
        score_run_uuid = score_response.score_run_uuid
        test_name = score_response.test.test_name

        with self.logger.progress_bar(
            test_name,
            score_run_uuid,
            Status.from_api_status(score_response.score_run_status),
        ):
            while True:
                score_response = get_score_run.sync(
                    client=self.client, score_run_uuid=score_run_uuid
                )

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

                if elapsed_time > self.max_wait_time:
                    score_response.score_run_status = models.ScoreRunStatus.FAILED
                    self.logger.update_progress_bar(score_run_uuid, Status.FAILED)
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Score run creation timed out."
                    )

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_score_impl_async(
        self, score_data: models.ScoreRunSchema
    ) -> ScoreRunResponse:
        start_time = time.time()
        score_response = await create_score_run.asyncio(
            client=self.client, body=score_data
        )
        score_run_uuid = score_response.score_run_uuid
        test_name = score_response.test.test_name

        with self.logger.progress_bar(
            test_name,
            score_run_uuid,
            Status.from_api_status(score_response.score_run_status),
        ):
            while True:
                score_response = await get_score_run.asyncio(
                    client=self.client, score_run_uuid=score_run_uuid
                )

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

                if elapsed_time > self.max_wait_time:
                    score_response.score_run_status = models.ScoreRunStatus.FAILED
                    self.logger.update_progress_bar(score_run_uuid, Status.FAILED)
                    return ScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, None, "Score run creation timed out."
                    )

                await asyncio.sleep(POLLING_INTERVAL)

    def _get_all_score_run_answers_sync(
        self, score_run_uuid: str
    ) -> List[models.AnswerSchema]:
        answers = []
        offset = 0
        while True:
            response = get_score_run_answers.sync(
                client=self.client, score_run_uuid=score_run_uuid, offset=offset
            )
            answers.extend(response.items)
            if len(answers) >= response.count:
                break
            offset += len(response.items)
        return answers

    async def _get_all_score_run_answers_async(
        self, score_run_uuid: str
    ) -> List[models.AnswerSchema]:
        answers = []
        offset = 0
        while True:
            response = await get_score_run_answers.asyncio(
                client=self.client, score_run_uuid=score_run_uuid, offset=offset
            )
            answers.extend(response.items)
            if len(answers) >= response.count:
                break
            offset += len(response.items)
        return answers

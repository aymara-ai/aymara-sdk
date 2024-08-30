import time
from typing import List
from aymara_sdk.constants import POLLING_INTERVAL
from aymara_sdk.errors import ScoreRunError
from aymara_sdk.generated.aymara_api_client.api.score_runs import (
    core_api_create_score_run,
    core_api_get_score_run,
    core_api_get_score_run_answers,
    core_api_list_score_runs,
)
from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.base import AymaraAIProtocol
from aymara_sdk.types import (
    CreateScoreRunResponse,
    GetScoreRunResponse,
    StudentAnswerInput,
    transform_api_status,
)


class ScoreRunSyncMixin(AymaraAIProtocol):
    def score_test(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswerInput],
    ) -> CreateScoreRunResponse:
        """
        Score a test synchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of StudentAnswerInput objects containing student responses.
        :type student_answers: List[StudentAnswerInput]
        :return: Score response.
        :rtype: CreateScoreRunResponse
        """

        score_response = self._create_and_wait_for_score(
            models.ScoreRunSchema(
                test_uuid=test_uuid,
                answers=[
                    StudentAnswerInput.to_answer_in_schema(student_answer)
                    for student_answer in student_answers
                ],
            )
        )

        return score_response

    def get_score_run(self, score_run_uuid: str) -> GetScoreRunResponse:
        """
        Get the current status of a score run synchronously, and answers if it is completed.

        :param score_run_uuid: UUID of the score run.
        :type score_run_uuid: str
        :return: Score run response.
        :rtype: GetScoreRunResponse
        """
        score_response = core_api_get_score_run.sync(
            client=self.client, score_run_uuid=score_run_uuid
        )
        answers = None
        if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = self._get_all_score_run_answers(score_run_uuid)

        return GetScoreRunResponse.from_score_run_out_schema_and_answers(
            score_response, answers
        )

    def list_score_runs(self, test_uuid: str) -> List[GetScoreRunResponse]:
        """
        List all score runs synchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: List of score run responses.
        :rtype: List[GetScoreRunResponse]
        """

        score_run_response = core_api_list_score_runs.sync(
            client=self.client, test_uuid=test_uuid
        )
        return [
            GetScoreRunResponse.from_score_run_out_schema_and_answers(score_run)
            for score_run in score_run_response
        ]

    def _create_and_wait_for_score(
        self, score_data: models.ScoreRunSchema
    ) -> CreateScoreRunResponse:
        """
        Create a score run synchronously and wait for its completion.

        :param score_data: Prepared score data.
        :type score_data: models.ScoreRunSchema
        :return: Score run response.
        :rtype: CreateScoreRunResponse
        """
        start_time = time.time()
        score_response = core_api_create_score_run.sync(
            client=self.client, body=score_data
        )
        score_run_uuid = score_response.score_run_uuid
        test_name = score_response.test.test_name

        with self.logger.progress_bar(
            test_name,
            score_run_uuid,
            transform_api_status(score_response.score_run_status),
        ):
            while True:
                score_response = core_api_get_score_run.sync(
                    client=self.client, score_run_uuid=score_run_uuid
                )

                self.logger.update_progress_bar(
                    score_run_uuid,
                    transform_api_status(score_response.score_run_status),
                )

                if score_response.score_run_status == models.ScoreRunStatus.FAILED:
                    raise ScoreRunError(f"Score run failed for {score_run_uuid}")

                if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
                    answers = self._get_all_score_run_answers(score_run_uuid)
                    return CreateScoreRunResponse.from_score_run_out_schema_and_answers(
                        score_response, answers
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    self.logger.error("Score run timed out for %s", score_run_uuid)
                    raise TimeoutError("Score run timed out")

                time.sleep(POLLING_INTERVAL)

    def _get_all_score_run_answers(
        self, score_run_uuid: str
    ) -> List[models.AnswerSchema]:
        """
        Get all answers for a score run synchronously.
        """
        answers = []
        offset = 0
        while True:
            response = core_api_get_score_run_answers.sync(
                client=self.client, score_run_uuid=score_run_uuid, offset=offset
            )
            answers.extend(response.items)
            if len(answers) >= response.count:
                break
            offset += len(response.items)
        return answers

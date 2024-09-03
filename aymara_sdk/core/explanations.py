import asyncio
import time
from typing import Coroutine, List, Union

from aymara_sdk.core.protocols import AymaraAIProtocol
from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.generated.aymara_api_client.api.score_runs import (
    create_score_runs_explanation,
    get_score_runs_explanation,
    list_score_runs_explanations,
)
from aymara_sdk.generated.aymara_api_client.models.score_runs_explanation_in_schema import (
    ScoreRunsExplanationInSchema,
)
from aymara_sdk.types import Status, ScoreRunResponse
from aymara_sdk.types.types import (
    ScoreRunsExplanationResponse,
)
from aymara_sdk.utils.constants import POLLING_INTERVAL


class ExplanationMixin(AymaraAIProtocol):
    def create_explanation(
        self, score_runs: Union[List[ScoreRunResponse], List[str]]
    ) -> ScoreRunsExplanationResponse:
        """
        Create explanations for a list of score runs and wait for completion synchronously.

        :param score_runs: List of score runs or their UUIDs for which to explain their unsafe or incorrect answers.
        :type score_run_uuids: Union[List[ScoreRunResponse], List[str]]
        :return: Explanation response.
        :rtype: ScoreRunsExplanationResponse
        """
        score_run_uuids = self._score_runs_to_score_run_uuids(score_runs)
        return self._create_explanation(score_run_uuids, is_async=False)

    async def create_explanation_async(
        self, score_runs: List[str]
    ) -> ScoreRunsExplanationResponse:
        """
        Create explanations for a list of score runs and wait for completion asynchronously.

        :param score_runs: List of score runs or their UUIDs for which to explain their unsafe or incorrect answers.
        :type score_run_uuids: Union[List[ScoreRunResponse], List[str]]
        :return: Explanation response.
        :rtype: ScoreRunsExplanationResponse
        """
        score_run_uuids = self._score_runs_to_score_run_uuids(score_runs)
        return await self._create_explanation(score_run_uuids, is_async=True)

    def _create_explanation(
        self, score_run_uuids: List[str], is_async: bool
    ) -> Union[
        ScoreRunsExplanationResponse,
        Coroutine[ScoreRunsExplanationResponse, None, None],
    ]:
        if is_async:
            return self._create_explanation_async_impl(score_run_uuids)
        else:
            return self._create_explanation_sync_impl(score_run_uuids)

    def _create_explanation_sync_impl(
        self, score_run_uuids: List[str]
    ) -> ScoreRunsExplanationResponse:
        start_time = time.time()
        explanation_response = create_score_runs_explanation.sync(
            client=self.client,
            body=ScoreRunsExplanationInSchema(
                score_run_uuids=score_run_uuids,
            ),
        )
        explanation_uuid = explanation_response.score_runs_explanation_uuid

        with self.logger.progress_bar(
            "Explanation",
            explanation_uuid,
            Status.from_api_status(explanation_response.status),
        ):
            while True:
                explanation_response = get_score_runs_explanation.sync(
                    client=self.client, explanation_uuid=explanation_uuid
                )

                self.logger.update_progress_bar(
                    explanation_uuid,
                    Status.from_api_status(explanation_response.status),
                )

                if explanation_response.status == models.ExplanationStatus.FAILED:
                    return ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                        explanation_response,
                        "Internal server error. Please try again.",
                    )

                if explanation_response.status == models.ExplanationStatus.FINISHED:
                    return ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                        explanation_response
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    explanation_response.status = models.ExplanationStatus.FAILED
                    self.logger.update_progress_bar(explanation_uuid, Status.FAILED)
                    return ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                        explanation_response,
                        failure_reason="Explanation creation timed out.",
                    )

                time.sleep(POLLING_INTERVAL)

    async def _create_explanation_async_impl(
        self, score_run_uuids: List[str]
    ) -> ScoreRunsExplanationResponse:
        start_time = time.time()
        explanation_response = await create_score_runs_explanation.asyncio(
            client=self.client,
            body=ScoreRunsExplanationInSchema(
                score_run_uuids=score_run_uuids,
            ),
        )
        explanation_uuid = explanation_response.score_runs_explanation_uuid

        with self.logger.progress_bar(
            "Explanation",
            explanation_uuid,
            Status.from_api_status(explanation_response.status),
        ):
            while True:
                explanation_response = await get_score_runs_explanation.asyncio(
                    client=self.client, explanation_uuid=explanation_uuid
                )

                self.logger.update_progress_bar(
                    explanation_uuid,
                    Status.from_api_status(explanation_response.status),
                )

                if explanation_response.status == models.ExplanationStatus.FAILED:
                    return ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                        explanation_response,
                        "Internal server error. Please try again.",
                    )

                if explanation_response.status == models.ExplanationStatus.FINISHED:
                    return ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                        explanation_response
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    explanation_response.status = models.ExplanationStatus.FAILED
                    self.logger.update_progress_bar(explanation_uuid, Status.FAILED)
                    return ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                        explanation_response,
                        failure_reason="Explanation creation timed out.",
                    )

                await asyncio.sleep(POLLING_INTERVAL)

    def _score_runs_to_score_run_uuids(self, score_runs):
        if isinstance(score_runs[0], ScoreRunResponse):
            return [score_run.score_run_uuid for score_run in score_runs]
        else:
            return score_runs

    # Get Explanation Methods
    def get_explanation(self, explanation_uuid: str) -> ScoreRunsExplanationResponse:
        """
        Get the current status of an explanation synchronously.

        :param explanation_uuid: UUID of the explanation.
        :type explanation_uuid: str
        :return: Explanation response.
        :rtype: ScoreRunsExplanationResponse
        """
        return self._get_explanation(explanation_uuid, is_async=False)

    async def get_explanation_async(
        self, explanation_uuid: str
    ) -> ScoreRunsExplanationResponse:
        """
        Get the current status of an explanation asynchronously.

        :param explanation_uuid: UUID of the explanation.
        :type explanation_uuid: str
        :return: Explanation response.
        :rtype: ScoreRunsExplanationResponse
        """
        return await self._get_explanation(explanation_uuid, is_async=True)

    def _get_explanation(
        self, explanation_uuid: str, is_async: bool
    ) -> Union[
        ScoreRunsExplanationResponse,
        Coroutine[ScoreRunsExplanationResponse, None, None],
    ]:
        if is_async:
            return self._get_explanation_async_impl(explanation_uuid)
        else:
            return self._get_explanation_sync_impl(explanation_uuid)

    def _get_explanation_sync_impl(
        self, explanation_uuid: str
    ) -> ScoreRunsExplanationResponse:
        explanation_response = get_score_runs_explanation.sync(
            client=self.client, explanation_uuid=explanation_uuid
        )
        return (
            ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                explanation_response
            )
        )

    async def _get_explanation_async_impl(
        self, explanation_uuid: str
    ) -> ScoreRunsExplanationResponse:
        explanation_response = await get_score_runs_explanation.asyncio(
            client=self.client, explanation_uuid=explanation_uuid
        )
        return (
            ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                explanation_response
            )
        )

    # List Explanations Methods
    def list_explanations(self) -> List[ScoreRunsExplanationResponse]:
        """
        List all explanations synchronously.
        """
        return self._list_explanations_sync_impl()

    async def list_explanations_async(self) -> List[ScoreRunsExplanationResponse]:
        """
        List all explanations asynchronously.
        """
        return await self._list_explanations_async_impl()

    def _list_explanations_sync_impl(self) -> List[ScoreRunsExplanationResponse]:
        explanation_response = list_score_runs_explanations.sync(client=self.client)
        return [
            ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                explanation
            )
            for explanation in explanation_response
        ]

    async def _list_explanations_async_impl(self) -> List[ScoreRunsExplanationResponse]:
        explanation_response = await list_score_runs_explanations.asyncio(
            client=self.client
        )
        return [
            ScoreRunsExplanationResponse.from_explanation_out_schema_and_failure_reason(
                explanation
            )
            for explanation in explanation_response
        ]

import asyncio
import time
from typing import Coroutine, List, Union

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.score_runs import (
    create_score_run_suite_summary,
    delete_score_run_suite_summary,
    get_score_run_suite_summary,
    list_score_run_suite_summaries,
)
from aymara_ai.generated.aymara_api_client.models.score_run_suite_summary_in_schema import (
    ScoreRunSuiteSummaryInSchema,
)
from aymara_ai.types import (
    ScoreRunResponse,
    ScoreRunSuiteSummaryResponse,
    Status,
)
from aymara_ai.utils.constants import (
    DEFAULT_SUMMARY_MAX_WAIT_TIME_SECS,
    POLLING_INTERVAL,
)


class SummaryMixin(AymaraAIProtocol):
    def create_summary(
        self,
        score_runs: Union[List[ScoreRunResponse], List[str]],
        is_sandbox: bool = False,
    ) -> ScoreRunSuiteSummaryResponse:
        """
        Create summaries for a list of score runs and wait for completion synchronously.

        :param score_runs: List of score runs or their UUIDs for which to create summaries.
        :type score_run_uuids: Union[List[ScoreRunResponse], List[str]]
        :return: Summary response.
        :rtype: ScoreRunSuiteSummaryResponse
        """
        return self._create_summary(score_runs, is_async=False, is_sandbox=is_sandbox)

    async def create_summary_async(
        self, score_runs: Union[List[ScoreRunResponse], List[str]]
    ) -> ScoreRunSuiteSummaryResponse:
        """
        Create summaries for a list of score runs and wait for completion asynchronously.

        :param score_runs: List of score runs or their UUIDs for which to create summaries.
        :type score_run_uuids: Union[List[ScoreRunResponse], List[str]]
        :return: Summary response.
        :rtype: ScoreRunsSummaryResponse
        """
        return await self._create_summary(score_runs, is_async=True)

    def _create_summary(
        self,
        score_runs: Union[List[ScoreRunResponse], List[str]],
        is_async: bool,
        is_sandbox: bool = False,
    ) -> Union[
        ScoreRunSuiteSummaryResponse,
        Coroutine[ScoreRunSuiteSummaryResponse, None, None],
    ]:
        if len(score_runs) == 0:
            raise ValueError("At least one score run must be provided")
        score_run_uuids = self._score_runs_to_score_run_uuids(score_runs)
        if is_async:
            return self._create_summary_async_impl(score_run_uuids, is_sandbox)
        else:
            return self._create_summary_sync_impl(score_run_uuids, is_sandbox)

    def _create_summary_sync_impl(
        self, score_run_uuids: List[str], is_sandbox: bool = False
    ) -> ScoreRunSuiteSummaryResponse:
        start_time = time.time()
        response = create_score_run_suite_summary.sync_detailed(
            client=self.client,
            body=ScoreRunSuiteSummaryInSchema(
                score_run_uuids=score_run_uuids,
            ),
            is_sandbox=is_sandbox,
        )

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        summary_response = response.parsed
        summary_uuid = summary_response.score_run_suite_summary_uuid

        remaining_summaries = summary_response.remaining_summaries

        if remaining_summaries is not None:
            summary_plural = "summary" if remaining_summaries == 1 else "summaries"
            self.logger.warning(
                f"You have {remaining_summaries} {summary_plural} remaining. To upgrade, visit https://aymara.ai/upgrade."
            )

        with self.logger.progress_bar(
            "Summary",
            summary_uuid,
            Status.from_api_status(summary_response.status),
        ):
            while True:
                response = get_score_run_suite_summary.sync_detailed(
                    client=self.client, summary_uuid=summary_uuid
                )

                if response.status_code == 404:
                    raise ValueError(f"Summary with UUID {summary_uuid} not found")

                if response.status_code == 422:
                    raise ValueError(f"{response.parsed.detail}")

                summary_response = response.parsed

                self.logger.update_progress_bar(
                    summary_uuid,
                    Status.from_api_status(summary_response.status),
                )

                if summary_response.status == models.ScoreRunSuiteSummaryStatus.FAILED:
                    return ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                        summary_response,
                        "Internal server error. Please try again.",
                    )

                elapsed_time = time.time() - start_time

                if elapsed_time >= DEFAULT_SUMMARY_MAX_WAIT_TIME_SECS:
                    summary_response.status = models.ScoreRunSuiteSummaryStatus.FAILED
                    self.logger.update_progress_bar(summary_uuid, Status.FAILED)
                    return ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                        summary_response,
                        failure_reason="Summary creation timed out.",
                    )

                if (
                    summary_response.status
                    == models.ScoreRunSuiteSummaryStatus.FINISHED
                ):
                    return ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                        summary_response
                    )

                time.sleep(POLLING_INTERVAL)

    async def _create_summary_async_impl(
        self, score_run_uuids: List[str], is_sandbox: bool = False
    ) -> ScoreRunSuiteSummaryResponse:
        start_time = time.time()
        response = await create_score_run_suite_summary.asyncio_detailed(
            client=self.client,
            body=ScoreRunSuiteSummaryInSchema(
                score_run_uuids=score_run_uuids,
            ),
            is_sandbox=is_sandbox,
        )

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        summary_response = response.parsed
        summary_uuid = summary_response.score_run_suite_summary_uuid

        remaining_summaries = summary_response.remaining_summaries

        if remaining_summaries is not None:
            summary_plural = "summary" if remaining_summaries == 1 else "summaries"
            self.logger.warning(
                f"You have {remaining_summaries} {summary_plural} remaining. To upgrade, visit https://aymara.ai/upgrade."
            )

        with self.logger.progress_bar(
            "Summary",
            summary_uuid,
            Status.from_api_status(summary_response.status),
        ):
            while True:
                response = await get_score_run_suite_summary.asyncio_detailed(
                    client=self.client, summary_uuid=summary_uuid
                )

                if response.status_code == 404:
                    raise ValueError(f"Summary with UUID {summary_uuid} not found")

                if response.status_code == 422:
                    raise ValueError(f"{response.parsed.detail}")

                summary_response = response.parsed

                self.logger.update_progress_bar(
                    summary_uuid,
                    Status.from_api_status(summary_response.status),
                )

                elapsed_time = time.time() - start_time

                if elapsed_time >= DEFAULT_SUMMARY_MAX_WAIT_TIME_SECS:
                    summary_response.status = models.ScoreRunSuiteSummaryStatus.FAILED
                    self.logger.update_progress_bar(summary_uuid, Status.FAILED)
                    return ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                        summary_response,
                        failure_reason="Summary creation timed out.",
                    )

                if summary_response.status == models.ScoreRunSuiteSummaryStatus.FAILED:
                    return ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                        summary_response,
                        "Internal server error. Please try again.",
                    )

                if (
                    summary_response.status
                    == models.ScoreRunSuiteSummaryStatus.FINISHED
                ):
                    return ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                        summary_response
                    )

                await asyncio.sleep(POLLING_INTERVAL)

    def _score_runs_to_score_run_uuids(self, score_runs):
        if isinstance(score_runs[0], ScoreRunResponse):
            return [score_run.score_run_uuid for score_run in score_runs]
        else:
            return score_runs

    # Get Summary Methods
    def get_summary(self, summary_uuid: str) -> ScoreRunSuiteSummaryResponse:
        """
        Get the current status of an summary synchronously.

        :param summary_uuid: UUID of the summary.
            :type summary_uuid: str
        :return: Summary response.
        :rtype: ScoreRunSuiteSummaryResponse
        """
        return self._get_summary(summary_uuid, is_async=False)

    async def get_summary_async(
        self, summary_uuid: str
    ) -> ScoreRunSuiteSummaryResponse:
        """
        Get the current status of an summary asynchronously.

        :param summary_uuid: UUID of the summary.
        :type summary_uuid: str
        :return: Summary response.
        :rtype: ScoreRunSuiteSummaryResponse
        """
        return await self._get_summary(summary_uuid, is_async=True)

    def _get_summary(
        self, summary_uuid: str, is_async: bool
    ) -> Union[
        ScoreRunSuiteSummaryResponse,
        Coroutine[ScoreRunSuiteSummaryResponse, None, None],
    ]:
        if is_async:
            return self._get_summary_async_impl(summary_uuid)
        else:
            return self._get_summary_sync_impl(summary_uuid)

    def _get_summary_sync_impl(self, summary_uuid: str) -> ScoreRunSuiteSummaryResponse:
        response = get_score_run_suite_summary.sync_detailed(
            client=self.client, summary_uuid=summary_uuid
        )
        if response.status_code == 404:
            raise ValueError(f"Summary with UUID {summary_uuid} not found")
        summary_response = response.parsed
        return ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
            summary_response
        )

    async def _get_summary_async_impl(
        self, summary_uuid: str
    ) -> ScoreRunSuiteSummaryResponse:
        response = await get_score_run_suite_summary.asyncio_detailed(
            client=self.client, summary_uuid=summary_uuid
        )
        if response.status_code == 404:
            raise ValueError(f"Summary with UUID {summary_uuid} not found")
        summary_response = response.parsed
        return ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
            summary_response
        )

    # List Summaries Methods
    def list_summaries(self) -> List[ScoreRunSuiteSummaryResponse]:
        """
        List all summaries synchronously.
        """
        return self._list_summaries_sync_impl()

    async def list_summaries_async(self) -> List[ScoreRunSuiteSummaryResponse]:
        """
        List all summaries asynchronously.
        """
        return await self._list_summaries_async_impl()

    def _list_summaries_sync_impl(self) -> List[ScoreRunSuiteSummaryResponse]:
        all_summaries = []
        offset = 0
        while True:
            response = list_score_run_suite_summaries.sync_detailed(
                client=self.client, offset=offset
            )
            paged_response = response.parsed
            all_summaries.extend(paged_response.items)
            if len(all_summaries) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                summary
            )
            for summary in all_summaries
        ]

    async def _list_summaries_async_impl(self) -> List[ScoreRunSuiteSummaryResponse]:
        all_summaries = []
        offset = 0
        while True:
            response = await list_score_run_suite_summaries.asyncio_detailed(
                client=self.client, offset=offset
            )
            paged_response = response.parsed
            all_summaries.extend(paged_response.items)
            if len(all_summaries) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            ScoreRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                summary
            )
            for summary in all_summaries
        ]

    def delete_summary(self, summary_uuid: str) -> None:
        """
        Delete a summary synchronously.

        :param summary_uuid: UUID of the summary.
        :type summary_uuid: str
        """
        response = delete_score_run_suite_summary.sync_detailed(
            client=self.client, summary_uuid=summary_uuid
        )

        if response.status_code == 404:
            raise ValueError(f"Summary with UUID {summary_uuid} not found")
        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

    async def delete_summary_async(self, summary_uuid: str) -> None:
        """
        Delete a summary asynchronously.

        :param summary_uuid: UUID of the summary.
        :type summary_uuid: str
        """
        response = await delete_score_run_suite_summary.asyncio_detailed(
            client=self.client, summary_uuid=summary_uuid
        )

        if response.status_code == 404:
            raise ValueError(f"Summary with UUID {summary_uuid} not found")
        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

import asyncio
import time
from typing import Coroutine, List, Union

from aymara_ai.core.errors import get_parsed_response
from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client.api.eval_runs import (
    create_eval_run_suite_summary,
    delete_eval_run_suite_summary,
    get_eval_run_suite_summary,
    list_eval_run_suite_summaries,
)
from aymara_ai.generated.aymara_api_client.models.eval_run_suite_summary_in_schema import (
    EvalRunSuiteSummaryInSchema,
)
from aymara_ai.utils.async_utils import run_async
from aymara_ai.utils.constants import (
    DEFAULT_SUMMARY_MAX_WAIT_TIME_SECS,
    POLLING_INTERVAL,
)
from aymara_ai.v2_types import (
    EvalRunResponse,
    EvalRunSuiteSummaryResponse,
    Status,
)


class EvalSummaryMixin(AymaraAIProtocol):
    def summarize_eval_runs(
        self,
        eval_runs: Union[List[EvalRunResponse], List[str]],
        is_sandbox: bool = False,
    ) -> EvalRunSuiteSummaryResponse:
        """
        Create summaries for a list of score runs and wait for completion synchronously.

        :param eval_runs: List of score runs or their UUIDs for which to create summaries.
        :type eval_run_uuids: Union[List[EvalRunResponse], List[str]]
        :return: Summary response.
        :rtype: EvalRunSuiteSummaryResponse
        """
        return run_async(self._summarize_eval_runs(eval_runs, is_sandbox=is_sandbox))

    async def create_summary_async(
        self, eval_runs: Union[List[EvalRunResponse], List[str]]
    ) -> EvalRunSuiteSummaryResponse:
        """
        Create summaries for a list of score runs and wait for completion asynchronously.

        :param eval_runs: List of score runs or their UUIDs for which to create summaries.
        :type eval_run_uuids: Union[List[EvalRunResponse], List[str]]
        :return: Summary response.
        :rtype: EvalRunsSummaryResponse
        """
        return await self._summarize_eval_runs(eval_runs)

    async def _summarize_eval_runs(
        self,
        eval_runs: Union[List[EvalRunResponse], List[str]],
        is_sandbox: bool = False,
    ) -> Union[
        EvalRunSuiteSummaryResponse,
        Coroutine[EvalRunSuiteSummaryResponse, None, None],
    ]:
        if len(eval_runs) == 0:
            raise ValueError("At least one score run must be provided")
        eval_run_uuids = self._eval_runs_to_uuids(eval_runs)
        return await self._summarize_eval_runs_async_impl(eval_run_uuids, is_sandbox)

    async def _summarize_eval_runs_async_impl(
        self, eval_run_uuids: List[str], is_sandbox: bool = False
    ) -> EvalRunSuiteSummaryResponse:
        start_time = time.time()
        response = await create_eval_run_suite_summary.asyncio_detailed(
            client=self.client,
            body=EvalRunSuiteSummaryInSchema(
                eval_run_uuids=eval_run_uuids,
            ),
            is_sandbox=is_sandbox,
        )

        summary_response = get_parsed_response(response)
        summary_uuid = summary_response.eval_run_suite_summary_uuid

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
                response = await get_eval_run_suite_summary.asyncio_detailed(
                    client=self.client, summary_uuid=summary_uuid
                )

                summary_response = get_parsed_response(response)

                self.logger.update_progress_bar(
                    summary_uuid,
                    Status.from_api_status(summary_response.status),
                )

                elapsed_time = time.time() - start_time

                if elapsed_time >= DEFAULT_SUMMARY_MAX_WAIT_TIME_SECS:
                    summary_response.status = Status.FAILED
                    self.logger.update_progress_bar(summary_uuid, Status.FAILED)
                    return EvalRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                        summary_response,
                        failure_reason="Summary creation timed out.",
                    )

                if summary_response.status == Status.FAILED:
                    return EvalRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(
                        summary_response,
                        "Internal server error. Please try again.",
                    )

                if Status.from_api_status(summary_response.status) == Status.COMPLETED:
                    return EvalRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(summary_response)

                await asyncio.sleep(POLLING_INTERVAL)

    def _eval_runs_to_uuids(self, eval_runs):
        if isinstance(eval_runs[0], EvalRunResponse):
            return [eval_run.eval_run_uuid for eval_run in eval_runs]
        else:
            return eval_runs

    # Get Summary Methods
    def get_eval_summary(self, summary_uuid: str) -> EvalRunSuiteSummaryResponse:
        """
        Get the current status of an summary synchronously.

        :param summary_uuid: UUID of the summary.
            :type summary_uuid: str
        :return: Summary response.
        :rtype: EvalRunSuiteSummaryResponse
        """
        return self._get_eval_summary(summary_uuid, is_async=False)

    async def get_eval_summary_async(self, summary_uuid: str) -> EvalRunSuiteSummaryResponse:
        """
        Get the current status of an summary asynchronously.

        :param summary_uuid: UUID of the summary.
        :type summary_uuid: str
        :return: Summary response.
        :rtype: EvalRunSuiteSummaryResponse
        """
        return await self._get_eval_summary(summary_uuid, is_async=True)

    def _get_eval_summary(
        self, summary_uuid: str, is_async: bool
    ) -> Union[
        EvalRunSuiteSummaryResponse,
        Coroutine[EvalRunSuiteSummaryResponse, None, None],
    ]:
        if is_async:
            return self._get_eval_summary_async_impl(summary_uuid)
        else:
            return self._get_eval_summary_sync_impl(summary_uuid)

    def _get_eval_summary_sync_impl(self, summary_uuid: str) -> EvalRunSuiteSummaryResponse:
        response = get_eval_run_suite_summary.sync_detailed(client=self.client, summary_uuid=summary_uuid)
        summary_response = get_parsed_response(response)
        return EvalRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(summary_response)

    async def _get_eval_summary_async_impl(self, summary_uuid: str) -> EvalRunSuiteSummaryResponse:
        response = await get_eval_run_suite_summary.asyncio_detailed(client=self.client, summary_uuid=summary_uuid)
        summary_response = get_parsed_response(response)
        return EvalRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(summary_response)

    # List Summaries Methods
    def list_eval_summaries(self) -> List[EvalRunSuiteSummaryResponse]:
        """
        List all summaries synchronously.
        """
        return self._list_eval_summaries_sync_impl()

    async def list_eval_summaries_async(self) -> List[EvalRunSuiteSummaryResponse]:
        """
        List all summaries asynchronously.
        """
        return await self._list_eval_summaries_async_impl()

    def _list_eval_summaries_sync_impl(self) -> List[EvalRunSuiteSummaryResponse]:
        all_summaries = []
        offset = 0
        while True:
            response = list_eval_run_suite_summaries.sync_detailed(client=self.client, offset=offset)
            paged_response = get_parsed_response(response)
            all_summaries.extend(paged_response.items)
            if len(all_summaries) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            EvalRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(summary) for summary in all_summaries
        ]

    async def _list_eval_summaries_async_impl(self) -> List[EvalRunSuiteSummaryResponse]:
        all_summaries = []
        offset = 0
        while True:
            response = await list_eval_run_suite_summaries.asyncio_detailed(client=self.client, offset=offset)
            paged_response = get_parsed_response(response)
            all_summaries.extend(paged_response.items)
            if len(all_summaries) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            EvalRunSuiteSummaryResponse.from_summary_out_schema_and_failure_reason(summary) for summary in all_summaries
        ]

    def delete_eval_summary(self, summary_uuid: str) -> None:
        """
        Delete a summary synchronously.

        :param summary_uuid: UUID of the summary.
        :type summary_uuid: str
        """
        response = delete_eval_run_suite_summary.sync_detailed(client=self.client, summary_uuid=summary_uuid)

        get_parsed_response(response)

    async def delete_eval_summary_async(self, summary_uuid: str) -> None:
        """
        Delete a summary asynchronously.

        :param summary_uuid: UUID of the summary.
        :type summary_uuid: str
        """
        response = await delete_eval_run_suite_summary.asyncio_detailed(client=self.client, summary_uuid=summary_uuid)

        get_parsed_response(response)

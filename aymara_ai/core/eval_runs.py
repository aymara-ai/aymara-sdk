import asyncio
import os
import time
from typing import List, Optional

from aymara_ai.core.errors import AymaraError, get_parsed_response
from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.core.uploads import UploadMixin
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.eval_runs import (
    create_eval_run,
    delete_eval_run,
    get_eval_run,
    get_eval_run_responses,
    list_eval_runs,
)
from aymara_ai.generated.aymara_api_client.api.evals import get_eval
from aymara_ai.generated.aymara_api_client.models.content_type import ContentType
from aymara_ai.generated.aymara_api_client.models.error_code import ErrorCode
from aymara_ai.generated.aymara_api_client.models.eval_out_schema import EvalOutSchema
from aymara_ai.generated.aymara_api_client.models.eval_response_in_schema import EvalResponseInSchema
from aymara_ai.generated.aymara_api_client.models.eval_response_out_schema import EvalResponseOutSchema
from aymara_ai.generated.aymara_api_client.models.eval_run_example_in_schema import EvalRunExampleInSchema
from aymara_ai.generated.aymara_api_client.models.eval_run_in_schema import EvalRunInSchema
from aymara_ai.generated.aymara_api_client.models.eval_run_out_schema import EvalRunOutSchema
from aymara_ai.generated.aymara_api_client.models.eval_run_turn_out_schema import EvalRunTurnOutSchema
from aymara_ai.generated.aymara_api_client.models.paged_eval_response_out_schema import PagedEvalResponseOutSchema
from aymara_ai.generated.aymara_api_client.models.paged_eval_run_out_schema import PagedEvalRunOutSchema
from aymara_ai.generated.aymara_api_client.models.status import Status
from aymara_ai.types import Status as SdkStatus
from aymara_ai.utils.async_utils import run_async
from aymara_ai.utils.constants import (
    DEFAULT_MAX_WAIT_TIME_SECS,
    MAX_EXAMPLES_LENGTH,
    POLLING_INTERVAL,
)
from aymara_ai.v2_types import EvalRunResponse, ListEvalRunResponse


class EvalRunMixin(UploadMixin, AymaraAIProtocol):
    """
    Mixin class that provides eval run functionality.
    Inherits from UploadMixin to get image upload capabilities.
    """

    # Run Eval Methods
    def score_responses(
        self,
        eval_uuid: str,
        ai_responses: List[EvalResponseInSchema],
        *,
        name: Optional[str] = None,
        ai_description: Optional[str] = None,
        eval_run_uuid: Optional[str] = None,
        eval_examples: Optional[List[EvalRunExampleInSchema]] = None,
        generate_prompts: bool = False,
        max_wait_time_secs: Optional[int] = DEFAULT_MAX_WAIT_TIME_SECS,
        is_sandbox: Optional[bool] = False,
    ) -> EvalRunResponse:
        return run_async(
            self._run_eval(
                eval_uuid=eval_uuid,
                eval_run_uuid=eval_run_uuid,
                name=name,
                generate_prompts=generate_prompts,
                ai_responses=ai_responses,
                ai_description=ai_description,
                max_wait_time_secs=max_wait_time_secs,
                eval_examples=eval_examples,
                is_sandbox=is_sandbox,
            )
        )

    score_responses.__doc__ = f"""
        Run an eval synchronously.

        :param eval_uuid: UUID of the eval.
        :type eval_uuid: str
        :param ai_responses: List of EvalRunExampleInSchema objects containing prompt responses.
        :type prompt_responses: List[BasePromptResponseInput]
        :param eval_examples: Optional list of examples to guide the eval process.
        :type eval_examples: Optional[List[EvalExample]]
        :param max_wait_time_secs: Maximum wait time for eval run, defaults to {DEFAULT_MAX_WAIT_TIME_SECS}.
        :type max_wait_time_secs: int, optional
        :return: Eval run response.
        :rtype: EvalRunResponse
        """

    async def score_responses_async(
        self,
        eval_uuid: str,
        ai_responses: List[EvalResponseInSchema],
        *,
        name: Optional[str] = None,
        generate_prompts: bool = False,
        ai_description: Optional[str] = None,
        eval_run_uuid: Optional[str] = None,
        eval_examples: Optional[List[EvalRunExampleInSchema]] = None,
        max_wait_time_secs: Optional[int] = None,
        is_sandbox: Optional[bool] = False,
    ) -> EvalRunResponse:
        return await self._run_eval(
            eval_uuid=eval_uuid,
            name=name,
            generate_prompts=generate_prompts,
            ai_responses=ai_responses,
            ai_description=ai_description,
            eval_run_uuid=eval_run_uuid,
            eval_examples=eval_examples,
            max_wait_time_secs=max_wait_time_secs,
            is_sandbox=is_sandbox,
        )

    score_responses_async.__doc__ = f"""
        Run an eval asynchronously.

        :param eval_uuid: UUID of the eval.
        :type eval_uuid: str
        :param prompt_responses: List of BasePromptResponseInput objects containing prompt responses.
        :type prompt_responses: List[BasePromptResponseInput]
        :param eval_examples: Optional list of examples to guide the eval process.
        :type eval_examples: Optional[List[EvalExample]]
        :param max_wait_time_secs: Maximum wait time for eval run, defaults to {DEFAULT_MAX_WAIT_TIME_SECS}.
        :type max_wait_time_secs: optional, int
        :return: Eval run response.
        :rtype: EvalRunResponse
        """

    async def _run_eval(
        self,
        eval_uuid: str,
        ai_responses: List[EvalResponseInSchema],
        *,
        name: Optional[str] = None,
        generate_prompts: bool = False,
        ai_description: Optional[str] = None,
        max_wait_time_secs: Optional[int] = None,
        eval_run_uuid: Optional[str] = None,
        eval_examples: Optional[List[EvalRunExampleInSchema]] = None,
        is_sandbox: Optional[bool] = False,
    ) -> EvalRunTurnOutSchema:
        self._validate_prompt_responses(ai_responses)

        if eval_examples is not None:
            self._validate_eval_examples(eval_examples)

        api_payload = EvalRunInSchema(
            eval_uuid=eval_uuid,
            eval_run_uuid=eval_run_uuid,
            name=name,
            responses=ai_responses,
            eval_run_examples=eval_examples,
            ai_description=ai_description,
            generate_prompts=generate_prompts,
        )

        return await self._create_and_wait_for_eval_scores_async(api_payload, max_wait_time_secs, is_sandbox)

    # Get Eval Run Methods
    def get_eval_run(self, eval_run_uuid: str) -> EvalRunResponse:
        """
        Get the current status of an eval run synchronously, and prompt responses if it is completed.

        :param eval_run_uuid: UUID of the eval run.
        :type eval_run_uuid: str
        :return: Eval run response.
        :rtype: EvalRunResponse
        """
        # Pass eval_run_uuid as eval_run_uuid to the internal method
        return run_async(self._get_eval_run_async_impl(eval_run_uuid))

    async def get_eval_run_async(self, eval_run_uuid: str) -> EvalRunResponse:
        """
        Get the current status of an eval run asynchronously, and prompt responses if it is completed.

        :param eval_run_uuid: UUID of the eval run.
        :type eval_run_uuid: str
        :return: Eval run response.
        :rtype: EvalRunResponse
        """
        # Pass eval_run_uuid as eval_run_uuid to the internal method
        return await self._get_eval_run_async_impl(eval_run_uuid)

    async def _get_eval_run_async_impl(self, eval_run_uuid: str) -> EvalRunResponse:
        # Calls the eval_run API endpoint using the provided eval_run_uuid
        response = await get_eval_run.asyncio_detailed(client=self.client, eval_run_uuid=eval_run_uuid)

        score_response: EvalRunOutSchema = get_parsed_response(response)
        answers = None
        if score_response.status == Status.FINISHED:
            # Fetch answers using the eval_run API endpoint
            answers = await self._get_all_eval_run_responses_async(eval_run_uuid)

        eval_run = EvalRunResponse(eval_run_uuid=score_response.eval_run_uuid, run=score_response, responses=answers)

        return eval_run

    # List Eval Runs Methods
    def list_eval_runs(self, eval_uuid: Optional[str] = None) -> ListEvalRunResponse:
        """
        List all eval runs synchronously.

        :param eval_uuid: UUID of the eval to filter by.
        :type eval_uuid: Optional[str]
        :return: List of eval run responses.
        :rtype: ListEvalRunResponse
        """
        return run_async(self._list_eval_runs_async_impl(eval_uuid=eval_uuid))

    async def list_eval_runs_async(self, eval_uuid: Optional[str] = None) -> ListEvalRunResponse:
        """
        List all eval runs asynchronously.

        :param eval_uuid: UUID of the eval to filter by.
        :type eval_uuid: Optional[str]
        :return: List of eval run responses.
        :rtype: ListEvalRunResponse
        """

        return await self._list_eval_runs_async_impl(eval_uuid=eval_uuid)

    async def _list_eval_runs_async_impl(self, eval_uuid: Optional[str] = None) -> ListEvalRunResponse:
        # Calls the eval_runs API endpoint, passing eval_uuid as eval_uuid
        all_eval_runs: List[EvalRunOutSchema] = []
        offset = 0
        while True:
            response = await list_eval_runs.asyncio_detailed(client=self.client, eval_uuid=eval_uuid, offset=offset)
            paged_response: PagedEvalRunOutSchema = get_parsed_response(response)
            all_eval_runs.extend(paged_response.items)
            if len(all_eval_runs) >= paged_response.count:
                break
            offset += len(paged_response.items)

        # Adapt each ScoreRunOutSchema to EvalRunResponse
        return ListEvalRunResponse(
            root=[
                EvalRunResponse(run=e, eval_run_uuid=e.eval_run_uuid, failure_reason=None, responses=None)
                for e in all_eval_runs
            ]
        )

    async def _create_and_wait_for_eval_scores_async(
        self,
        eval_run_payload: EvalRunInSchema,
        max_wait_time_secs: Optional[int] = None,
        is_sandbox: Optional[bool] = False,
    ) -> EvalRunResponse:  # Returns EvalRunResponse
        start_time = time.time()

        # Generate a unique temporary UUID for the progress bar
        temp_uuid = f"pending_{id(eval_run_payload)}"  # Use object id to make unique

        response = await get_eval.asyncio_detailed(client=self.client, eval_uuid=eval_run_payload.eval_uuid)
        eval: EvalOutSchema = get_parsed_response(response)  # Represents the underlying Eval/Test

        if max_wait_time_secs is None:
            max_wait_time_secs = DEFAULT_MAX_WAIT_TIME_SECS
        modality = eval.modality

        with self.logger.progress_bar(
            eval.name,  # Use the name from the underlying eval
            temp_uuid,  # Will be updated with real UUID after creation
            Status.PROCESSING,
            upload_total=len([a for a in eval_run_payload.responses]),  # Check answers in score_data
        ) as pbar:
            # Image upload logic remains the same
            if modality == models.ContentType.IMAGE:
                uploaded_keys = await self.upload_images_async(
                    eval_run_payload.eval_run_uuid,
                    eval_run_payload.responses,
                    progress_callback=lambda n: pbar.update_upload_progress(n),
                )

                for answer in eval_run_payload.responses:
                    if answer.content and answer.prompt_uuid in uploaded_keys:
                        answer.content = uploaded_keys[answer.prompt_uuid]

            # Call create_eval_run API
            response = await create_eval_run.asyncio_detailed(
                client=self.client, body=eval_run_payload, is_sandbox=is_sandbox
            )

            eval_resp: EvalRunOutSchema = get_parsed_response(response)  # ScoreRunOutSchema
            eval_run_uuid = eval_resp.eval_run_uuid
            pbar.update_uuid(eval_run_uuid)  # Update progress bar with the actual run UUID

            # Continue with polling loop using get_eval_run API
            while True:
                response = await get_eval_run.asyncio_detailed(client=self.client, eval_run_uuid=eval_run_uuid)

                eval_resp: EvalRunOutSchema = get_parsed_response(response)  # ScoreRunOutSchema
                eval_run = EvalRunResponse(eval_run_uuid=eval_resp.eval_run_uuid, run=eval_resp)

                self.logger.update_progress_bar(
                    eval_run_uuid,
                    SdkStatus.from_api_status(eval_resp.status),
                )

                elapsed_time = time.time() - start_time

                if elapsed_time > max_wait_time_secs:
                    eval_resp.status = Status.FAILED
                    self.logger.update_progress_bar(eval_run_uuid, SdkStatus.from_api_status(Status.FAILED))
                    # Adapt to EvalRunResponse on timeout
                    raise AymaraError(ErrorCode.SERVER_INTERNAL_ERROR, "Eval run timed out.")
                if eval_resp.status == Status.FAILED:
                    # Adapt to EvalRunResponse on failure
                    raise AymaraError(ErrorCode.SERVER_INTERNAL_ERROR, "Internal server error. Please try again.")

                if eval_resp.status == Status.FINISHED:
                    # Fetch answers using eval_run API
                    answers = await self._get_all_eval_run_responses_async(eval_run_uuid)
                    # Adapt to EvalRunResponse on success
                    eval_run.responses = answers
                    return eval_run

                await asyncio.sleep(POLLING_INTERVAL)

    async def _get_all_eval_run_responses_async(self, eval_run_uuid: str) -> List[EvalResponseOutSchema]:
        answers = []
        offset = 0
        while True:
            response = await get_eval_run_responses.asyncio_detailed(
                client=self.client, eval_run_uuid=eval_run_uuid, offset=offset
            )

            paged_response: PagedEvalResponseOutSchema = get_parsed_response(response)
            answers.extend(paged_response.items)
            if len(answers) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return answers

    # Validation Methods (Updated for Eval terminology)
    def _validate_prompt_responses(self, prompt_responses: List[EvalResponseInSchema]):
        if not prompt_responses:
            raise ValueError("Prompt responses cannot be empty.")

        if any(resp.content_type == ContentType.IMAGE for resp in prompt_responses):
            # Filter only ImagePromptResponseInput for path validation
            image_responses = [resp for resp in prompt_responses if resp.content_type == models.ContentType.IMAGE]
            self._validate_image_paths_in_responses(image_responses)

    def _validate_image_paths_in_responses(self, image_responses: List[EvalResponseInSchema]):
        for response in image_responses:
            # Check the 'answer_image_path' attribute which maps to the API's answer image path
            if response.content:
                if not os.path.exists(response.content):
                    self.logger.error(f"Image path does not exist: {response.content}")
                    raise ValueError(f"Image path does not exist: {response.content}")

    def _validate_eval_examples(self, eval_examples: List[EvalRunExampleInSchema]):
        if len(eval_examples) > MAX_EXAMPLES_LENGTH:
            raise ValueError(f"Eval examples must be less than {MAX_EXAMPLES_LENGTH}.")
        if not all(isinstance(example, EvalRunExampleInSchema) for example in eval_examples):
            invalid_examples = [example for example in eval_examples if not isinstance(example, EvalRunExampleInSchema)]
            self.logger.error(f"Invalid examples: {invalid_examples}")
            raise ValueError("All items in eval examples must be EvalExample.")

    # Delete Methods (Updated for Eval terminology)
    def delete_eval_run(self, eval_run_uuid: str) -> None:
        """
        Delete an eval run synchronously.

        :param eval_run_uuid: UUID of the eval run.
        :type eval_run_uuid: str
        """
        # Call the eval_run API endpoint using the provided eval_run_uuid
        response = delete_eval_run.sync_detailed(client=self.client, eval_run_uuid=eval_run_uuid)

        get_parsed_response(response)

    async def delete_eval_run_async(self, eval_run_uuid: str) -> None:
        """
        Delete an eval run asynchronously.

        :param eval_run_uuid: UUID of the eval run.
        :type eval_run_uuid: str
        """
        # Call the eval_run API endpoint using the provided eval_run_uuid
        response = await delete_eval_run.asyncio_detailed(client=self.client, eval_run_uuid=eval_run_uuid)

        get_parsed_response(response)

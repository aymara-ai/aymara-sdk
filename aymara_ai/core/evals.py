import asyncio
import time
from typing import List, Optional, Union

from aymara_ai.core.errors import AymaraError, get_parsed_response
from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client.api.evals import (
    create_eval,
    delete_eval,
    get_eval,
    get_eval_prompts,
    list_evals,
)
from aymara_ai.generated.aymara_api_client.models.content_type import ContentType
from aymara_ai.generated.aymara_api_client.models.error_code import ErrorCode
from aymara_ai.generated.aymara_api_client.models.eval_in_schema import EvalInSchema
from aymara_ai.generated.aymara_api_client.models.eval_out_schema import EvalOutSchema
from aymara_ai.generated.aymara_api_client.models.eval_prompt_schema import EvalPromptSchema
from aymara_ai.generated.aymara_api_client.models.paged_eval_prompt_schema import PagedEvalPromptSchema
from aymara_ai.generated.aymara_api_client.models.prompt_example_in_schema import PromptExampleInSchema
from aymara_ai.generated.aymara_api_client.models.status import Status as ApiStatus
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import GroundTruth, Status
from aymara_ai.utils.async_utils import run_async
from aymara_ai.utils.constants import (
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MAX_WAIT_TIME_SECS,
    DEFAULT_NUM_QUESTIONS,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_TEST_NAME_LEN_MAX,
    DEFAULT_TEST_NAME_LEN_MIN,
    MAX_ADDITIONAL_INSTRUCTIONS_LENGTH,
    MAX_EXAMPLES_LENGTH,
    POLLING_INTERVAL,
    SUPPORTED_LANGUAGES,
)
from aymara_ai.v2_types import EvalResponse, ListEval


class EvalMixin(AymaraAIProtocol):
    use_sandbox = False

    def create_eval(
        self,
        *,
        name: str,
        ai_description: str,
        ai_instructions: Optional[str] = None,
        eval_type: str,
        eval_instructions: Optional[str] = None,
        ground_truth: Optional[GroundTruth] = None,
        modality: ContentType = ContentType.TEXT,
        jailbreak: bool = False,
        language: str = DEFAULT_TEST_LANGUAGE,
        num_prompts: int = DEFAULT_NUM_QUESTIONS,
        prompt_examples: Optional[List[PromptExampleInSchema]] = None,
        max_wait_time_secs: int = DEFAULT_MAX_WAIT_TIME_SECS,
        use_sandbox: Optional[bool] = False,
    ) -> EvalResponse:
        """Create an evaluation synchronously and wait for completion.

        This method creates an evaluation for an AI system and waits for it to complete before returning.
        It handles all the background processes involved in eval creation, validation, and prompt generation.

        Args:
            name: The name of the eval. Must be between 3 and 50 characters.
            eval_type: The type of eval to create. One of the values from TestType (e.g., "safety", "jailbreak")
                or a supported Eval template slug.
            ai_description: A description of the AI system being evaluated.
            ai_instructions: Instructions that the AI system under evaluation are to follow.
            eval_instructions: Additional instructions for the eval.
            ground_truth: The ground truth for the eval.
            modality: The modality of the eval (e.g., text, image).
            jailbreak: Whether the eval is a jailbreak eval.
            language: The language to use for the eval. Defaults to English. Must be one of the supported languages.
            num_prompts: Number of concurrent prompts to generate. Must be between 3 and 100 for most eval types.
            prompt_examples: Examples to be used in the eval.
            max_wait_time_secs: Maximum time to wait for eval completion in seconds.
            use_sandbox: Whether to create the eval in sandbox mode (not counted against quotas).

        Returns:
            EvalResponse: Object containing eval information, status, and generated prompts.

        Raises:
            ValueError: If any validation checks fail (invalid name length, unsupported language, etc.)
            AymaraError: If there's an issue related to using the Aymara API.

        Example:
            ```python
            response = client.create_eval(
                name="Safety Test",
                eval_type="safety",
                ai_description="An AI assistant for customer support",
                ai_instructions="Don't allow any unsafe answers",
                num_prompts=5
            )
            ```
        """

        # Wrap the async implementation with run_async
        return run_async(
            self._create_eval(
                name=name,
                ai_description=ai_description,
                ai_instructions=ai_instructions,
                eval_type=eval_type,
                eval_instructions=eval_instructions,
                jailbreak=jailbreak,
                knowledge_base=None,
                language=language,
                modality=modality,
                num_prompts=num_prompts,
                prompt_examples=prompt_examples,
                max_wait_time_secs=max_wait_time_secs,
                use_sandbox=use_sandbox,
            )
        )

    async def create_eval_async(
        self,
        *,
        name: str,
        ai_description: str,
        ai_instructions: Optional[str] = None,
        eval_type: str,
        eval_instructions: Optional[str] = None,
        ground_truth: Optional[GroundTruth] = None,
        modality: ContentType = ContentType.TEXT,
        jailbreak: bool = False,
        language: str = DEFAULT_TEST_LANGUAGE,
        num_prompts: int = DEFAULT_NUM_QUESTIONS,
        prompt_examples: Optional[List[PromptExampleInSchema]] = None,
        max_wait_time_secs: int = DEFAULT_MAX_WAIT_TIME_SECS,
        use_sandbox: Optional[bool] = False,
    ) -> EvalResponse:
        """Create an evaluation asynchronously and wait for completion.

        See the `create_eval` method for detailed arguments and return values.
        """

        # Directly call the async implementation
        return await self._create_eval(
            name=name,
            ai_description=ai_description,
            ai_instructions=ai_instructions,
            eval_type=eval_type,
            eval_instructions=eval_instructions,
            jailbreak=jailbreak,
            knowledge_base=None,
            language=language,
            modality=modality,
            num_prompts=num_prompts,
            prompt_examples=prompt_examples,
            max_wait_time_secs=max_wait_time_secs,
            use_sandbox=use_sandbox,
        )

    async def _create_eval(
        self,
        *,
        name: str,
        ai_description: str,
        ai_instructions: Optional[str],
        eval_type: str,
        eval_instructions: Optional[str] = None,
        language: str,
        jailbreak: bool = False,
        modality: Union[ContentType, str],
        ground_truth: Optional[GroundTruth] = None,
        knowledge_base: Optional[str],
        max_wait_time_secs: int,
        num_prompts: Optional[int] = None,
        prompt_examples: Optional[List[PromptExampleInSchema]] = None,
        use_sandbox: Optional[bool] = False,
    ) -> EvalResponse:
        """Primary implementation for creating evals (async version)."""

        use_sandbox = use_sandbox or self.use_sandbox

        if isinstance(modality, str):
            modality = ContentType(modality.lower())

        self._validate_eval_inputs(
            eval_name=name,
            ai_description=ai_description,
            ai_instructions=ai_instructions,
            eval_type=eval_type,
            eval_instructions=eval_instructions,
            knowledge_base=knowledge_base,
            language=language,
            num_prompts=num_prompts,
            prompt_examples=prompt_examples,
        )

        eval_data = EvalInSchema(
            name=name,
            ai_description=ai_description,
            ai_instructions=ai_instructions,
            # knowledge_base=knowledge_base,
            language=language,
            num_prompts=num_prompts,
            eval_type=eval_type,
            eval_instructions=eval_instructions,
            prompt_examples=prompt_examples,
            is_jailbreak=jailbreak,
            modality=modality,
            is_sandbox=use_sandbox,
        )

        # Always use the async implementation
        return await self._create_and_wait_for_eval_impl(eval_data, max_wait_time_secs)

    def _validate_eval_inputs(
        self,
        *,
        eval_name: str,
        ai_description: str,
        ai_instructions: Optional[str],
        knowledge_base: Optional[str],
        eval_type: str,
        eval_instructions: Optional[str] = None,
        language: str,
        num_prompts: Optional[int],
        prompt_examples: Optional[List[PromptExampleInSchema]] = None,
    ) -> None:
        """Validate inputs for eval creation."""
        if not ai_description:
            raise ValueError("student_description is required")

        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"language must be one of {SUPPORTED_LANGUAGES}")

        if (eval_type == TestType.SAFETY or eval_type == TestType.IMAGE_SAFETY) and ai_instructions is None:
            raise ValueError("ai_instructions is required for safety evals")

        if len(eval_name) < DEFAULT_TEST_NAME_LEN_MIN or len(eval_name) > DEFAULT_TEST_NAME_LEN_MAX:
            raise ValueError(
                f"name must be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters"
            )
        if num_prompts is not None:
            if eval_type == TestType.JAILBREAK and num_prompts < 1:
                raise ValueError("num_prompts must be at least one prompt")
            elif eval_type != TestType.JAILBREAK and not (
                DEFAULT_NUM_QUESTIONS_MIN <= num_prompts <= DEFAULT_NUM_QUESTIONS_MAX
            ):
                raise ValueError(
                    f"num_prompts must be between {DEFAULT_NUM_QUESTIONS_MIN} "
                    f"and {DEFAULT_NUM_QUESTIONS_MAX} prompts"
                )

        token1 = len(ai_description) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER

        token_2_field = "ai_instructions"

        token2 = len(ai_instructions) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER if ai_instructions is not None else 0

        total_tokens = token1 + token2

        if total_tokens > DEFAULT_MAX_TOKENS:
            raise ValueError(
                f"ai_description is ~{token1:,} tokens and {token_2_field} is ~{token2:,} tokens. "
                f"They are ~{total_tokens:,} tokens in total but they should be less than "
                f"{DEFAULT_MAX_TOKENS:,} tokens."
            )
        if eval_instructions is not None:
            token3 = len(eval_instructions) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            total_tokens = token1 + token2 + token3

            if total_tokens > DEFAULT_MAX_TOKENS:
                raise ValueError(
                    f"ai_description is ~{token1:,} tokens, {token_2_field} is ~{token2:,} tokens, "
                    f"and eval_instructions is ~{token3:,} tokens. They are ~{total_tokens:,} tokens "
                    f"in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
                )

            if len(eval_instructions) > MAX_ADDITIONAL_INSTRUCTIONS_LENGTH:
                raise ValueError(f"eval_instructions must be less than {MAX_ADDITIONAL_INSTRUCTIONS_LENGTH} characters")

        # Validate examples separately to avoid type errors
        max_examples = MAX_EXAMPLES_LENGTH * 2
        if prompt_examples is not None:
            if len(prompt_examples) > max_examples:
                raise ValueError(f"prompt_examples must have fewer than {max_examples} examples")

    async def _create_and_wait_for_eval_impl(
        self,
        eval_payload: EvalInSchema,
        max_wait_time_secs: int,
    ) -> EvalResponse:
        """Primary implementation of eval creation and waiting logic (async version)."""
        start_time = time.time()

        # Create the eval
        response = await create_eval.asyncio_detailed(client=self.client, body=eval_payload)
        create_response: EvalOutSchema = get_parsed_response(response)

        eval_uuid = create_response.eval_uuid
        eval_name = create_response.name

        with self.logger.progress_bar(
            eval_name,
            eval_uuid,
            Status.from_api_status(create_response.status),
        ):
            while True:
                # Get eval status
                response = await get_eval.asyncio_detailed(client=self.client, eval_uuid=eval_uuid)
                eval_response: EvalOutSchema = get_parsed_response(response)

                self.logger.update_progress_bar(
                    eval_uuid,
                    Status.from_api_status(eval_response.status),
                )

                elapsed_time = time.time() - start_time
                eval = EvalResponse(eval=eval_response)
                if elapsed_time > max_wait_time_secs:
                    eval_response.status = ApiStatus.FAILED
                    self.logger.update_progress_bar(eval_uuid, Status.FAILED)
                    raise AymaraError(ErrorCode.SERVER_INTERNAL_ERROR, "Eval creation timed out")

                if eval_response.status == ApiStatus.FAILED:
                    failure_reason = "Internal server error, please try again."
                    raise AymaraError(ErrorCode.SERVER_INTERNAL_ERROR, failure_reason)

                if eval_response.status == ApiStatus.FINISHED:
                    if eval_payload.eval_type != TestType.MULTITURN_SAFETY:
                        prompts = await self._get_all_prompts_async(eval_uuid)

                        eval.prompts = prompts
                    return eval

                # Sleep before next poll
                await asyncio.sleep(POLLING_INTERVAL)

    async def _get_all_prompts_async(self, eval_uuid: str) -> List[EvalPromptSchema]:
        prompts = []
        offset = 0
        while True:
            response = await get_eval_prompts.asyncio_detailed(client=self.client, eval_uuid=eval_uuid, offset=offset)

            paged_response: PagedEvalPromptSchema = get_parsed_response(response)
            prompts.extend(paged_response.items)
            if len(prompts) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return prompts

    # List Evals Methods
    def list_evals(self) -> List[EvalOutSchema]:
        """
        List all evals synchronously.
        """
        evals = run_async(self._list_evals_async_impl())

        return evals

    async def list_evals_async(self) -> List[EvalOutSchema]:
        """
        List all evals asynchronously.
        """
        evals = await self._list_evals_async_impl()

        return evals

    async def _list_evals_async_impl(self) -> List[EvalOutSchema]:
        all_evals = []
        offset = 0
        while True:
            response = await list_evals.asyncio_detailed(client=self.client, offset=offset)

            paged_response = get_parsed_response(response)
            all_evals.extend(paged_response.items)
            if len(all_evals) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return ListEval(root=[EvalResponse(eval=e) for e in all_evals])

    def delete_eval(self, eval_uuid: str) -> None:
        """
        Delete a eval synchronously.
        """
        response = delete_eval.sync_detailed(client=self.client, eval_uuid=eval_uuid)
        parsed_response = get_parsed_response(response)

    async def delete_eval_async(self, eval_uuid: str) -> None:
        """
        Delete a eval asynchronously.
        """
        response = await delete_eval.asyncio_detailed(client=self.client, eval_uuid=eval_uuid)
        parsed_response = get_parsed_response(response)

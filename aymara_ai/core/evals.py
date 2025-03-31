import asyncio
import time
from typing import List, Optional

from aymara_ai.core.errors import get_parsed_response
from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import create_test, get_test, get_test_questions
from aymara_ai.generated.aymara_api_client.models.paged_question_schema import PagedQuestionSchema
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import BaseTestResponse, PromptExample, Status
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
        language: str = DEFAULT_TEST_LANGUAGE,
        num_prompts: int = DEFAULT_NUM_QUESTIONS,
        prompt_examples: Optional[List[PromptExample]] = None,
        max_wait_time_secs: int = DEFAULT_MAX_WAIT_TIME_SECS,
        use_sandbox: Optional[bool] = False,
    ) -> BaseTestResponse:
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
            language: The language to use for the test. Defaults to English. Must be one of the supported languages.
            num_prompts: Number of concurrent prompts to generate. Must be between 3 and 100 for most test types.
            prompt_examples: Examples to be used in the eval.
            max_wait_time_secs: Maximum time to wait for eval completion in seconds.
            use_sandbox: Whether to create the eval in sandbox mode (not counted against quotas).

        Returns:
            BaseTestResponse: Object containing eval information, status, and generated questions.

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
                knowledge_base=None,
                language=language,
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
        language: str = DEFAULT_TEST_LANGUAGE,
        num_prompts: int = DEFAULT_NUM_QUESTIONS,
        prompt_examples: Optional[List[PromptExample]] = None,
        max_wait_time_secs: int = DEFAULT_MAX_WAIT_TIME_SECS,
        use_sandbox: Optional[bool] = False,
    ) -> BaseTestResponse:
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
            knowledge_base=None,
            language=language,
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
        knowledge_base: Optional[str],
        max_wait_time_secs: int,
        num_prompts: Optional[int] = None,
        prompt_examples: Optional[List[PromptExample]] = None,
        use_sandbox: Optional[bool] = False,
    ) -> BaseTestResponse:
        """Primary implementation for creating tests (async version)."""

        use_sandbox = use_sandbox or self.use_sandbox

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

        examples = []
        if prompt_examples:
            examples.extend([ex.to_example_in_schema() for ex in prompt_examples])

        test_data = models.TestInSchema(
            test_name=name,
            student_description=ai_description,
            test_policy=ai_instructions,
            test_system_prompt=None,
            knowledge_base=knowledge_base,
            test_language=language,
            num_test_questions=num_prompts,
            test_type=eval_type,
            additional_instructions=eval_instructions,
            test_examples=examples,
        )

        # Always use the async implementation
        return await self._create_and_wait_for_eval_impl(test_data, max_wait_time_secs, use_sandbox)

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
        prompt_examples: Optional[List[PromptExample]] = None,
    ) -> None:
        """Validate inputs for test creation."""
        if not ai_description:
            raise ValueError("student_description is required")

        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"language must be one of {SUPPORTED_LANGUAGES}")

        if (eval_type == TestType.SAFETY or eval_type == TestType.IMAGE_SAFETY) and ai_instructions is None:
            raise ValueError("ai_instructions is required for safety tests")

        if len(eval_name) < DEFAULT_TEST_NAME_LEN_MIN or len(eval_name) > DEFAULT_TEST_NAME_LEN_MAX:
            raise ValueError(
                f"name must be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters"
            )
        if num_prompts is not None:
            if eval_type == TestType.JAILBREAK and num_prompts < 1:
                raise ValueError("num_prompts must be at least one question")
            elif eval_type != TestType.JAILBREAK and not (
                DEFAULT_NUM_QUESTIONS_MIN <= num_prompts <= DEFAULT_NUM_QUESTIONS_MAX
            ):
                raise ValueError(
                    f"num_prompts must be between {DEFAULT_NUM_QUESTIONS_MIN} "
                    f"and {DEFAULT_NUM_QUESTIONS_MAX} questions"
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
        eval_config: models.TestInSchema,
        max_wait_time_secs: int,
        is_sandbox: Optional[bool] = None,
    ) -> BaseTestResponse:
        """Primary implementation of test creation and waiting logic (async version)."""
        start_time = time.time()

        # Create the test
        response = await create_test.asyncio_detailed(client=self.client, body=eval_config, is_sandbox=is_sandbox)
        create_response: models.TestOutSchema = get_parsed_response(response)

        test_uuid = create_response.test_uuid
        test_name = create_response.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            Status.from_api_status(create_response.test_status),
        ):
            while True:
                # Get test status
                response = await get_test.asyncio_detailed(client=self.client, test_uuid=test_uuid)
                test_response: models.TestOutSchema = get_parsed_response(response)

                self.logger.update_progress_bar(
                    test_uuid,
                    Status.from_api_status(test_response.test_status),
                )

                elapsed_time = time.time() - start_time

                if elapsed_time > max_wait_time_secs:
                    test_response.test_status = models.TestStatus.FAILED
                    self.logger.update_progress_bar(test_uuid, Status.FAILED)
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test=test_response, questions=None, failure_reason="Test creation timed out"
                    )

                if test_response.test_status == models.TestStatus.FAILED:
                    failure_reason = "Internal server error, please try again."
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test=test_response, questions=None, failure_reason=failure_reason
                    )

                if test_response.test_status == models.TestStatus.FINISHED:
                    if eval_config.test_type != TestType.MULTITURN_SAFETY:
                        questions = await self._get_all_prompts_async(test_uuid)

                    return BaseTestResponse.from_test_out_schema_and_questions(test=test_response, questions=questions)

                # Sleep before next poll
                await asyncio.sleep(POLLING_INTERVAL)

    async def _get_all_prompts_async(self, test_uuid: str) -> List[models.QuestionSchema]:
        questions = []
        offset = 0
        while True:
            response = await get_test_questions.asyncio_detailed(client=self.client, test_uuid=test_uuid, offset=offset)

            paged_response: PagedQuestionSchema = get_parsed_response(response)
            questions.extend(paged_response.items)
            if len(questions) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return questions

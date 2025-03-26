import asyncio
import time
from typing import List, Optional

from aymara_ai.core.errors import get_parsed_response
from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import create_test, get_test, get_test_questions
from aymara_ai.generated.aymara_api_client.models.paged_question_schema import PagedQuestionSchema
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import BadExample, BaseTestResponse, GoodExample, InstructionOptions, Status
from aymara_ai.utils.async_utils import run_async
from aymara_ai.utils.constants import (
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_MAX_TOKENS,
    DEFAULT_NUM_CONVERSATIONS_MAX,
    DEFAULT_NUM_CONVERSATIONS_MIN,
    DEFAULT_NUM_QUESTIONS,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_TEST_NAME_LEN_MAX,
    DEFAULT_TEST_NAME_LEN_MIN,
    MAX_ADDITIONAL_INSTRUCTIONS_LENGTH,
    MAX_EXAMPLES_LENGTH,
    POLLING_INTERVAL,
    SUPPORTED_LANGUAGES,
)


class EvalMixin(AymaraAIProtocol):
    def create_eval(
        self,
        *,
        name: str,
        template: str,
        ai_under_test: str,
        instructOptions: Optional[InstructionOptions] = None,
        language: str = DEFAULT_TEST_LANGUAGE,
        batch_size: int = DEFAULT_NUM_QUESTIONS,
        max_wait_time_secs: int = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
        is_sandbox: Optional[bool] = False,
    ) -> BaseTestResponse:
        """Create a test synchronously and wait for completion."""
        # Wrap the async implementation with run_async
        return run_async(
            self._create_eval(
                test_name=name,
                student_description=ai_under_test,
                test_policy=instructOptions.policy if instructOptions else None,
                test_system_prompt=None,
                knowledge_base=None,
                test_language=language,
                num_test_questions=batch_size,
                test_type=template,
                max_wait_time_secs=max_wait_time_secs,
                additional_instructions=instructOptions.additional_instructions if instructOptions else None,
                good_examples=instructOptions.good_examples if instructOptions else None,
                bad_examples=instructOptions.bad_examples if instructOptions else None,
                is_sandbox=is_sandbox,
            )
        )

    async def create_eval_async(
        self,
        *,
        name: str,
        template: str,
        ai_under_test: str,
        instructOptions: Optional[InstructionOptions] = None,
        language: str = DEFAULT_TEST_LANGUAGE,
        batch_size: int = DEFAULT_NUM_QUESTIONS,
        max_wait_time_secs: int = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
        is_sandbox: Optional[bool] = False,
    ) -> BaseTestResponse:
        """Create a test asynchronously and wait for completion."""
        # Directly call the async implementation
        return await self._create_eval(
            test_name=name,
            student_description=ai_under_test,
            test_policy=instructOptions.policy if instructOptions else None,
            test_system_prompt=None,
            knowledge_base=None,
            test_language=language,
            num_test_questions=batch_size,
            test_type=template,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=instructOptions.additional_instructions if instructOptions else None,
            good_examples=instructOptions.good_examples if instructOptions else None,
            bad_examples=instructOptions.bad_examples if instructOptions else None,
            is_sandbox=is_sandbox,
        )

    async def _create_eval(
        self,
        test_name: str,
        student_description: str,
        test_type: str,
        test_language: str,
        test_system_prompt: Optional[str],
        test_policy: Optional[str],
        knowledge_base: Optional[str],
        max_wait_time_secs: int,
        num_test_questions: Optional[int] = None,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        is_sandbox: Optional[bool] = False,
        num_conversations: Optional[int] = None,
    ) -> BaseTestResponse:
        """Primary implementation for creating tests (async version)."""
        self._validate_test_inputs(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            test_language=test_language,
            num_test_questions=num_test_questions,
            test_type=test_type,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
            num_conversations=num_conversations,
        )

        examples = []
        if good_examples:
            examples.extend([ex.to_example_in_schema() for ex in good_examples])
        if bad_examples:
            examples.extend([ex.to_example_in_schema() for ex in bad_examples])

        test_data = models.TestInSchema(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            test_language=test_language,
            num_test_questions=num_test_questions,
            test_type=test_type,
            additional_instructions=additional_instructions,
            test_examples=examples if examples else None,
            num_conversations=num_conversations,
        )

        # Always use the async implementation
        return await self._create_and_wait_for_test_impl(test_data, max_wait_time_secs, is_sandbox)

    def _validate_test_inputs(
        self,
        test_name: str,
        student_description: str,
        test_policy: Optional[str],
        test_system_prompt: Optional[str],
        knowledge_base: Optional[str],
        test_language: str,
        num_test_questions: Optional[int],
        test_type: str,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        num_conversations: Optional[int] = None,
    ) -> None:
        """Validate inputs for test creation."""
        if not student_description:
            raise ValueError("student_description is required")

        if test_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"test_language must be one of {SUPPORTED_LANGUAGES}")

        if (test_type == TestType.SAFETY or test_type == TestType.IMAGE_SAFETY) and test_policy is None:
            raise ValueError("test_policy is required for safety tests")

        if test_type == TestType.JAILBREAK and test_system_prompt is None:
            raise ValueError("test_system_prompt is required for jailbreak tests")

        if test_type == TestType.ACCURACY and knowledge_base is None:
            raise ValueError("knowledge_base is required for accuracy tests")

        if len(test_name) < DEFAULT_TEST_NAME_LEN_MIN or len(test_name) > DEFAULT_TEST_NAME_LEN_MAX:
            raise ValueError(
                f"test_name must be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters"
            )
        if num_test_questions is not None:
            if test_type == TestType.JAILBREAK and num_test_questions < 1:
                raise ValueError("limit_num_questions must be at least one question")
            elif test_type != TestType.JAILBREAK and not (
                DEFAULT_NUM_QUESTIONS_MIN <= num_test_questions <= DEFAULT_NUM_QUESTIONS_MAX
            ):
                raise ValueError(
                    f"num_test_questions must be between {DEFAULT_NUM_QUESTIONS_MIN} "
                    f"and {DEFAULT_NUM_QUESTIONS_MAX} questions"
                )
        if num_conversations is not None:
            if test_type != TestType.MULTITURN_SAFETY:
                raise ValueError("num_conversations is only valid for multiturn safety tests")
            elif not (DEFAULT_NUM_CONVERSATIONS_MIN <= num_conversations <= DEFAULT_NUM_CONVERSATIONS_MAX):
                raise ValueError(
                    f"num_conversations must be between {DEFAULT_NUM_CONVERSATIONS_MIN} "
                    f"and {DEFAULT_NUM_CONVERSATIONS_MAX} conversations"
                )
        token1 = len(student_description) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER

        token_2_field = (
            "test_policy"
            if test_type == TestType.SAFETY
            or test_type == TestType.IMAGE_SAFETY
            or test_type == TestType.MULTITURN_SAFETY
            else "test_system_prompt"
            if test_type == TestType.JAILBREAK
            else "knowledge_base"
        )

        token2 = (
            len(test_policy) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            if test_policy is not None
            else len(test_system_prompt) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            if test_system_prompt is not None
            else len(knowledge_base) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            if knowledge_base is not None
            else 0
        )

        total_tokens = token1 + token2

        if total_tokens > DEFAULT_MAX_TOKENS:
            raise ValueError(
                f"student_description is ~{token1:,} tokens and {token_2_field} is ~{token2:,} tokens. "
                f"They are ~{total_tokens:,} tokens in total but they should be less than "
                f"{DEFAULT_MAX_TOKENS:,} tokens."
            )
        if additional_instructions is not None:
            token3 = len(additional_instructions) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            total_tokens = token1 + token2 + token3

            if total_tokens > DEFAULT_MAX_TOKENS:
                raise ValueError(
                    f"student_description is ~{token1:,} tokens, {token_2_field} is ~{token2:,} tokens, "
                    f"and additional_instructions is ~{token3:,} tokens. They are ~{total_tokens:,} tokens "
                    f"in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
                )

            if len(additional_instructions) > MAX_ADDITIONAL_INSTRUCTIONS_LENGTH:
                raise ValueError(
                    f"additional_instructions must be less than {MAX_ADDITIONAL_INSTRUCTIONS_LENGTH} characters"
                )

        # Validate examples separately to avoid type errors
        if good_examples is not None:
            for example in good_examples:
                if not isinstance(example, GoodExample):
                    raise ValueError("good_examples must contain instances of GoodExample")
            if len(good_examples) > MAX_EXAMPLES_LENGTH:
                raise ValueError(f"good_examples must have fewer than {MAX_EXAMPLES_LENGTH} examples")

        if bad_examples is not None:
            for example in bad_examples:
                if not isinstance(example, BadExample):
                    raise ValueError("bad_examples must contain instances of BadExample")
            if len(bad_examples) > MAX_EXAMPLES_LENGTH:
                raise ValueError(f"bad_examples must have fewer than {MAX_EXAMPLES_LENGTH} examples")

        # Add knowledge_base to token calculation if it exists
        if knowledge_base is not None:
            token3 = len(knowledge_base) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            total_tokens = token1 + token2 + token3

            if total_tokens > DEFAULT_MAX_TOKENS:
                raise ValueError(
                    f"student_description is ~{token1:,} tokens, {token_2_field} is ~{token2:,} tokens, "
                    f"and knowledge_base is ~{token3:,} tokens. They are ~{total_tokens:,} tokens "
                    f"in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
                )

    async def _create_and_wait_for_test_impl(
        self,
        test_data: models.TestInSchema,
        max_wait_time_secs: int,
        is_sandbox: Optional[bool] = None,
    ) -> BaseTestResponse:
        """Primary implementation of test creation and waiting logic (async version)."""
        start_time = time.time()

        # Create the test
        response = await create_test.asyncio_detailed(client=self.client, body=test_data, is_sandbox=is_sandbox)
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
                        test_response, None, None, "Test creation timed out"
                    )

                if test_response.test_status == models.TestStatus.FAILED:
                    failure_reason = "Internal server error, please try again."
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, None, failure_reason
                    )

                if test_response.test_status == models.TestStatus.FINISHED:
                    if test_data.test_type == TestType.MULTITURN_SAFETY:
                        conversations = create_response.conversations
                        return BaseTestResponse.from_test_out_schema_and_questions(test_response, None, conversations)
                    else:
                        questions = await self._get_all_prompts_async(test_uuid)
                        return BaseTestResponse.from_test_out_schema_and_questions(test_response, questions, None)

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

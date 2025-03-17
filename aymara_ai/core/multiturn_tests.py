import asyncio
import time
from typing import Optional, Union, Coroutine, List

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import (
    create_multiturn_test,
    continue_multiturn,
    get_test,
    get_test_questions,
)
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import (
    BaseTestResponse,
    GoodExample,
    BadExample,
    Status,
)
from aymara_ai.utils.constants import (
    DEFAULT_NUM_CONVERSATIONS_MAX,
    DEFAULT_NUM_CONVERSATIONS_MIN,
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_TEST_NAME_LEN_MIN,
    DEFAULT_TEST_NAME_LEN_MAX,
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_MAX_TOKENS,
    MAX_ADDITIONAL_INSTRUCTIONS_LENGTH,
    MAX_EXAMPLES_LENGTH,
    POLLING_INTERVAL,
    SUPPORTED_LANGUAGES,
)


class MultiturnTestMixin(AymaraAIProtocol):
    def create_multiturn_test(
        self,
        test_name: str,
        student_description: str,
        test_type: TestType = TestType.MULTITURN_SAFETY,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        test_policy: Optional[str] = None,
        num_test_questions: Optional[int] = None,
        num_conversations: Optional[int] = None,
        test_system_prompt: Optional[str] = None,
        knowledge_base: Optional[str] = None,
        additional_instructions: Optional[str] = None,
        test_examples: Optional[List[Union[GoodExample, BadExample]]] = None,
        max_turns: int = 10,
        max_wait_time_secs: Optional[int] = None,
    ):
        """
        Create a multiturn test synchronously and wait for completion.

        :param test_name: Name of the test
        :param student_description: Description of the AI that will take the test
        :param test_type: Type of test, defaults to SAFETY
        :param test_language: Language of the test, defaults to 'en'
        :param test_policy: Policy for safety tests
        :param num_test_questions: Number of test questions
        :param num_conversations: Number of conversations
        :param test_system_prompt: System prompt for the test
        :param knowledge_base: Knowledge base for the test
        :param additional_instructions: Additional test instructions
        :param test_examples: List of example tests
        :param max_turns: Maximum number of turns per conversation, defaults to 10
        :param max_wait_time_secs: Maximum wait time for test creation
        """

        return self._create_multiturn_test(
            test_name=test_name,
            student_description=student_description,
            test_type=test_type,
            test_language=test_language,
            test_policy=test_policy,
            num_test_questions=num_test_questions,
            num_conversations=num_conversations,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            additional_instructions=additional_instructions,
            test_examples=test_examples,
            max_turns=max_turns,
            is_async=False,
            max_wait_time_secs=max_wait_time_secs,
        )

    async def create_multiturn_test_async(
        self,
        test_name: str,
        student_description: str,
        test_type: TestType = TestType.SAFETY,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        test_policy: Optional[str] = None,
        num_test_questions: Optional[int] = None,
        num_conversations: Optional[int] = None,
        test_system_prompt: Optional[str] = None,
        knowledge_base: Optional[str] = None,
        additional_instructions: Optional[str] = None,
        test_examples: Optional[List[Union[GoodExample, BadExample]]] = None,
        max_turns: int = 10,
        max_wait_time_secs: Optional[int] = None,
    ):
        """
        Create a multiturn test asynchronously and wait for completion.
        Parameters are the same as create_multiturn_test.
        """
        return await self._create_multiturn_test(
            test_name=test_name,
            student_description=student_description,
            test_type=test_type,
            test_language=test_language,
            test_policy=test_policy,
            num_test_questions=num_test_questions,
            num_conversations=num_conversations,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            additional_instructions=additional_instructions,
            test_examples=test_examples,
            max_turns=max_turns,
            is_async=True,
            max_wait_time_secs=max_wait_time_secs,
        )

    def _create_multiturn_test(
        self,
        test_name: str,
        student_description: str,
        test_type: TestType,
        test_language: str,
        test_policy: Optional[str],
        num_test_questions: Optional[int],
        num_conversations: Optional[int],
        test_system_prompt: Optional[str],
        knowledge_base: Optional[str],
        additional_instructions: Optional[str],
        test_examples: Optional[List[Union[GoodExample, BadExample]]],
        max_turns: int,
        is_async: bool,
        max_wait_time_secs: Optional[int] = None,
    ):
        self._validate_multiturn_test_inputs(
            test_name=test_name,
            student_description=student_description,
            test_type=test_type,
            test_language=test_language,
            test_policy=test_policy,
            num_test_questions=num_test_questions,
            num_conversations=num_conversations,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            additional_instructions=additional_instructions,
            test_examples=test_examples,
            max_turns=max_turns,
        )

        examples = []
        if test_examples:
            examples.extend([ex.to_example_in_schema() for ex in test_examples])

        test_data = models.MultiturnTestInSchema(
            test_name=test_name,
            student_description=student_description,
            test_type=test_type,
            test_language=test_language,
            test_policy=test_policy,
            num_test_questions=num_test_questions,
            num_conversations=num_conversations,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            additional_instructions=additional_instructions,
            test_examples=examples if examples else None,
            max_turns=max_turns,
        )

        if is_async:
            return self._create_and_wait_for_multiturn_test_impl_async(
                test_data, max_wait_time_secs
            )
        else:
            return self._create_and_wait_for_multiturn_test_impl_sync(
                test_data, max_wait_time_secs
            )

    def _validate_multiturn_test_inputs(
        self,
        test_name: str,
        student_description: str,
        test_type: TestType,
        test_language: str,
        test_policy: Optional[str],
        num_test_questions: Optional[int],
        num_conversations: Optional[int],
        test_system_prompt: Optional[str],
        knowledge_base: Optional[str],
        additional_instructions: Optional[str],
        test_examples: Optional[List[Union[GoodExample, BadExample]]],
        max_turns: int,
    ) -> None:
        if not student_description:
            raise ValueError("student_description is required")

        if test_type == TestType.SAFETY and not test_policy:
            raise ValueError("test_policy is required for safety tests")

        if test_type == TestType.JAILBREAK and not test_system_prompt:
            raise ValueError("test_system_prompt is required for jailbreak tests")

        if test_type == TestType.ACCURACY and not knowledge_base:
            raise ValueError("knowledge_base is required for accuracy tests")

        if test_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"test_language must be one of {SUPPORTED_LANGUAGES}")

        if (
            len(test_name) < DEFAULT_TEST_NAME_LEN_MIN
            or len(test_name) > DEFAULT_TEST_NAME_LEN_MAX
        ):
            raise ValueError(
                f"test_name must be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters"
            )

        if num_conversations is not None and not (
            DEFAULT_NUM_CONVERSATIONS_MIN
            <= num_conversations
            <= DEFAULT_NUM_CONVERSATIONS_MAX
        ):
            raise ValueError(
                f"num_conversations must be between {DEFAULT_NUM_CONVERSATIONS_MIN} and {DEFAULT_NUM_CONVERSATIONS_MAX}"
            )

        if max_turns < 1:
            raise ValueError("max_turns must be at least 1")

        # Token validation
        total_tokens = len(student_description) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER

        if test_policy:
            total_tokens += len(test_policy) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
        if test_system_prompt:
            total_tokens += len(test_system_prompt) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
        if knowledge_base:
            total_tokens += len(knowledge_base) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
        if additional_instructions:
            if len(additional_instructions) > MAX_ADDITIONAL_INSTRUCTIONS_LENGTH:
                raise ValueError(
                    f"additional_instructions must be less than {MAX_ADDITIONAL_INSTRUCTIONS_LENGTH} characters"
                )
            total_tokens += (
                len(additional_instructions) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            )

        if total_tokens > DEFAULT_MAX_TOKENS:
            raise ValueError(
                f"Total tokens ({total_tokens:,}) exceeds maximum allowed ({DEFAULT_MAX_TOKENS:,})"
            )

        if test_examples and len(test_examples) > MAX_EXAMPLES_LENGTH:
            raise ValueError(
                f"Total number of examples must be less than {MAX_EXAMPLES_LENGTH}"
            )

    def _create_and_wait_for_multiturn_test_impl_sync(
        self,
        test_data: models.MultiturnTestInSchema,
        max_wait_time_secs: Optional[int],
    ):
        start_time = time.time()
        response = create_multiturn_test.sync_detailed(
            client=self.client, body=test_data
        )
        create_response = response.parsed
        print(f"create_response: {create_response}")

        if response.status_code == 422:
            raise ValueError(f"{create_response.detail}")

        # Extract test_uuid and test_name from the first message
        test_uuid = create_response.test_uuid
        test_name = create_response.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            Status.from_api_status(create_response.test_status),
        ):
            while True:
                response = get_test.sync_detailed(
                    client=self.client, test_uuid=test_uuid
                )

                if response.status_code == 404:
                    raise ValueError(f"Test with UUID {test_uuid} not found")

                test_response = response.parsed

                self.logger.update_progress_bar(
                    test_uuid,
                    Status.from_api_status(test_response.test_status),
                )

                if max_wait_time_secs and time.time() - start_time > max_wait_time_secs:
                    test_response.test_status = models.TestStatus.FAILED
                    self.logger.update_progress_bar(test_uuid, Status.FAILED)
                    return test_response

                if test_response.test_status == models.TestStatus.FAILED:
                    return test_response

                if test_response.test_status == models.TestStatus.FINISHED:
                    return test_response

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_multiturn_test_impl_async(
        self,
        test_data: models.MultiturnTestInSchema,
        max_wait_time_secs: Optional[int],
    ) -> BaseTestResponse:
        start_time = time.time()
        response = await create_multiturn_test.asyncio_detailed(
            client=self.client, body=test_data
        )

        create_response = response.parsed

        if response.status_code == 422:
            raise ValueError(f"{create_response.detail}")

        # Extract test_uuid and test_name from the first message
        if not create_response.messages:
            raise ValueError("No messages received in response")

        first_message = create_response.messages[0]
        test_uuid = first_message.test_uuid
        test_name = first_message.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            Status.PENDING,  # Initial status since we don't get it in response
        ):
            while True:
                response = await get_test.asyncio_detailed(
                    client=self.client, test_uuid=test_uuid
                )

                if response.status_code == 404:
                    raise ValueError(f"Test with UUID {test_uuid} not found")

                test_response = response.parsed

                self.logger.update_progress_bar(
                    test_uuid,
                    Status.from_api_status(test_response.test_status),
                )

                if max_wait_time_secs and time.time() - start_time > max_wait_time_secs:
                    test_response.test_status = models.TestStatus.FAILED
                    self.logger.update_progress_bar(test_uuid, Status.FAILED)
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Test creation timed out"
                    )

                if test_response.test_status == models.TestStatus.FAILED:
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Internal server error, please try again."
                    )

                if test_response.test_status == models.TestStatus.FINISHED:
                    messages = await self._get_all_messages_async(test_uuid)
                    return BaseTestResponse.from_test_out_schema_and_messages(
                        test_response, messages, None
                    )

                await asyncio.sleep(POLLING_INTERVAL)

    def _get_all_messages_sync(self, test_uuid: str) -> List[dict]:
        messages = []
        offset = 0
        while True:
            response = get_test_questions.sync_detailed(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            if response.status_code == 404:
                raise ValueError(f"Test with UUID {test_uuid} not found")

            paged_response = response.parsed
            messages.extend(
                paged_response.messages
            )  # Assuming messages is a list of dicts
            if len(messages) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return messages

    async def _get_all_messages_async(self, test_uuid: str) -> List[dict]:
        messages = []
        offset = 0
        while True:
            response = await get_test_questions.asyncio_detailed(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            if response.status_code == 404:
                raise ValueError(f"Test with UUID {test_uuid} not found")

            paged_response = response.parsed
            messages.extend(
                paged_response.messages
            )  # Assuming messages is a list of dicts
            if len(messages) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return messages

    def continue_multiturn(
        self,
        continue_requests: List[models.MultiturnContinueInSchema],
    ):
        """
        Continue multiple multiturn conversations by providing user responses.

        :param continue_requests: List of continuation requests, each containing test_uuid, conversation_uuid, and message_text
        :type continue_requests: List[MultiturnContinueInSchema]
        :return: Response containing the next steps in the conversations
        :rtype: MultiturnOutSchema
        """
        print(f"continue_requests: {continue_requests}")
        response = continue_multiturn.sync_detailed(
            client=self.client,
            body=continue_requests,
        )

        if response.status_code == 404:
            raise ValueError("Test or question not found")

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        return response.parsed

    async def continue_multiturn_async(
        self,
        continue_requests: List[models.MultiturnContinueInSchema],
    ):
        """
        Continue multiple multiturn conversations asynchronously by providing user responses.

        :param continue_requests: List of continuation requests, each containing test_uuid, conversation_uuid, and message_text
        :type continue_requests: List[MultiturnContinueInSchema]
        :return: Response containing the next steps in the conversations
        :rtype: MultiturnOutSchema
        """
        response = await continue_multiturn.asyncio_detailed(
            client=self.client,
            body=continue_requests,
        )

        if response.status_code == 404:
            raise ValueError("Test or question not found")

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        return response.parsed

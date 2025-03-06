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
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_NUM_QUESTIONS,
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
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions: int = DEFAULT_NUM_QUESTIONS,
        max_wait_time_secs: Optional[int] = None,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
    ) -> BaseTestResponse:
        print(f"Creating multiturn test with {num_test_questions} questions")
        """
        Create a multiturn test synchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test.
        :type student_description: str
        :param test_policy: Policy of the test, which will measure compliance.
        :type test_policy: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}.
        :type num_test_questions: int, optional
        :param max_wait_time_secs: Maximum wait time for test creation.
        :type max_wait_time_secs: int, optional
        :param additional_instructions: Optional additional instructions for test generation.
        :type additional_instructions: str, optional
        :param good_examples: Optional list of good examples to guide question generation.
        :type good_examples: List[GoodExample], optional
        :param bad_examples: Optional list of bad examples to guide question generation.
        :type bad_examples: List[BadExample], optional
        :return: Test response containing test details and generated questions.
        :rtype: BaseTestResponse
        """
        return self._create_multiturn_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_language=test_language,
            num_test_questions=num_test_questions,
            is_async=False,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
        )

    async def create_multiturn_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions: int = DEFAULT_NUM_QUESTIONS,
        max_wait_time_secs: Optional[int] = None,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
    ) -> BaseTestResponse:
        """
        Create a multiturn test asynchronously and wait for completion.

        Parameters are the same as create_multiturn_test.
        """
        return await self._create_multiturn_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_language=test_language,
            num_test_questions=num_test_questions,
            is_async=True,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
        )

    def _create_multiturn_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str,
        num_test_questions: int,
        is_async: bool,
        max_wait_time_secs: Optional[int] = None,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
    ) -> Union[BaseTestResponse, Coroutine[BaseTestResponse, None, None]]:
        print(
            f"I am inside create multiturn test, {test_name}, {student_description}, {test_policy}, {test_language}, {num_test_questions}, {additional_instructions}, {good_examples}, {bad_examples}"
        )
        self._validate_multiturn_test_inputs(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_language=test_language,
            num_test_questions=num_test_questions,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
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
            test_language=test_language,
            num_test_questions=num_test_questions,
            test_type=TestType.SAFETY,
            additional_instructions=additional_instructions,
            test_examples=examples if examples else None,
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
        test_policy: str,
        test_language: str,
        num_test_questions: int,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
    ) -> None:
        if not student_description:
            raise ValueError("student_description is required")

        if not test_policy:
            raise ValueError("test_policy is required for multiturn tests")

        if test_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"test_language must be one of {SUPPORTED_LANGUAGES}")

        if (
            len(test_name) < DEFAULT_TEST_NAME_LEN_MIN
            or len(test_name) > DEFAULT_TEST_NAME_LEN_MAX
        ):
            raise ValueError(
                f"test_name must be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters"
            )

        if not (
            DEFAULT_NUM_QUESTIONS_MIN <= num_test_questions <= DEFAULT_NUM_QUESTIONS_MAX
        ):
            raise ValueError(
                f"num_test_questions must be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions"
            )

        token1 = len(student_description) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
        token2 = len(test_policy) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
        total_tokens = token1 + token2

        if total_tokens > DEFAULT_MAX_TOKENS:
            raise ValueError(
                f"student_description is ~{token1:,} tokens and test_policy is ~{token2:,} tokens. "
                f"They are ~{total_tokens:,} tokens in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
            )

        if additional_instructions is not None:
            if len(additional_instructions) > MAX_ADDITIONAL_INSTRUCTIONS_LENGTH:
                raise ValueError(
                    f"additional_instructions must be less than {MAX_ADDITIONAL_INSTRUCTIONS_LENGTH} characters"
                )

            token3 = len(additional_instructions) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            total_tokens = token1 + token2 + token3

            if total_tokens > DEFAULT_MAX_TOKENS:
                raise ValueError(
                    f"Total tokens ({total_tokens:,}) exceeds maximum allowed ({DEFAULT_MAX_TOKENS:,})"
                )

        if good_examples is not None or bad_examples is not None:
            for example in good_examples or []:
                if not isinstance(example, GoodExample):
                    raise ValueError("good_examples must be instances of GoodExample")

            for example in bad_examples or []:
                if not isinstance(example, BadExample):
                    raise ValueError("bad_examples must be instances of BadExample")

            if len((good_examples or []) + (bad_examples or [])) > MAX_EXAMPLES_LENGTH:
                raise ValueError(
                    f"Total number of examples must be less than {MAX_EXAMPLES_LENGTH}"
                )

    def _create_and_wait_for_multiturn_test_impl_sync(
        self,
        test_data: models.TestInSchema,
        max_wait_time_secs: Optional[int],
    ) -> BaseTestResponse:
        start_time = time.time()
        response = create_multiturn_test.sync_detailed(
            client=self.client, body=test_data
        )
        print(f"response: {response}")
        create_response = response.content
        print(f"create_response: {create_response}")

        if response.status_code == 422:
            raise ValueError(f"{create_response.detail}")

        # Extract test_uuid and test_name from the first message
        if not create_response.messages:
            raise ValueError("No messages received in response")

        first_message = create_response.messages[0]
        test_uuid = first_message.test_uuid
        test_name = first_message.test_name

        print(f"test_uuid: {test_uuid}")
        print(f"test_name: {test_name}")

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            Status.PENDING,  # Initial status since we don't get it in response
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
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Test creation timed out"
                    )

                if test_response.test_status == models.TestStatus.FAILED:
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Internal server error, please try again."
                    )

                if test_response.test_status == models.TestStatus.FINISHED:
                    messages = self._get_all_messages_sync(test_uuid)
                    return BaseTestResponse.from_test_out_schema_and_messages(
                        test_response, messages, None
                    )

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_multiturn_test_impl_async(
        self,
        test_data: models.TestInSchema,
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
        test_uuid: str,
        question_uuid: str,
        user_response: str,
    ) -> models.ContinueMultiturnResponse:
        """
        Continue a multiturn conversation by providing a user response.

        :param test_uuid: UUID of the test
        :type test_uuid: str
        :param question_uuid: UUID of the question
        :type question_uuid: str
        :param user_response: User's response to continue the conversation
        :type user_response: str
        :return: Response containing the next step in the conversation
        :rtype: ContinueMultiturnResponse
        """
        response = continue_multiturn.sync_detailed(
            client=self.client,
            test_uuid=test_uuid,
            question_uuid=question_uuid,
            json_body=models.MultiturnUserResponseSchema(user_response=user_response),
        )

        if response.status_code == 404:
            raise ValueError("Test or question not found")

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        return response.parsed

    async def continue_multiturn_async(
        self,
        test_uuid: str,
        question_uuid: str,
        user_response: str,
    ) -> models.ContinueMultiturnResponse:
        """
        Continue a multiturn conversation asynchronously by providing a user response.

        Parameters are the same as continue_multiturn.
        """
        response = await continue_multiturn.asyncio_detailed(
            client=self.client,
            test_uuid=test_uuid,
            question_uuid=question_uuid,
            json_body=models.MultiturnUserResponseSchema(user_response=user_response),
        )

        if response.status_code == 404:
            raise ValueError("Test or question not found")

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        return response.parsed

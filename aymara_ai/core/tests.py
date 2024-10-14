import asyncio
import time
from typing import Coroutine, List, Optional, Union

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import (
    create_test,
    delete_test,
    get_test,
    get_test_questions,
    list_tests,
)
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import (
    BaseTestResponse,
    JailbreakTestResponse,
    ListTestResponse,
    SafetyTestResponse,
    Status,
)
from aymara_ai.utils.constants import (
    AYMARA_TEST_POLICY_PREFIX,
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_MAX_TOKENS,
    DEFAULT_NUM_QUESTIONS,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_TEST_NAME_LEN_MAX,
    DEFAULT_TEST_NAME_LEN_MIN,
    POLLING_INTERVAL,
    SUPPORTED_LANGUAGES,
    AymaraTestPolicy,
)


class TestMixin(AymaraAIProtocol):
    # Create Safety Test Methods
    def create_safety_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: Union[str, AymaraTestPolicy],
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions: int = DEFAULT_NUM_QUESTIONS,
    ) -> SafetyTestResponse:
        """
        Create an Aymara safety test synchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_policy: Policy of the test, which will measure compliance against this policy (required for safety tests).
        :type test_policy: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type num_test_questions: int, optional
        :return: Test response containing test details and generated questions.
        :rtype: SafetyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """
        return self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=None,
            test_language=test_language,
            num_test_questions=num_test_questions,
            is_async=False,
            test_type=TestType.SAFETY,
        )

    async def create_safety_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: Union[str, AymaraTestPolicy],
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions: int = DEFAULT_NUM_QUESTIONS,
    ) -> SafetyTestResponse:
        """
        Create an Aymara safety test asynchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_policy: Policy of the test, which will measure compliance against this policy (required for safety tests).
        :type test_policy: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type num_test_questions: int, optional
        :return: Test response containing test details and generated questions.
        :rtype: SafetyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """
        return await self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=None,
            test_language=test_language,
            num_test_questions=num_test_questions,
            is_async=True,
            test_type=TestType.SAFETY,
        )

    # Create Jailbreak Test Methods
    def create_jailbreak_test(
        self,
        test_name: str,
        student_description: str,
        test_system_prompt: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
    ) -> JailbreakTestResponse:
        """
        Create an Aymara jailbreak test synchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_system_prompt: System prompt of the jailbreak test.
        :type test_system_prompt: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :return: Test response containing test details and generated questions.
        :rtype: JailbreakTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_system_prompt is not provided for jailbreak tests.
        """
        return self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=None,
            test_system_prompt=test_system_prompt,
            test_language=test_language,
            is_async=False,
            test_type=TestType.JAILBREAK,
        )

    async def create_jailbreak_test_async(
        self,
        test_name: str,
        student_description: str,
        test_system_prompt: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
    ) -> JailbreakTestResponse:
        """
        Create an Aymara jailbreak test asynchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_system_prompt: System prompt of the jailbreak test.
        :type test_system_prompt: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :return: Test response containing test details and generated questions.
        :rtype: JailbreakTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_system_prompt is not provided for jailbreak tests.
        """
        return await self._create_test(
            test_name,
            student_description,
            test_policy=None,
            test_system_prompt=test_system_prompt,
            test_language=test_language,
            is_async=True,
            test_type=TestType.JAILBREAK,
        )

    def _create_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: Union[str, AymaraTestPolicy],
        test_system_prompt: str,
        test_language: str,
        is_async: bool,
        test_type: TestType,
        num_test_questions: Optional[int] = None,
    ) -> Union[BaseTestResponse, Coroutine[BaseTestResponse, None, None]]:
        # Convert AymaraTestPolicy to string and prefix with "aymara_test_policy:" for safety tests
        if test_type == TestType.SAFETY and isinstance(test_policy, AymaraTestPolicy):
            test_policy = f"{AYMARA_TEST_POLICY_PREFIX}{test_policy.value}"

        self._validate_test_inputs(
            test_name,
            student_description,
            test_policy,
            test_system_prompt,
            test_language,
            num_test_questions,
            test_type,
        )

        test_data = models.TestInSchema(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy if test_type == TestType.SAFETY else None,
            test_system_prompt=test_system_prompt
            if test_type == TestType.JAILBREAK
            else None,
            test_language=test_language,
            num_test_questions=num_test_questions,
            test_type=test_type,
        )

        if is_async:
            return self._create_and_wait_for_test_impl_async(test_data)
        else:
            return self._create_and_wait_for_test_impl_sync(test_data)

    def _validate_test_inputs(
        self,
        test_name: str,
        student_description: str,
        test_policy: Optional[str],
        test_system_prompt: Optional[str],
        test_language: str,
        num_test_questions: Optional[int],
        test_type: TestType,
    ) -> None:
        if not student_description:
            raise ValueError("student_description is required")

        if test_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"test_language must be one of {SUPPORTED_LANGUAGES}")

        if test_type == TestType.SAFETY and test_policy is None:
            raise ValueError("test_policy is required for safety tests")

        if test_type == TestType.JAILBREAK and test_system_prompt is None:
            raise ValueError("test_system_prompt is required for jailbreak tests")

        if (
            len(test_name) < DEFAULT_TEST_NAME_LEN_MIN
            or len(test_name) > DEFAULT_TEST_NAME_LEN_MAX
        ):
            raise ValueError(
                f"test_name must be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters"
            )

        if num_test_questions is not None and (
            num_test_questions < DEFAULT_NUM_QUESTIONS_MIN
            or num_test_questions > DEFAULT_NUM_QUESTIONS_MAX
        ):
            raise ValueError(
                f"num_test_questions must be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions"
            )

        token1 = len(student_description) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER

        token_2_field = (
            "test_policy" if test_type == TestType.SAFETY else "test_system_prompt"
        )
        token2 = (
            len(test_policy) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            if test_type == TestType.SAFETY
            else len(test_system_prompt) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
        )

        total_tokens = token1 + token2
        if total_tokens > DEFAULT_MAX_TOKENS:
            raise ValueError(
                f"student_description is ~{token1:,} tokens and {token_2_field} is ~{token2:,} tokens. They are ~{total_tokens:,} tokens in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
            )

    def _create_and_wait_for_test_impl_sync(
        self, test_data: models.TestInSchema
    ) -> BaseTestResponse:
        start_time = time.time()
        response = create_test.sync_detailed(client=self.client, body=test_data)

        create_response = response.parsed

        if response.status_code == 422:
            raise ValueError(f"{create_response.detail}")

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

                if test_response.test_status == models.TestStatus.FAILED:
                    failure_reason = "Internal server error, please try again."
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, failure_reason
                    )

                if test_response.test_status == models.TestStatus.FINISHED:
                    questions = self._get_all_questions_sync(test_uuid)
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, questions, None
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time_secs:
                    test_response.test_status = models.TestStatus.FAILED
                    self.logger.update_progress_bar(test_uuid, Status.FAILED)
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Test creation timed out"
                    )

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_test_impl_async(
        self, test_data: models.TestInSchema
    ) -> BaseTestResponse:
        start_time = time.time()
        response = await create_test.asyncio_detailed(
            client=self.client, body=test_data
        )

        create_response = response.parsed

        if response.status_code == 422:
            raise ValueError(f"{create_response.detail}")

        test_uuid = create_response.test_uuid
        test_name = create_response.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            Status.from_api_status(create_response.test_status),
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

                if test_response.test_status == models.TestStatus.FAILED:
                    failure_reason = "Internal server error, please try again."
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, failure_reason
                    )

                if test_response.test_status == models.TestStatus.FINISHED:
                    questions = await self._get_all_questions_async(test_uuid)
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, questions, None
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time_secs:
                    test_response.test_status = models.TestStatus.FAILED
                    self.logger.update_progress_bar(test_uuid, Status.FAILED)
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Test creation timed out"
                    )

                await asyncio.sleep(POLLING_INTERVAL)

    # Get Test Methods
    def get_test(self, test_uuid: str) -> BaseTestResponse:
        """
        Get the current status of a test synchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: TestResponse
        """
        return self._get_test(test_uuid, is_async=False)

    async def get_test_async(self, test_uuid: str) -> BaseTestResponse:
        """
        Get the current status of a test asynchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: TestResponse
        """
        return await self._get_test(test_uuid, is_async=True)

    def _get_test(
        self, test_uuid: str, is_async: bool
    ) -> Union[BaseTestResponse, Coroutine[BaseTestResponse, None, None]]:
        if is_async:
            return self._get_test_async_impl(test_uuid)
        else:
            return self._get_test_sync_impl(test_uuid)

    def _get_test_sync_impl(self, test_uuid: str) -> BaseTestResponse:
        response = get_test.sync_detailed(client=self.client, test_uuid=test_uuid)

        if response.status_code == 404:
            raise ValueError(f"Test with UUID {test_uuid} not found")

        test_response = response.parsed
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = self._get_all_questions_sync(test_uuid)

        return BaseTestResponse.from_test_out_schema_and_questions(
            test_response, questions
        )

    async def _get_test_async_impl(self, test_uuid: str) -> BaseTestResponse:
        response = await get_test.asyncio_detailed(
            client=self.client, test_uuid=test_uuid
        )

        if response.status_code == 404:
            raise ValueError(f"Test with UUID {test_uuid} not found")

        test_response = response.parsed
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = await self._get_all_questions_async(test_uuid)

        return BaseTestResponse.from_test_out_schema_and_questions(
            test_response, questions
        )

    # List Tests Methods
    def list_tests(self) -> ListTestResponse:
        """
        List all tests synchronously.
        """
        tests = self._list_tests_sync_impl()

        return ListTestResponse(tests)

    async def list_tests_async(self) -> ListTestResponse:
        """
        List all tests asynchronously.
        """
        tests = await self._list_tests_async_impl()

        return ListTestResponse(tests)

    def _list_tests_sync_impl(self) -> List[BaseTestResponse]:
        all_tests = []
        offset = 0
        while True:
            response = list_tests.sync_detailed(client=self.client, offset=offset)

            paged_response = response.parsed
            all_tests.extend(paged_response.items)
            if len(all_tests) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            BaseTestResponse.from_test_out_schema_and_questions(test)
            for test in all_tests
        ]

    async def _list_tests_async_impl(self) -> List[BaseTestResponse]:
        all_tests = []
        offset = 0
        while True:
            response = await list_tests.asyncio_detailed(
                client=self.client, offset=offset
            )

            paged_response = response.parsed
            all_tests.extend(paged_response.items)
            if len(all_tests) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            BaseTestResponse.from_test_out_schema_and_questions(test)
            for test in all_tests
        ]

    # Helper Methods
    def _get_all_questions_sync(self, test_uuid: str) -> List[models.QuestionSchema]:
        questions = []
        offset = 0
        while True:
            response = get_test_questions.sync_detailed(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            if response.status_code == 404:
                raise ValueError(f"Test with UUID {test_uuid} not found")

            paged_response = response.parsed
            questions.extend(paged_response.items)
            if len(questions) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return questions

    async def _get_all_questions_async(
        self, test_uuid: str
    ) -> List[models.QuestionSchema]:
        questions = []
        offset = 0
        while True:
            response = await get_test_questions.asyncio_detailed(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            if response.status_code == 404:
                raise ValueError(f"Test with UUID {test_uuid} not found")

            paged_response = response.parsed
            questions.extend(paged_response.items)
            if len(questions) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return questions

    def delete_test(self, test_uuid: str) -> None:
        """
        Delete a test synchronously.
        """
        response = delete_test.sync_detailed(client=self.client, test_uuid=test_uuid)
        if response.status_code == 404:
            raise ValueError(f"Test with UUID {test_uuid} not found")

    async def delete_test_async(self, test_uuid: str) -> None:
        """
        Delete a test asynchronously.
        """
        response = await delete_test.asyncio_detailed(
            client=self.client, test_uuid=test_uuid
        )
        if response.status_code == 404:
            raise ValueError(f"Test with UUID {test_uuid} not found")

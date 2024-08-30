import asyncio
import time
from typing import Coroutine, List, Union

from aymara_sdk.core.protocols import AymaraAIProtocol
from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.generated.aymara_api_client.api.tests import (
    core_api_create_test,
    core_api_get_test,
    core_api_get_test_questions,
    core_api_list_tests,
)
from aymara_sdk.types import Status, TestResponse
from aymara_sdk.utils.constants import (
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_MAX_TOKENS,
    DEFAULT_NUM_QUESTIONS,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_TEST_NAME_LEN_MAX,
    DEFAULT_TEST_NAME_LEN_MIN,
    POLLING_INTERVAL,
)


class TestMixin(AymaraAIProtocol):
    # Create Test Methods
    def create_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
    ) -> TestResponse:
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
        :param n_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type n_test_questions: int, optional
        :return: Test response containing test details and generated questions.
        :rtype: TestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If n_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """
        return self._create_test(
            test_name,
            student_description,
            test_policy,
            test_language,
            n_test_questions,
            is_async=False,
        )

    async def create_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
    ) -> TestResponse:
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
        :param n_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type n_test_questions: int, optional
        :return: Test response containing test details and generated questions.
        :rtype: TestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If n_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """
        return await self._create_test(
            test_name,
            student_description,
            test_policy,
            test_language,
            n_test_questions,
            is_async=True,
        )

    def _create_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str,
        n_test_questions: int,
        is_async: bool,
    ) -> Union[TestResponse, Coroutine[TestResponse, None, None]]:
        self._validate_test_inputs(
            test_name, student_description, test_policy, n_test_questions
        )

        test_data = models.TestSchema(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_language=test_language,
            n_test_questions=n_test_questions,
        )

        return self._create_and_wait_for_test_impl(test_data, is_async)

    def _validate_test_inputs(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        n_test_questions: int,
    ) -> None:
        if test_policy is None:
            raise ValueError("test_policy is required for safety tests")

        if (
            len(test_name) < DEFAULT_TEST_NAME_LEN_MIN
            or len(test_name) > DEFAULT_TEST_NAME_LEN_MAX
        ):
            raise ValueError(
                f"test_name must be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters"
            )

        if (
            n_test_questions < DEFAULT_NUM_QUESTIONS_MIN
            or n_test_questions > DEFAULT_NUM_QUESTIONS_MAX
        ):
            raise ValueError(
                f"n_test_questions must be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions"
            )

        token1 = len(student_description) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
        token2 = len(test_policy) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER

        total_tokens = token1 + token2
        if total_tokens > DEFAULT_MAX_TOKENS:
            raise ValueError(
                f"student_description is ~{token1:,} tokens and test_policy is ~{token2:,} tokens. They are ~{total_tokens:,} tokens in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
            )

    async def _create_and_wait_for_test_impl(
        self, test_data: models.TestSchema, is_async: bool
    ) -> TestResponse:
        start_time = time.time()
        create_response = (
            await core_api_create_test.asyncio(client=self.client, body=test_data)
            if is_async
            else core_api_create_test.sync(client=self.client, body=test_data)
        )

        test_uuid = create_response.test_uuid
        test_name = create_response.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            Status.from_api_status(create_response.test_status),
        ):
            while True:
                test_response = (
                    await core_api_get_test.asyncio(
                        client=self.client, test_uuid=test_uuid
                    )
                    if is_async
                    else core_api_get_test.sync(client=self.client, test_uuid=test_uuid)
                )

                self.logger.update_progress_bar(
                    test_uuid,
                    Status.from_api_status(test_response.test_status),
                )

                if test_response.test_status == models.TestStatus.FAILED:
                    failure_reason = "Internal server error, please try again."
                    return TestResponse.from_test_out_schema_and_questions(
                        test_response, None, failure_reason
                    )

                if test_response.test_status == models.TestStatus.FINISHED:
                    questions = (
                        await self._get_all_questions_async(test_uuid)
                        if is_async
                        else self._get_all_questions_sync(test_uuid)
                    )
                    return TestResponse.from_test_out_schema_and_questions(
                        test_response, questions
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    test_response.test_status = models.TestStatus.FAILED
                    self.logger.update_progress_bar(test_uuid, Status.FAILED)
                    return TestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Test creation timed out"
                    )

                if is_async:
                    await asyncio.sleep(POLLING_INTERVAL)
                else:
                    time.sleep(POLLING_INTERVAL)

    # Get Test Methods
    def get_test(self, test_uuid: str) -> TestResponse:
        """
        Get the current status of a test synchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: TestResponse
        """
        return self._get_test(test_uuid, is_async=False)

    async def get_test_async(self, test_uuid: str) -> TestResponse:
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
    ) -> Union[TestResponse, Coroutine[TestResponse, None, None]]:
        if is_async:
            return self._get_test_async_impl(test_uuid)
        else:
            return self._get_test_sync_impl(test_uuid)

    def _get_test_sync_impl(self, test_uuid: str) -> TestResponse:
        test_response = core_api_get_test.sync(client=self.client, test_uuid=test_uuid)
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = self._get_all_questions_sync(test_uuid)

        return TestResponse.from_test_out_schema_and_questions(test_response, questions)

    async def _get_test_async_impl(self, test_uuid: str) -> TestResponse:
        test_response = await core_api_get_test.asyncio(
            client=self.client, test_uuid=test_uuid
        )
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = await self._get_all_questions_async(test_uuid)

        return TestResponse.from_test_out_schema_and_questions(test_response, questions)

    # List Tests Methods
    def list_tests(self) -> List[TestResponse]:
        """
        List all tests synchronously.
        """
        return self._list_tests_sync_impl()

    async def list_tests_async(self) -> List[TestResponse]:
        """
        List all tests asynchronously.
        """
        return await self._list_tests_async_impl()

    def _list_tests_sync_impl(self) -> List[TestResponse]:
        test_response = core_api_list_tests.sync(client=self.client)
        return [
            TestResponse.from_test_out_schema_and_questions(test)
            for test in test_response
        ]

    async def _list_tests_async_impl(self) -> List[TestResponse]:
        test_response = await core_api_list_tests.asyncio(client=self.client)
        return [
            TestResponse.from_test_out_schema_and_questions(test)
            for test in test_response
        ]

    # Helper Methods
    def _get_all_questions_sync(self, test_uuid: str) -> List[models.QuestionSchema]:
        questions = []
        offset = 0
        while True:
            response = core_api_get_test_questions.sync(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            questions.extend(response.items)
            if len(questions) >= response.count:
                break
            offset += len(response.items)
        return questions

    async def _get_all_questions_async(
        self, test_uuid: str
    ) -> List[models.QuestionSchema]:
        questions = []
        offset = 0
        while True:
            response = await core_api_get_test_questions.asyncio(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            questions.extend(response.items)
            if len(questions) >= response.count:
                break
            offset += len(response.items)
        return questions

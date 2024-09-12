import asyncio
import time
from typing import Coroutine, List, Optional, Union

import pandas as pd

from aymara_sdk.core.protocols import AymaraAIProtocol
from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.generated.aymara_api_client.api.tests import (
    create_test,
    get_test,
    get_test_questions,
    list_tests,
)
from aymara_sdk.types import Status, TestResponse
from aymara_sdk.utils.constants import (
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
    # Create Test Methods
    def create_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: Union[str, AymaraTestPolicy],
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
        test_policy: Union[str, AymaraTestPolicy],
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
        test_policy: Union[str, AymaraTestPolicy],
        test_language: str,
        n_test_questions: int,
        is_async: bool,
    ) -> Union[TestResponse, Coroutine[TestResponse, None, None]]:
        # Convert AymaraTestPolicy to string and prefix with "aymara_test_policy:"
        if isinstance(test_policy, AymaraTestPolicy):
            test_policy = f"{AYMARA_TEST_POLICY_PREFIX}{test_policy.value}"

        self._validate_test_inputs(
            test_name, student_description, test_policy, test_language, n_test_questions
        )

        test_data = models.TestSchema(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_language=test_language,
            n_test_questions=n_test_questions,
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
        test_language: str,
        n_test_questions: int,
    ) -> None:
        if not student_description:
            raise ValueError("student_description is required")

        if test_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"test_language must be one of {SUPPORTED_LANGUAGES}")

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

    def _create_and_wait_for_test_impl_sync(
        self, test_data: models.TestSchema
    ) -> TestResponse:
        start_time = time.time()
        create_response = create_test.sync(client=self.client, body=test_data)

        test_uuid = create_response.test_uuid
        test_name = create_response.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            Status.from_api_status(create_response.test_status),
        ):
            while True:
                test_response = get_test.sync(client=self.client, test_uuid=test_uuid)

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
                    questions = self._get_all_questions_sync(test_uuid)
                    return TestResponse.from_test_out_schema_and_questions(
                        test_response, questions, None
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    test_response.test_status = models.TestStatus.FAILED
                    self.logger.update_progress_bar(test_uuid, Status.FAILED)
                    return TestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Test creation timed out"
                    )

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_test_impl_async(
        self, test_data: models.TestSchema
    ) -> TestResponse:
        start_time = time.time()
        create_response = await create_test.asyncio(client=self.client, body=test_data)

        test_uuid = create_response.test_uuid
        test_name = create_response.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            Status.from_api_status(create_response.test_status),
        ):
            while True:
                test_response = await get_test.asyncio(
                    client=self.client, test_uuid=test_uuid
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
                    questions = await self._get_all_questions_async(test_uuid)
                    return TestResponse.from_test_out_schema_and_questions(
                        test_response, questions, None
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    test_response.test_status = models.TestStatus.FAILED
                    self.logger.update_progress_bar(test_uuid, Status.FAILED)
                    return TestResponse.from_test_out_schema_and_questions(
                        test_response, None, "Test creation timed out"
                    )

                await asyncio.sleep(POLLING_INTERVAL)

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
        test_response = get_test.sync(client=self.client, test_uuid=test_uuid)
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = self._get_all_questions_sync(test_uuid)

        return TestResponse.from_test_out_schema_and_questions(test_response, questions)

    async def _get_test_async_impl(self, test_uuid: str) -> TestResponse:
        test_response = await get_test.asyncio(client=self.client, test_uuid=test_uuid)
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = await self._get_all_questions_async(test_uuid)

        return TestResponse.from_test_out_schema_and_questions(test_response, questions)

    # List Tests Methods
    def list_tests(self, as_df=False) -> Union[List[TestResponse], pd.DataFrame]:
        """
        List all tests synchronously.
        """
        tests = self._list_tests_sync_impl()

        if as_df:
            tests = self._tests_to_df(tests)

        return tests

    async def list_tests_async(
        self, as_df=False
    ) -> Union[List[TestResponse], pd.DataFrame]:
        """
        List all tests asynchronously.
        """
        tests = await self._list_tests_async_impl()

        if as_df:
            tests = self._tests_to_df(tests)

        return tests

    def _list_tests_sync_impl(self) -> List[TestResponse]:
        all_tests = []
        offset = 0
        while True:
            paged_response = list_tests.sync(client=self.client, offset=offset)
            all_tests.extend(paged_response.items)
            if len(all_tests) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            TestResponse.from_test_out_schema_and_questions(test) for test in all_tests
        ]

    async def _list_tests_async_impl(self) -> List[TestResponse]:
        all_tests = []
        offset = 0
        while True:
            paged_response = await list_tests.asyncio(client=self.client, offset=offset)
            all_tests.extend(paged_response.items)
            if len(all_tests) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            TestResponse.from_test_out_schema_and_questions(test) for test in all_tests
        ]

    def _tests_to_df(self, tests):
        return pd.DataFrame(
            [
                {
                    "test_uuid": test.test_uuid,
                    "test_name": test.test_name,
                    "test_status": test.test_status,
                    "failure_reason": test.failure_reason,
                }
                for test in tests
            ]
        )

    # Helper Methods
    def _get_all_questions_sync(self, test_uuid: str) -> List[models.QuestionSchema]:
        questions = []
        offset = 0
        while True:
            response = get_test_questions.sync(
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
            response = await get_test_questions.asyncio(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            questions.extend(response.items)
            if len(questions) >= response.count:
                break
            offset += len(response.items)
        return questions

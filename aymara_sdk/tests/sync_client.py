import time
from typing import List
from aymara_sdk.constants import (
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_NUM_QUESTIONS,
    DEFAULT_TEST_NAME_LEN_MAX,
    DEFAULT_TEST_NAME_LEN_MIN,
    POLLING_INTERVAL,
)
from aymara_sdk.errors import TestCreationError
from aymara_sdk.generated.aymara_api_client.api.tests import (
    core_api_create_test,
    core_api_get_test,
    core_api_get_test_questions,
    core_api_list_tests,
)
from aymara_sdk.generated.aymara_api_client.models.test_schema import TestSchema
from aymara_sdk.base import AymaraAIProtocol
from aymara_sdk.types import CreateTestResponse, GetTestResponse, transform_api_status
from aymara_sdk.generated.aymara_api_client import models


class TestSyncMixin(AymaraAIProtocol):
    def create_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
    ) -> CreateTestResponse:
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
        :rtype: CreateTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If n_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """
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

        return self._create_and_wait_for_test(
            TestSchema(
                test_name=test_name,
                student_description=student_description,
                test_policy=test_policy,
                test_language=test_language,
                n_test_questions=n_test_questions,
            )
        )

    def get_test(self, test_uuid: str) -> GetTestResponse:
        """
        Get the current status of a test synchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: GetTestResponse
        """
        self.logger.debug(f"Getting test synchronously for: {test_uuid}")
        test_response = core_api_get_test.sync(client=self.client, test_uuid=test_uuid)
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = self._get_all_questions(test_uuid)

        return GetTestResponse.from_test_out_schema_and_questions(
            test_response, questions
        )

    def list_tests(self) -> List[GetTestResponse]:
        """
        List all tests synchronously.
        """
        self.logger.debug("Listing tests synchronously")
        test_response = core_api_list_tests.sync(client=self.client)
        return [
            GetTestResponse.from_test_out_schema_and_questions(test)
            for test in test_response
        ]

    def _create_and_wait_for_test(
        self, test_data: models.TestSchema
    ) -> CreateTestResponse:
        start_time = time.time()
        create_response = core_api_create_test.sync(client=self.client, body=test_data)

        test_uuid = create_response.test_uuid
        test_name = create_response.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            transform_api_status(create_response.test_status),
        ):
            while True:
                test_response = core_api_get_test.sync(
                    client=self.client, test_uuid=test_uuid
                )

                self.logger.update_progress_bar(
                    test_uuid,
                    transform_api_status(test_response.test_status),
                )

                if (
                    test_response.test_status == models.TestStatus.FINISHED
                    or test_response.test_status == models.TestStatus.FAILED
                ):
                    questions = self._get_all_questions(test_uuid)

                    return CreateTestResponse.from_test_out_schema_and_questions(
                        test_response, questions
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    raise TestCreationError(f"Test creation timed out for {test_name}")

                time.sleep(POLLING_INTERVAL)

    def _get_all_questions(self, test_uuid: str) -> List[models.QuestionSchema]:
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

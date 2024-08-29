"""
Aymara AI SDK

This module provides the main interface for interacting with the Aymara AI API.
It includes functionality for creating and managing tests, scoring tests, and visualizing results.
"""

import math
import os
import time
import asyncio
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd


from typing import List, Optional, Union
from aymara_sdk.errors import ScoreRunError
from aymara_sdk.generated.aymara_api_client.api.score_runs import (
    core_api_create_score_run,
    core_api_get_score_run,
    core_api_get_score_run_answers,
)
from aymara_sdk.generated.aymara_api_client.api.tests import (
    core_api_create_test,
    core_api_get_test,
    core_api_get_test_questions,
)
from aymara_sdk.generated.aymara_api_client import (
    models,
    client,
)
from aymara_sdk.logger import SDKLogger

from aymara_sdk.types import (
    GetTestResponse,
    CreateTestResponse,
    QuestionResponse,
    ScoreTestParams,
    ScoreTestResponse,
    ScoredAnswerResponse,
    StudentAnswer,
    TestParams,
)

from aymara_sdk.types import Status


POLLING_INTERVAL = 1  # seconds

# Test Creation Defaults
DEFAULT_MAX_WAIT_TIME: int = 120
DEFAULT_NUM_QUESTIONS: int = 20
DEFAULT_TEST_LANGUAGE: str = "en"

# Input Limit Defaults
DEFAULT_TEST_NAME_LEN_MIN: int = 1
DEFAULT_TEST_NAME_LEN_MAX: int = 100
DEFAULT_NUM_QUESTIONS_MIN: int = 1
DEFAULT_NUM_QUESTIONS_MAX: int = 150
DEFAULT_CHAR_TO_TOKEN_MULTIPLIER: float = 0.15
DEFAULT_MAX_TOKENS: int = 100000


class AymaraAI:
    """
    Aymara AI SDK Client

    This class provides methods for interacting with the Aymara AI API, including
    creating and managing tests, scoring tests, and retrieving results.

    :param api_key: API key for authenticating with the Aymara AI API.
        Read from the AYMARA_API_KEY environment variable if not provided.
    :type api_key: str, optional
    :param base_url: Base URL for the Aymara AI API, defaults to "https://api.aymara.ai".
    :type base_url: str, optional
    :param max_wait_time: Maximum wait time for test creation, defaults to DEFAULT_MAX_WAIT_TIME.
    :type max_wait_time: int, optional
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.aymara.ai",
        max_wait_time: int = DEFAULT_MAX_WAIT_TIME,
    ):
        self.logger = SDKLogger()

        if api_key is None:
            api_key = os.getenv("AYMARA_API_KEY")
        if api_key is None:
            self.logger.error("API key is required")
            raise ValueError("API key is required")

        self.client = client.Client(base_url=base_url, headers={"x-api-key": api_key})
        self.max_wait_time = max_wait_time
        self.logger.info(f"AymaraAI client initialized with base URL: {base_url}")

    def __enter__(self):
        """
        Enable the AymaraAI to be used as a context manager for synchronous operations.

        :return: The AymaraAI client instance.
        :rtype: AymaraAI
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensure the synchronous session is closed when exiting the context.

        :param exc_type: Exception type.
        :type exc_type: type
        :param exc_val: Exception value.
        :type exc_val: Exception
        :param exc_tb: Exception traceback.
        :type exc_tb: traceback
        """
        self.client._client.close()

    async def __aenter__(self):
        """
        Enable the AymaraAI to be used as an async context manager for asynchronous operations.

        :return: The AymaraAI client instance.
        :rtype: AymaraAI
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Ensure the asynchronous session is closed when exiting the async context.

        :param exc_type: Exception type.
        :type exc_type: type
        :param exc_val: Exception value.
        :type exc_val: Exception
        :param exc_tb: Exception traceback.
        :type exc_tb: traceback
        """
        await self.client._async_client.aclose()

    # ----------------
    # Tests
    # ----------------

    def create_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
    ) -> CreateTestResponse:
        """
        Create a test synchronously and wait for completion.

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
        :raises ValueError: If test_system_prompt is not provided for jailbreak tests.
        """
        test_data = self._prepare_test_data(
            test_name,
            test_policy,
            student_description,
            test_language,
            n_test_questions,
        )

        return self._create_and_wait_for_test(test_data)

    async def create_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
    ) -> CreateTestResponse:
        """
        Create a test asynchronously and wait for completion.

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
        :raises ValueError: If test_system_prompt is not provided for jailbreak tests.
        """
        test_data = self._prepare_test_data(
            test_name,
            test_policy,
            student_description,
            test_language,
            n_test_questions,
        )

        return await self._create_and_wait_for_test_async(test_data)

    def get_test(self, test_uuid: str) -> GetTestResponse:
        """
        Get the current status of a test, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: GetTestResponse
        """
        self.logger.debug(f"Getting test for: {test_uuid}")
        test_response = core_api_get_test.sync(client=self.client, test_uuid=test_uuid)
        test_status = self._transform_test_status(test_response.test_status)
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = self._get_all_questions(test_uuid)

        self.logger.debug(f"Test status for {test_uuid}: {test_status.value}")
        return GetTestResponse(
            test_uuid=test_uuid,
            test_name=test_response.test_name,
            test_status=test_status,
            test_type=test_response.test_type,
            questions=questions,
        )

    async def get_test_async(self, test_uuid: str) -> GetTestResponse:
        """
        Get the current status of a test asynchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: GetTestResponse
        """
        self.logger.debug(f"Getting test asynchronously for: {test_uuid}")
        test_response = await core_api_get_test.asyncio(
            client=self.client, test_uuid=test_uuid
        )
        test_status = self._transform_test_status(test_response.test_status)
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = await self._get_all_questions_async(test_uuid)

        self.logger.debug("Test status for %s: %s", test_uuid, test_status.value)
        return GetTestResponse(
            test_uuid=test_uuid,
            test_name=test_response.test_name,
            test_status=test_status,
            test_type=test_response.test_type,
            questions=[
                QuestionResponse.from_question_schema(question)
                for question in questions
            ]
            if questions
            else None,
        )

    async def create_multiple_tests_async(
        self, test_inputs: List[TestParams]
    ) -> List[CreateTestResponse]:
        """
        Create multiple tests asynchronously and monitor their progress.

        :param test_inputs: List of TestParams objects containing test creation inputs.
        :type test_inputs: List[TestParams]
        :return: List of CreateTestResponse objects for the created tests.
        :rtype: List[CreateTestResponse]
        """

        tasks = [
            self._create_and_wait_for_test_async(test_data) for test_data in test_inputs
        ]
        results = []
        for task in tqdm.as_completed(
            tasks,
            desc="Creating tests...",
            unit="tests",
            bar_format="{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}",
        ):
            result = await task
            results.append(result)
        return results

    def _prepare_test_data(
        self,
        test_name: str,
        test_policy: str,
        student_description: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
    ) -> models.TestSchema:
        """
        Prepare the test data for creating a test.

        :param test_name: Name of the test.
        :type test_name: str
        :param test_policy: Policy for the test (required for safety tests).
        :type test_policy: Optional[str]
        :param test_system_prompt: System prompt for the test (required for jailbreak tests).
        :type test_system_prompt: Optional[str]
        :param student_description: Description of the student.
        :type student_description: str
        :param test_language: Language of the test, defaults to DEFAULT_TEST_LANGUAGE.
        :type test_language: str, optional
        :param n_test_questions: Number of test questions, defaults to DEFAULT_NUM_QUESTIONS.
        :type n_test_questions: int, optional
        :return: Prepared test data.
        :rtype: models.TestSchema

        :raises ValueError: If test_policy is not provided for safety tests.
        :raises ValueError: If test_system_prompt is not provided for jailbreak tests.
        """
        if test_policy is None:
            self.logger.error("test_policy is required for safety tests")
            raise ValueError("test_policy is required for safety tests")

        return models.TestSchema(
            test_name=test_name,
            test_language=test_language,
            n_test_questions=n_test_questions,
            student_description=student_description,
            test_policy=test_policy,
        )

    def _create_test_response(
        self,
        test_uuid: str,
        test_name: str,
        test_status: models.TestStatus,
        questions: List[models.QuestionSchema],
    ) -> CreateTestResponse:
        """
        Create a test response.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param test_status: Status of the test.
        :type test_status: models.TestStatus
        :param questions: List of test questions.
        :type questions: List[models.QuestionSchema]
        :return: Created test response.
        :rtype: CreateTestResponse
        """
        return CreateTestResponse(
            test_uuid=test_uuid,
            test_name=test_name,
            test_status=self._transform_test_status(test_status),
            questions=[
                QuestionResponse.from_question_schema(question)
                for question in questions
            ],
        )

    def _get_all_questions(self, test_uuid: str) -> List[models.QuestionSchema]:
        """
        Get all questions for a test, paginating through the questions if necessary.
        """
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
        """
        Get all questions for a test asynchronously.
        """

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

    def _create_and_wait_for_test(
        self, test_data: models.TestSchema
    ) -> CreateTestResponse:
        start_time = time.time()
        create_response = core_api_create_test.sync(client=self.client, body=test_data)

        test_uuid = create_response.test_uuid
        test_name = test_data.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            self._transform_test_status(create_response.test_status),
        ):
            while True:
                test_response = core_api_get_test.sync(
                    client=self.client, test_uuid=test_uuid
                )

                self.logger.update_progress_bar(
                    test_uuid,
                    self._transform_test_status(test_response.test_status),
                )

                if (
                    test_response.test_status == models.TestStatus.FINISHED
                    or test_response.test_status == models.TestStatus.FAILED
                ):
                    questions = self._get_all_questions(test_uuid)

                    return self._create_test_response(
                        test_uuid,
                        test_name,
                        test_response.test_status,
                        questions,
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    self.logger.error(f"Test creation timed out for {test_name}")
                    return None

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_test_async(
        self, test_data: models.TestSchema
    ) -> Optional[CreateTestResponse]:
        start_time = time.time()
        create_response = await core_api_create_test.asyncio(
            client=self.client, body=test_data
        )

        test_uuid = create_response.test_uuid
        test_name = test_data.test_name

        with self.logger.progress_bar(
            test_name,
            test_uuid,
            self._transform_test_status(create_response.test_status),
        ):
            while True:
                test_response = await core_api_get_test.asyncio(
                    client=self.client, test_uuid=test_uuid
                )

                self.logger.update_progress_bar(
                    test_uuid,
                    self._transform_test_status(test_response.test_status),
                )

                if (
                    test_response.test_status == models.TestStatus.FINISHED
                    or test_response.test_status == models.TestStatus.FAILED
                ):
                    questions = await self._get_all_questions_async(test_uuid)

                    return self._create_test_response(
                        test_uuid,
                        test_name,
                        test_response.test_status,
                        questions,
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    self.logger.error(f"Test creation timed out for {test_name}")
                    return None

                await asyncio.sleep(POLLING_INTERVAL)

    def _transform_test_status(self, api_test_status: models.TestStatus) -> Status:
        """
        Transform an API test status to the user-friendly test status.

        :param api_test_status: API test status.
        :type api_test_status: APITestStatus
        :return: Transformed test status.
        :rtype: Status
        """
        status_mapping = {
            "record_created": Status.PENDING,
            "generating_questions": Status.PENDING,
            "finished": Status.COMPLETED,
            "failed": Status.FAILED,
        }
        return status_mapping[api_test_status]

    # ----------------
    # Scores
    # ----------------

    def score_test(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
    ) -> ScoreTestResponse:
        """
        Score a test synchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of StudentAnswer objects containing student responses.
        :type student_answers: List[StudentAnswer]
        :return: Score response.
        :rtype: ScoreTestResponse
        """
        score_data = self._prepare_score_data(test_uuid, student_answers)

        return self._create_and_wait_for_score(score_data)

    async def score_test_async(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
    ) -> ScoreTestResponse:
        """
        Score a test asynchronously.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of StudentAnswer objects containing student responses.
        :type student_answers: List[StudentAnswer]
        :return: Score response.
        :rtype: ScoreTestResponse
        """
        self.logger.info("Scoring test asynchronously: %s", test_uuid)
        score_data = self._prepare_score_data(test_uuid, student_answers)

        self.logger.info("Scoring test and waiting for completion: %s", test_uuid)
        score_response = await self._create_and_wait_for_score_async(score_data)

        self.logger.info(
            "Score run created asynchronously: %s", score_response.score_run_uuid
        )
        return score_response

    def get_score_run(self, score_run_uuid: str) -> ScoreTestResponse:
        """
        Get the current status of a score run, and answers with scores if it is completed.

        :param score_run_uuid: UUID of the score run.
        :type score_run_uuid: str
        :return: Score test response.
        :rtype: ScoreTestResponse
        """
        score_run_response = core_api_get_score_run.sync(
            client=self.client, score_run_uuid=score_run_uuid
        )
        print(score_run_response)
        answers = None
        if score_run_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = self._get_all_score_run_answers(score_run_uuid)
        return self._create_score_run_response(
            score_run_response.test.test_uuid,
            score_run_response.test.test_name,
            score_run_response.test.n_test_questions,
            score_run_uuid,
            score_run_response.score_run_status,
            answers,
        )

    async def get_score_run_async(self, score_run_uuid: str) -> ScoreTestResponse:
        """
        Get the current status of a score run asynchronously,
        and answers with scores if it is completed.

        :param score_run_uuid: UUID of the score run.
        :type score_run_uuid: str
        :return: Score test response.
        :rtype: ScoreTestResponse
        """
        self.logger.info("Getting score run asynchronously for: %s", score_run_uuid)
        score_run_response = await core_api_get_score_run.asyncio(
            client=self.client, score_run_uuid=score_run_uuid
        )
        answers = None
        if score_run_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = await self._get_all_score_run_answers_async(score_run_uuid)
        return self._create_score_run_response(
            score_run_response.test.test_uuid,
            score_run_response.test.test_name,
            score_run_response.test.n_test_questions,
            score_run_uuid,
            score_run_response.score_run_status,
            answers,
        )

    async def score_multiple_tests_async(
        self, score_inputs: List[ScoreTestParams]
    ) -> List[ScoreTestResponse]:
        """
        Score multiple tests asynchronously and monitor their progress.

        :param score_inputs: List of ScoreTestParams objects containing score run inputs.
        :type score_inputs: List[ScoreTestParams]
        :return: List of ScoreTestResponse objects for the scored tests.
        :rtype: List[ScoreTestResponse]
        """

        tasks = [
            self._create_and_wait_for_score_async(
                self._prepare_score_data(
                    score_input.test_uuid, score_input.student_responses
                )
            )
            for score_input in score_inputs
        ]
        results = []
        for task in tqdm.as_completed(
            tasks,
            desc="Scoring tests...",
            unit="tests",
            bar_format="{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}",
        ):
            result = await task
            results.append(result)
        return results

    def _prepare_score_data(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
    ) -> models.ScoreRunSchema:
        """
        Prepare the score data for creating a score run.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of StudentAnswer objects containing student responses.
        :type student_answers: List[StudentAnswer]
        :return: Prepared score data.
        :rtype: models.ScoreRunSchema
        """

        if not student_answers:
            raise ValueError("At least one student response must be provided")

        return models.ScoreRunSchema(
            test_uuid=test_uuid,
            answers=[
                StudentAnswer.to_answer_in_schema(answer) for answer in student_answers
            ],
        )

    def _create_and_wait_for_score(
        self, score_data: models.ScoreRunSchema
    ) -> ScoreTestResponse:
        """
        Create a score run and wait for its completion.

        :param score_data: Prepared score data.
        :type score_data: models.ScoreRunSchema
        :return: Score test response.
        :rtype: ScoreTestResponse
        """
        start_time = time.time()
        score_response = core_api_create_score_run.sync(
            client=self.client, body=score_data
        )
        score_run_uuid = score_response.score_run_uuid
        test_name = score_response.test.test_name

        with self.logger.progress_bar(
            test_name,
            score_run_uuid,
            self._transform_score_status(score_response.score_run_status),
        ):
            while True:
                score_response = core_api_get_score_run.sync(
                    client=self.client, score_run_uuid=score_run_uuid
                )

                self.logger.update_progress_bar(
                    score_run_uuid,
                    self._transform_score_status(score_response.score_run_status),
                )

                if score_response.score_run_status == models.ScoreRunStatus.FAILED:
                    self.logger.error("Score run failed for %s", score_run_uuid)
                    raise ScoreRunError(f"Score run failed for {score_run_uuid}")

                if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
                    answers = self._get_all_score_run_answers(score_run_uuid)
                    return self._create_score_run_response(
                        score_response.test.test_uuid,
                        score_response.test.test_name,
                        score_response.test.n_test_questions,
                        score_run_uuid,
                        score_response.score_run_status,
                        answers,
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    self.logger.error("Score run timed out for %s", score_run_uuid)
                    raise TimeoutError("Score run timed out")

                time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_score_async(
        self, score_data: models.ScoreRunSchema
    ) -> ScoreTestResponse:
        """
        Create a score run asynchronously and wait for its completion.

        :param score_data: Prepared score data.
        :type score_data: models.ScoreRunSchema
        :return: Score test response.
        :rtype: ScoreTestResponse
        """
        start_time = time.time()
        score_response = await core_api_create_score_run.asyncio(
            client=self.client, body=score_data
        )
        score_run_uuid = score_response.score_run_uuid
        test_name = score_response.test.test_name

        with self.logger.progress_bar(
            test_name,
            score_run_uuid,
            self._transform_score_status(score_response.score_run_status),
        ):
            while True:
                score_response = await core_api_get_score_run.asyncio(
                    client=self.client, score_run_uuid=score_run_uuid
                )

                self.logger.update_progress_bar(
                    score_run_uuid,
                    self._transform_score_status(score_response.score_run_status),
                )

                if score_response.score_run_status == models.ScoreRunStatus.FAILED:
                    self.logger.error("Score run failed for %s", score_run_uuid)
                    raise ScoreRunError(f"Score run failed for {score_run_uuid}")

                if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
                    answers = await self._get_all_score_run_answers_async(
                        score_run_uuid
                    )
                    return self._create_score_run_response(
                        score_response.test.test_uuid,
                        score_response.test.test_name,
                        score_response.test.n_test_questions,
                        score_run_uuid,
                        score_response.score_run_status,
                        answers,
                    )

                elapsed_time = int(time.time() - start_time)

                if elapsed_time > self.max_wait_time:
                    self.logger.error("Score run timed out for %s", score_run_uuid)
                    raise TimeoutError("Score run timed out")

                await asyncio.sleep(POLLING_INTERVAL)

    def _get_all_score_run_answers(
        self, score_run_uuid: str
    ) -> List[models.AnswerSchema]:
        """
        Get all answers for a score run, paginating through the answers if necessary.
        """
        answers = []
        offset = 0
        while True:
            response = core_api_get_score_run_answers.sync(
                client=self.client, score_run_uuid=score_run_uuid, offset=offset
            )
            answers.extend(response.items)
            if len(answers) >= response.count:
                break
            offset += len(response.items)
        return answers

    async def _get_all_score_run_answers_async(
        self, score_run_uuid: str
    ) -> List[models.AnswerSchema]:
        """
        Get all answers for a score run asynchronously.
        """
        answers = []
        offset = 0
        while True:
            response = await core_api_get_score_run_answers.asyncio(
                client=self.client, score_run_uuid=score_run_uuid, offset=offset
            )
            answers.extend(response.items)
            if len(answers) >= response.count:
                break
            offset += len(response.items)
        return answers

    def _create_score_run_response(
        self,
        test_uuid: str,
        test_name: str,
        num_test_questions: int,
        score_run_uuid: str,
        score_run_status: models.ScoreRunStatus,
        answers: List[models.AnswerSchema] | None,
    ) -> ScoreTestResponse:
        """
        Process the score run response and return a ScoreTestResponse.

        :param score_run_response: API response for a score run.
        :type score_run_response: APIGetScoreResponse
        :return: Processed score test response.
        :rtype: ScoreTestResponse
        """
        return ScoreTestResponse(
            test_uuid=test_uuid,
            num_test_questions=num_test_questions,
            score_run_uuid=score_run_uuid,
            score_run_status=self._transform_score_status(score_run_status),
            test_name=test_name,
            answers=[self._transform_answer(answer) for answer in answers],
        )

    def _transform_score_status(
        self, api_score_status: models.ScoreRunStatus
    ) -> Status:
        """
        Transform an API score status to the user-friendly score status.

        :param api_score_status: API score run status.
        :type api_score_status: APIScoreRunStatus
        :return: Transformed score status.
        :rtype: Status
        """
        status_mapping = {
            "record_created": Status.PENDING,
            "scoring": Status.PENDING,
            "finished": Status.COMPLETED,
            "failed": Status.FAILED,
        }
        return status_mapping[api_score_status]

    def _transform_answer(
        self, api_answer: models.AnswerSchema
    ) -> ScoredAnswerResponse:
        """
        Transform an API answer to the user-friendly Answer model.

        :param test_type: Type of the test.
        :type test_type: TestType
        :param api_answer: API scored answer response.
        :type api_answer: AnswerSchema
        :return: Transformed scored answer.
        :rtype: ScoredAnswer
        """

        return ScoredAnswerResponse(
            question_uuid=api_answer.question.question_uuid,
            question_text=api_answer.question.question_text,
            answer_uuid=api_answer.answer_uuid,
            answer_text=api_answer.answer_text,
            confidence=api_answer.confidence,
            explanation=api_answer.explanation,
        )

    # Utility
    @staticmethod
    def get_pass_stats(
        score_runs: Union[List[ScoreTestResponse], ScoreTestResponse],
    ) -> pd.DataFrame:
        """
        Create a DataFrame of pass rates and pass totals from one or more score runs.

        :param score_runs: List of test score runs to graph.
        :type score_runs: List[ScoreTestResponse]
        :return: DataFrame of pass rates per score run.
        :rtype: pd.DataFrame
        """
        if isinstance(score_runs, ScoreTestResponse):
            score_runs = [score_runs]

        return pd.DataFrame(
            data={
                "test_name": [score.test_name for score in score_runs],
                "pass_rate": [score.pass_rate() for score in score_runs],
                "pass_total": [
                    score.pass_rate() * score.num_test_questions for score in score_runs
                ],
            },
            index=pd.Index(
                [score.score_run_uuid for score in score_runs], name="score_run_uuid"
            ),
        )

    @staticmethod
    def graph_pass_rates(
        score_runs: Union[List[ScoreTestResponse], ScoreTestResponse],
        title: Optional[str] = None,
        ylim_min: Optional[float] = None,
        yaxis_is_percent: bool = True,
        ylabel: str = "Answers Passed",
        xaxis_is_tests: bool = True,
        xlabel: Optional[str] = None,
        xtick_rot: float = 30.0,
        xtick_labels_dict: Optional[dict] = None,
        **kwargs,
    ) -> None:
        """
        Draw a bar graph of pass rates from one or more score runs.

        :param score_runs: List of test score runs to graph.
        :type score_runs: List[ScoreTestResponse]
        :param title: Graph title.
        :type title: str, optional
        :param ylim_min: y-axis lower limit, defaults to rounding down to the nearest decimal (yaxis_is_percent=True) or ten (yaxis_is_percent=False).
        :type ylim_min: float, optional
        :param yaxis_is_percent: Whether to show the pass rate as a percent (instead of the total number of questions passed), defaults to True.
        :type yaxis_is_percent: bool, optional
        :param ylabel: Label of the y-axis, defaults to 'Answers Passed'.
        :type ylabel: str
        :param xaxis_is_tests: Whether the x-axis represents tests (True) or score runs (False), defaults to True.
        :type xaxis_is_test: bool, optional
        :param xlabel: Label of the x-axis, defaults to 'Tests' if xaxis_is_test=True and 'Runs' if xaxis_is_test=False.
        :type xlabel: str
        :param xtick_rot: rotation of the x-axis tick labels, defaults to 30.
        :type xtick_rot: float
        :param xtick_labels_dict: Maps test_names (keys) to x-axis tick labels (values).
        :type xtick_labels_dict: dict, optional
        :param kwargs: Options to pass to matplotlib.pyplot.bar.
        """
        if isinstance(score_runs, ScoreTestResponse):
            score_runs = [score_runs]

        pass_rates = [score.pass_rate() for score in score_runs]
        names = [
            score.test_name if xaxis_is_tests else score.score_run_uuid
            for score in score_runs
        ]

        if ylim_min is None:
            ylim_min = math.floor(min(pass_rates) * 10) / 10

        fig, ax = plt.subplots()
        ax.bar(names, pass_rates, **kwargs)

        # Title
        ax.set_title(title)

        # x-axis
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=xtick_rot, ha="right")
        if xlabel is None:
            xlabel = "Tests" if xaxis_is_tests else "Score Runs"
        ax.set_xlabel(xlabel, fontweight="bold")
        if xtick_labels_dict:
            xtick_labels = [label.get_text() for label in ax.get_xticklabels()]
            new_labels = [xtick_labels_dict.get(label, label) for label in xtick_labels]
            ax.set_xticklabels(new_labels)

        # y-axis
        ax.set_ylabel(ylabel, fontweight="bold")
        if yaxis_is_percent:

            def to_percent(y, _):
                return f"{y * 100:.0f}%"

            ax.yaxis.set_major_formatter(FuncFormatter(to_percent))

        plt.tight_layout()
        plt.show()

"""
Aymara AI SDK
"""

import os
import time
import logging
import asyncio
from typing import Literal, Union, List, Optional, overload
from aymara_sdk.errors import ScoreRunError, TestCreationError
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

from aymara_sdk.types import (
    CreateScoreNoWaitResponse,
    CreateTestNoWaitResponse,
    GetTestResponse,
    CreateTestResponse,
    Question,
    ScoreTestResponse,
    ScoredJailbreakAnswer,
    ScoredSafetyAnswer,
    StudentAnswer,
)

from aymara_sdk.types import TestType, Status


logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

POLLING_INTERVAL = 2

logger = logging.getLogger("sdk")
logger.setLevel(logging.DEBUG)

# Test Creation Defaults
DEFAULT_MAX_WAIT_TIME: int = 120
DEFAULT_NUM_QUESTIONS: int = 20
DEFAULT_TEST_TYPE: TestType = TestType.SAFETY
DEFAULT_TEST_LANGUAGE: str = "en"


class AymaraAI:
    """
    Aymara AI SDK Client

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
        if api_key is None:
            api_key = os.getenv("AYMARA_API_KEY")
        if api_key is None:
            logger.error("API key is required")
            raise ValueError("API key is required")

        self.client = client.Client(base_url=base_url, headers={"x-api-key": api_key})
        self.max_wait_time = max_wait_time
        logger.info("AymaraAI client initialized with base URL: %s", base_url)

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

    @overload
    def create_test(
        self,
        test_name: str,
        student_description: str,
        test_type: TestType = DEFAULT_TEST_TYPE,
        test_policy: Optional[str] = None,
        test_system_prompt: Optional[str] = None,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
        wait_for_completion: Literal[True] = True,
    ) -> CreateTestResponse: ...

    @overload
    def create_test(
        self,
        test_name: str,
        student_description: str,
        test_type: TestType = DEFAULT_TEST_TYPE,
        test_policy: Optional[str] = None,
        test_system_prompt: Optional[str] = None,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
        wait_for_completion: Literal[False] = False,
    ) -> CreateTestNoWaitResponse: ...

    def create_test(
        self,
        test_name: str,
        student_description: str,
        test_type: TestType = DEFAULT_TEST_TYPE,
        test_policy: Optional[str] = None,
        test_system_prompt: Optional[str] = None,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
        wait_for_completion: bool = True,
    ) -> Union[CreateTestResponse, CreateTestNoWaitResponse]:
        """
        Create a test synchronously and optionally wait for completion.

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
        :param test_type: Type of the test, defaults to DEFAULT_TEST_TYPE.
        :type test_type: TestType, optional
        :param wait_for_completion: Whether to wait for the test to complete, defaults to True.
        :type wait_for_completion: bool, optional
        :return: Test response.
        :rtype: Union[CreateTestResponse, CreateTestNoWaitResponse]
        """
        test_data = self._prepare_test_data(
            test_name=test_name,
            test_policy=test_policy,
            test_system_prompt=test_system_prompt,
            student_description=student_description,
            test_language=test_language,
            n_test_questions=n_test_questions,
            test_type=test_type,
        )

        if wait_for_completion:
            logger.info("Creating test and waiting for completion: %s", test_name)
            return self._create_and_wait_for_test(test_data)
        else:
            logger.info("Creating test without waiting: %s", test_name)
            response = core_api_create_test.sync(client=self.client, body=test_data)
            return CreateTestNoWaitResponse(test_uuid=response.test_uuid)

    @overload
    async def create_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: Optional[str] = None,
        test_system_prompt: Optional[str] = None,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
        test_type: TestType = DEFAULT_TEST_TYPE,
        wait_for_completion: Literal[True] = True,
    ) -> CreateTestResponse: ...

    @overload
    async def create_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: Optional[str] = None,
        test_system_prompt: Optional[str] = None,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
        test_type: TestType = DEFAULT_TEST_TYPE,
        wait_for_completion: Literal[False] = False,
    ) -> CreateTestNoWaitResponse: ...

    async def create_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: Optional[str] = None,
        test_system_prompt: Optional[str] = None,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
        test_type: TestType = DEFAULT_TEST_TYPE,
        wait_for_completion: bool = False,
    ) -> Union[CreateTestResponse, CreateTestNoWaitResponse]:
        """
        Create a test asynchronously and optionally wait for completion.

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
        :param test_type: Type of the test, defaults to DEFAULT_TEST_TYPE.
        :type test_type: TestType, optional
        :param wait_for_completion: Whether to wait for the test to complete, defaults to False.
        :type wait_for_completion: bool, optional
        :return: Test response.
        :rtype: Union[CreateTestResponse, CreateTestNoWaitResponse]
        """
        test_data = self._prepare_test_data(
            test_name,
            test_policy,
            test_system_prompt,
            student_description,
            test_language,
            n_test_questions,
            test_type,
        )

        if wait_for_completion:
            logger.info("Creating test and waiting for completion: %s", test_name)
            return await self._create_and_wait_for_test_async(test_data)
        else:
            logger.info("Creating test asynchronously: %s", test_name)
            response = await core_api_create_test.asyncio(
                client=self.client, body=test_data
            )
            return CreateTestNoWaitResponse(test_uuid=response.test_uuid)

    def get_test(self, test_uuid: str) -> GetTestResponse:
        """
        Get the current status of a test, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: GetTestResponse
        """
        logger.info("Getting test for: %s", test_uuid)
        test_response = core_api_get_test.sync(client=self.client, test_uuid=test_uuid)
        test_status = self._transform_test_status(test_response.test_status)
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = self._get_all_questions(test_uuid)

        logger.debug("Test status for %s: %s", test_uuid, test_status.value)
        return GetTestResponse(
            test_uuid=test_uuid,
            test_name=test_response.test_name,
            test_status=test_status,
            test_type=test_response.test_type,
            questions=[
                Question.from_question_schema(question) for question in questions
            ]
            if questions
            else None,
        )

    async def get_test_async(self, test_uuid: str) -> GetTestResponse:
        """
        Get the current status of a test asynchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: GetTestResponse
        """
        logger.info("Getting test asynchronously for: %s", test_uuid)
        test_response = await core_api_get_test.asyncio(
            client=self.client, test_uuid=test_uuid
        )
        test_status = self._transform_test_status(test_response.test_status)
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = await self._get_all_questions_async(test_uuid)

        logger.debug("Test status for %s: %s", test_uuid, test_status.value)
        return GetTestResponse(
            test_uuid=test_uuid,
            test_name=test_response.test_name,
            test_status=test_status,
            test_type=test_response.test_type,
            questions=[
                Question.from_question_schema(question) for question in questions
            ]
            if questions
            else None,
        )

    def _prepare_test_data(
        self,
        test_name: str,
        test_policy: Optional[str],
        test_system_prompt: Optional[str],
        student_description: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        n_test_questions: int = DEFAULT_NUM_QUESTIONS,
        test_type: TestType = DEFAULT_TEST_TYPE,
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
        :param test_language: Language of the test, defaults to TEST_LANGUAGE.
        :type test_language: str, optional
        :param n_test_questions: Number of test questions, defaults to NUM_QUESTIONS.
        :type n_test_questions: int, optional
        :param test_type: Type of the test, defaults to TEST_TYPE.
        :type test_type: TestType, optional
        :return: Prepared test data.
        :rtype: models.TestSchema
        """
        if test_type == TestType.SAFETY and test_policy is None:
            raise ValueError("test_policy is required for safety tests")
        if test_type == TestType.JAILBREAK and test_system_prompt is None:
            raise ValueError("test_system_prompt is required for jailbreak tests")

        return models.TestSchema(
            test_name=test_name,
            test_type=test_type,
            test_language=test_language,
            n_test_questions=n_test_questions,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=test_system_prompt,
        )

    def _create_test_response(
        self,
        test_uuid: str,
        test_status: str,
        test_type: str,
        questions: List[models.QuestionSchema],
    ) -> CreateTestResponse:
        """
        Create a test response.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param test_status: Status of the test.
        :type test_status: str
        :param test_type: Type of the test.
        :type test_type: str
        :param questions: List of test questions.
        :type questions: List[models.QuestionSchema]
        :return: Created test response.
        :rtype: CreateTestResponse
        """
        return CreateTestResponse(
            test_uuid=test_uuid,
            test_status=self._transform_test_status(test_status),
            test_type=test_type,
            questions=[
                Question.from_question_schema(question) for question in questions
            ]
            if questions
            else None,
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
        """
        Create a test and wait for it to complete.

        :param test_data: Data for creating the test.
        :type test_data: models.TestSchema
        :return: Test response.
        :rtype: CreateTestResponse
        """
        start_time = time.time()
        create_response = core_api_create_test.sync(client=self.client, body=test_data)
        test_uuid = create_response.test_uuid

        while True:
            test_response = core_api_get_test.sync(
                client=self.client, test_uuid=test_uuid
            )
            logger.debug(
                "Test %s status: %s",
                test_uuid,
                self._transform_test_status(test_response.test_status).value,
            )

            if test_response.test_status == models.TestStatus.FAILED:
                logger.error("Test creation failed for %s", test_uuid)
                raise TestCreationError(f"Test creation failed for {test_uuid}")

            if test_response.test_status == models.TestStatus.FINISHED:
                logger.info("Test creation completed for %s", test_uuid)
                questions = self._get_all_questions(test_uuid)
                return self._create_test_response(
                    test_uuid,
                    test_response.test_status,
                    test_response.test_type,
                    questions,
                )

            if time.time() - start_time > self.max_wait_time:
                logger.error("Test creation timed out for %s", test_uuid)
                raise TimeoutError("Test creation timed out")

            time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_test_async(
        self, test_data: models.TestSchema
    ) -> CreateTestResponse:
        """
        Create a test asynchronously and wait for it to complete.

        :param test_data: Data for creating the test.
        :type test_data: models.TestSchema
        :return: Test response.
        :rtype: CreateTestResponse
        """
        start_time = asyncio.get_event_loop().time()
        create_response = await core_api_create_test.asyncio(
            client=self.client, body=test_data
        )
        test_uuid = create_response.test_uuid

        while True:
            test_response = await core_api_get_test.asyncio(
                client=self.client, test_uuid=test_uuid
            )
            logger.debug(
                "Test %s status: %s",
                test_uuid,
                self._transform_test_status(test_response.test_status).value,
            )

            if test_response.test_status == "failed":
                logger.error("Test creation failed for %s", test_uuid)
                raise TestCreationError(f"Test creation failed for {test_uuid}")

            if test_response.test_status == "finished":
                logger.info("Test creation completed for %s", test_uuid)
                questions = await core_api_get_test_questions.asyncio(
                    client=self.client, test_uuid=test_uuid
                )
                return self._create_test_response(
                    test_uuid,
                    test_response.test_status,
                    test_response.test_type,
                    questions,
                )

            if asyncio.get_event_loop().time() - start_time > self.max_wait_time:
                logger.error("Test creation timed out for %s", test_uuid)
                raise TimeoutError("Test creation timed out")

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

    @overload
    def score_test(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
        wait_for_completion: Literal[True] = True,
    ) -> ScoreTestResponse: ...

    @overload
    def score_test(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
        wait_for_completion: Literal[False] = False,
    ) -> CreateScoreNoWaitResponse: ...

    def score_test(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
        wait_for_completion: bool = True,
    ) -> Union[ScoreTestResponse, CreateScoreNoWaitResponse]:
        """
        Score a test synchronously and optionally wait for completion.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of StudentAnswer objects containing student responses.
        :type student_answers: List[StudentAnswer]
        :param wait_for_completion: Whether to wait for the score to complete, defaults to True.
        :type wait_for_completion: bool, optional
        :return: Score response.
        :rtype: Union[ScoreTestResponse, CreateScoreNoWaitResponse]
        """
        logger.info("Scoring test: %s", test_uuid)
        score_data = self._prepare_score_data(test_uuid, student_answers)

        if wait_for_completion:
            logger.info("Scoring test and waiting for completion: %s", test_uuid)
            score_response = self._create_and_wait_for_score(score_data)
        else:
            logger.info("Creating score run without waiting: test_uuid=%s", test_uuid)
            response = core_api_create_score_run.sync(
                client=self.client, body=score_data
            )
            score_response = CreateScoreNoWaitResponse(
                score_run_uuid=response.score_run_uuid
            )

        logger.info("Score run created: %s", score_response.score_run_uuid)
        return score_response

    @overload
    async def score_test_async(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
        wait_for_completion: Literal[True],
    ) -> ScoreTestResponse: ...

    @overload
    async def score_test_async(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
        wait_for_completion: Literal[False] = False,
    ) -> CreateScoreNoWaitResponse: ...

    async def score_test_async(
        self,
        test_uuid: str,
        student_answers: List[StudentAnswer],
        wait_for_completion: bool = True,
    ) -> Union[ScoreTestResponse, CreateScoreNoWaitResponse]:
        """
        Score a test asynchronously and optionally wait for completion.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :param student_answers: List of StudentAnswer objects containing student responses.
        :type student_answers: List[StudentAnswer]
        :param wait_for_completion: Whether to wait for the score to complete, defaults to True.
        :type wait_for_completion: bool, optional
        :return: Score response.
        :rtype: Union[ScoreTestResponse, CreateScoreNoWaitResponse]
        """
        logger.info("Scoring test asynchronously: %s", test_uuid)
        score_data = self._prepare_score_data(test_uuid, student_answers)

        if wait_for_completion:
            logger.info("Scoring test and waiting for completion: %s", test_uuid)
            score_response = await self._create_and_wait_for_score_async(score_data)
        else:
            logger.info("Creating score run asynchronously: %s", test_uuid)
            response = await core_api_create_score_run.asyncio(
                client=self.client, body=score_data
            )
            score_response = CreateScoreNoWaitResponse(
                score_run_uuid=response.score_run_uuid
            )

        logger.info(
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
        logger.info("Getting score run for: %s", score_run_uuid)
        score_run_response = core_api_get_score_run.sync(
            client=self.client, score_run_uuid=score_run_uuid
        )
        answers = None
        if score_run_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = self._get_all_score_run_answers(score_run_uuid)
        return self._create_score_run_response(
            score_run_response.test.test_uuid,
            score_run_response.test.test_type,
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
        logger.info("Getting score run asynchronously for: %s", score_run_uuid)
        score_run_response = await core_api_get_score_run.asyncio(
            client=self.client, score_run_uuid=score_run_uuid
        )
        answers = None
        if score_run_response.score_run_status == models.ScoreRunStatus.FINISHED:
            answers = await self._get_all_score_run_answers_async(score_run_uuid)
        return self._create_score_run_response(
            score_run_response.test.test_uuid,
            score_run_response.test.test_type,
            score_run_uuid,
            score_run_response.score_run_status,
            answers,
        )

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

        while True:
            score_response = core_api_get_score_run.sync(
                client=self.client, score_run_uuid=score_run_uuid
            )
            logger.debug(
                "Score run %s status: %s",
                score_run_uuid,
                self._transform_score_status(score_response.score_run_status).value,
            )

            if score_response.score_run_status == models.ScoreRunStatus.FAILED:
                logger.error("Score run failed for %s", score_run_uuid)
                raise ScoreRunError(f"Score run failed for {score_run_uuid}")

            if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
                answers = self._get_all_score_run_answers(score_run_uuid)
                logger.info(
                    "Score run completed with %s, answers: %s",
                    score_response.test.test_type,
                    answers,
                )
                return self._create_score_run_response(
                    score_response.test.test_uuid,
                    score_response.test.test_type,
                    score_run_uuid,
                    score_response.score_run_status,
                    answers,
                )
            if time.time() - start_time > self.max_wait_time:
                logger.error("Score run timed out for %s", score_run_uuid)
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
        start_time = asyncio.get_event_loop().time()
        score_response = await core_api_create_score_run.asyncio(
            client=self.client, body=score_data
        )
        score_run_uuid = score_response.score_run_uuid

        while True:
            score_response = await core_api_get_score_run.asyncio(
                client=self.client, score_run_uuid=score_run_uuid
            )
            logger.debug(
                "Score run %s status: %s",
                score_run_uuid,
                self._transform_score_status(score_response.score_run_status).value,
            )

            if score_response.score_run_status == models.ScoreRunStatus.FAILED:
                logger.error("Score run failed for %s", score_run_uuid)
                raise ScoreRunError(f"Score run failed for {score_run_uuid}")

            if score_response.score_run_status == models.ScoreRunStatus.FINISHED:
                answers = await self._get_all_score_run_answers_async(score_run_uuid)
                logger.info("Score run completed with %s", score_response)
                return self._create_score_run_response(
                    score_response.test.test_uuid,
                    score_response.test.test_type,
                    score_run_uuid,
                    score_response.score_run_status,
                    answers,
                )
            if asyncio.get_event_loop().time() - start_time > self.max_wait_time:
                logger.error("Score run timed out for %s", score_run_uuid)
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
        test_type: models.TestType,
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
            score_run_uuid=score_run_uuid,
            score_run_status=self._transform_score_status(score_run_status),
            answers=[self._transform_answer(test_type, answer) for answer in answers]
            if answers
            else None,
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

    @overload
    def _transform_answer(
        self,
        test_type: Literal[models.TestType.SAFETY],
        api_answer: models.AnswerSchema,
    ) -> ScoredSafetyAnswer: ...

    @overload
    def _transform_answer(
        self,
        test_type: Literal[models.TestType.JAILBREAK],
        api_answer: models.AnswerSchema,
    ) -> ScoredJailbreakAnswer: ...

    def _transform_answer(
        self, test_type: models.TestType, api_answer: models.AnswerSchema
    ) -> Union[ScoredSafetyAnswer, ScoredJailbreakAnswer]:
        """
        Transform an API answer to the user-friendly Answer model.

        :param test_type: Type of the test.
        :type test_type: TestType
        :param api_answer: API scored answer response.
        :type api_answer: AnswerSchema
        :return: Transformed scored answer.
        :rtype: Union[ScoredSafetyAnswer, ScoredJailbreakAnswer]
        """
        logger.debug("Transforming answer for test type: %s", test_type)
        if not isinstance(test_type, TestType):
            logger.warning(
                "Unexpected test_type: %s is not of type TestType", type(test_type)
            )
        if test_type == TestType.SAFETY:
            return ScoredSafetyAnswer(
                question_uuid=api_answer.question.question_uuid,
                question_text=api_answer.question.question_text,
                answer_uuid=api_answer.answer_uuid,
                answer_text=api_answer.answer_text,
                is_safe=api_answer.is_safe,
                confidence=api_answer.confidence,
                explanation=api_answer.explanation,
            )
        elif test_type == TestType.JAILBREAK:
            return ScoredJailbreakAnswer(
                question_uuid=api_answer.question.question_uuid,
                question_text=api_answer.question.question_text,
                answer_uuid=api_answer.answer_uuid,
                answer_text=api_answer.answer_text,
                is_follow=api_answer.is_follow,
                instruction_unfollowed=api_answer.instruction_unfollowed,
                explanation=api_answer.explanation,
            )
        else:
            raise ValueError(f"Unsupported test type: {test_type}")

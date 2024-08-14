"""
Aymara AI SDK
"""
import os
import time
import logging
import uuid
import json
import asyncio
from typing import Literal, Union, List
from sdk.api.tests import TestsAPI
from sdk.api.scores import ScoresAPI
from sdk.errors import ScoreRunError, TestCreationError
from sdk.types import CreateScoreAsyncResponse, CreateTestAsyncResponse, GetTestResponse, CreateTestResponse, Question, ScoreTestResponse, ScoredAnswer
from sdk._internal_types import APIMakeTestRequest, APIAnswerRequest, APITestQuestionResponse, APIMakeScoreRequest, APIScoredAnswerResponse
from .http_client import HTTPClient


MAX_WAIT_TIME = 60
POLLING_INTERVAL = 2
WRITER_MODEL_NAME = "gpt-4o-mini"
SCORE_MODEL_NAME = "gpt-4o-mini"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger("sdk")
logger.setLevel(logging.DEBUG)

# Test Creation Defaults
NUM_QUESTIONS = 20
TEST_TYPE = "safety"
TEST_LANGUAGE = "en"


class AymaraAI:
    """
    Aymara AI SDK Client

    :param api_key: API key for authenticating with the Aymara AI API.
    :type api_key: str, optional
    :param base_url: Base URL for the Aymara AI API, defaults to "https://api.aymara.ai".
    :type base_url: str, optional
    """

    def __init__(self, api_key: str | None = None,
                 base_url: str = "https://api.aymara.ai"):
        if api_key is None:
            api_key = os.getenv("AYMARA_API_KEY")
        if api_key is None:
            logger.error("API key is required")
            raise ValueError("API key is required")

        self.http_client = HTTPClient(base_url, api_key)
        self.tests = TestsAPI(self.http_client)
        self.scores = ScoresAPI(self.http_client)
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
        self.http_client.close()

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
        await self.http_client.aclose()

    # ----------------
    # Tests
    # ----------------
    def _prepare_test_data(self, test_name: str, test_policy: str, student_description: str,
                           test_language: str = TEST_LANGUAGE, n_test_questions: int = NUM_QUESTIONS,
                           test_type: Literal['safety', 'hallucination', 'jailbreak'] = TEST_TYPE) -> APIMakeTestRequest:
        """
        Prepare the test data for creating a test.

        :param test_name: Name of the test.
        :type test_name: str
        :param test_policy: Policy for the test.
        :type test_policy: str
        :param student_description: Description of the student.
        :type student_description: str
        :param test_language: Language of the test, defaults to TEST_LANGUAGE.
        :type test_language: str, optional
        :param n_test_questions: Number of test questions, defaults to NUM_QUESTIONS.
        :type n_test_questions: int, optional
        :param test_type: Type of the test, defaults to TEST_TYPE.
        :type test_type: Literal['safety', 'hallucination', 'jailbreak'], optional
        :return: Prepared test data.
        :rtype: APIMakeTestRequest
        """
        return APIMakeTestRequest(
            test_name=test_name,
            test_type=test_type,
            test_language=test_language,
            n_test_questions=n_test_questions,
            student_description=student_description,
            test_policy=test_policy,
            writer_model_name=WRITER_MODEL_NAME,
        )

    def _create_test_response(self, test_uuid: uuid.UUID, test_status: str, test_type: str, questions: List[APITestQuestionResponse]) -> CreateTestResponse:
        """
        Create a test response.

        :param test_uuid: UUID of the test.
        :type test_uuid: uuid.UUID
        :param test_status: Status of the test.
        :type test_status: str
        :param test_type: Type of the test.
        :type test_type: str
        :param questions: List of test questions.
        :type questions: List[APITestQuestionResponse]
        :return: Created test response.
        :rtype: CreateTestResponse
        """
        return CreateTestResponse(
            test_uuid=test_uuid,
            test_status=self._transform_test_status(test_status),
            test_type=test_type,
            questions=[self._transform_question(
                question) for question in questions]
        )

    def create_test(self,
                    test_name: str,
                    test_policy: str,
                    student_description: str,
                    test_language: str = TEST_LANGUAGE,
                    n_test_questions: int = NUM_QUESTIONS,
                    test_type: Literal['safety',
                                       'hallucination', 'jailbreak'] = TEST_TYPE,
                    wait_for_completion: bool = True) -> Union[CreateTestResponse, CreateTestAsyncResponse]:
        """
        Create a test synchronously and optionally wait for completion.

        :param test_name: Name of the test.
        :type test_name: str
        :param test_policy: Policy for the test.
        :type test_policy: str
        :param student_description: Description of the student.
        :type student_description: str
        :param test_language: Language of the test, defaults to TEST_LANGUAGE.
        :type test_language: str, optional
        :param n_test_questions: Number of test questions, defaults to NUM_QUESTIONS.
        :type n_test_questions: int, optional
        :param test_type: Type of the test, defaults to TEST_TYPE.
        :type test_type: Literal['safety', 'hallucination', 'jailbreak'], optional
        :param wait_for_completion: Whether to wait for the test to complete, defaults to True.
        :type wait_for_completion: bool, optional
        :return: Test response.
        :rtype: Union[CreateTestResponse, CreateTestAsyncResponse]
        """
        test_data = self._prepare_test_data(
            test_name, test_policy, student_description, test_language, n_test_questions, test_type)

        if wait_for_completion:
            logger.info(
                "Creating test and waiting for completion: %s", test_name)
            return self._create_and_wait_for_test(test_data)
        else:
            logger.info("Creating test without waiting: %s", test_name)
            response = self.tests.create(test_data)
            return CreateTestAsyncResponse(test_uuid=response.test_uuid)

    async def create_test_async(self,
                                test_name: str,
                                test_policy: str,
                                student_description: str,
                                test_language: str = TEST_LANGUAGE,
                                n_test_questions: int = NUM_QUESTIONS,
                                test_type: Literal['safety',
                                                   'hallucination', 'jailbreak'] = TEST_TYPE,
                                wait_for_completion: bool = False) -> Union[CreateTestResponse, CreateTestAsyncResponse]:
        """
        Create a test asynchronously and optionally wait for completion.

        :param test_name: Name of the test.
        :type test_name: str
        :param test_policy: Policy for the test.
        :type test_policy: str
        :param student_description: Description of the student.
        :type student_description: str
        :param test_language: Language of the test, defaults to TEST_LANGUAGE.
        :type test_language: str, optional
        :param n_test_questions: Number of test questions, defaults to NUM_QUESTIONS.
        :type n_test_questions: int, optional
        :param test_type: Type of the test, defaults to TEST_TYPE.
        :type test_type: Literal['safety', 'hallucination', 'jailbreak'], optional
        :param wait_for_completion: Whether to wait for the test to complete, defaults to False.
        :type wait_for_completion: bool, optional
        :return: Test response.
        :rtype: Union[CreateTestResponse, CreateTestAsyncResponse]
        """
        test_data = self._prepare_test_data(
            test_name, test_policy, student_description, test_language, n_test_questions, test_type)

        if wait_for_completion:
            logger.info(
                "Creating test and waiting for completion: %s", test_name)
            return await self._create_and_wait_for_test_async(test_data)
        else:
            logger.info("Creating test asynchronously: %s", test_name)
            response = await self.tests.async_create(test_data)
            return CreateTestAsyncResponse(test_uuid=response.test_uuid)

    def get_test(self, test_uuid: uuid.UUID) -> GetTestResponse:
        """
        Get the current status of a test, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: uuid.UUID
        :return: Test response.
        :rtype: GetTestResponse
        """
        logger.info("Getting test for: %s", test_uuid)
        test_response = self.tests.get(test_uuid)
        test_status = self._transform_test_status(test_response.test_status)
        questions = None
        if test_response.test_status == "finished":
            questions = [self._transform_question(
                q) for q in self.tests.get_all_questions(test_uuid)]

        logger.debug("Test status for %s: %s", test_uuid, test_status)
        return GetTestResponse(
            test_uuid=test_uuid,
            test_name=test_response.test_name,
            test_status=test_status,
            test_type=test_response.test_type,
            questions=questions
        )

    async def get_test_async(self, test_uuid: uuid.UUID) -> GetTestResponse:
        """
        Get the current status of a test asynchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: uuid.UUID
        :return: Test response.
        :rtype: GetTestResponse
        """
        logger.info("Getting test asynchronously for: %s", test_uuid)
        test_response = await self.tests.async_get(test_uuid)
        test_status = self._transform_test_status(test_response.test_status)
        questions = None
        if test_response.test_status == "finished":
            questions = [self._transform_question(
                q) for q in await self.tests.async_get_all_questions(test_uuid)]

        logger.debug("Test status for %s: %s", test_uuid, test_status)
        return GetTestResponse(
            test_uuid=test_uuid,
            test_name=test_response.test_name,
            test_status=test_status,
            test_type=test_response.test_type,
            questions=questions
        )

    def _create_and_wait_for_test(self, test_data: APIMakeTestRequest) -> CreateTestResponse:
        """
        Create a test and wait for it to complete.

        :param test_data: Data for creating the test.
        :type test_data: APIMakeTestRequest
        :return: Test response.
        :rtype: CreateTestResponse
        """
        create_response = self.tests.create(test_data)
        test_uuid = create_response.test_uuid
        logger.info("Test creation initiated: %s", test_uuid)

        start_time = time.time()
        while True:
            test_response = self.tests.get(test_uuid)
            logger.debug("Test %s status: %s", test_uuid,
                         self._transform_test_status(test_response.test_status))

            if test_response.test_status == "failed":
                logger.error("Test creation failed for %s", test_uuid)
                raise TestCreationError(
                    f"Test creation failed for {test_uuid}")

            if test_response.test_status == "finished":
                logger.info("Test creation completed for %s", test_uuid)
                questions = self.tests.get_all_questions(test_uuid)
                return self._create_test_response(test_uuid, test_response.test_status, test_response.test_type, questions)

            if time.time() - start_time > MAX_WAIT_TIME:
                logger.error("Test creation timed out for %s", test_uuid)
                raise TimeoutError("Test creation timed out")

            time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_test_async(self, test_data: APIMakeTestRequest) -> CreateTestResponse:
        """
        Create a test asynchronously and wait for it to complete.

        :param test_data: Data for creating the test.
        :type test_data: APIMakeTestRequest
        :return: Test response.
        :rtype: CreateTestResponse
        """
        create_response = await self.tests.async_create(test_data)
        test_uuid = create_response.test_uuid
        logger.info("Test creation initiated asynchronously: %s", test_uuid)

        start_time = asyncio.get_event_loop().time()
        while True:
            test_response = await self.tests.async_get(test_uuid)
            logger.debug("Test %s status: %s", test_uuid,
                         self._transform_test_status(test_response.test_status))

            if test_response.test_status == "failed":
                logger.error("Test creation failed for %s", test_uuid)
                raise TestCreationError(
                    f"Test creation failed for {test_uuid}")

            if test_response.test_status == "finished":
                logger.info("Test creation completed for %s", test_uuid)
                questions = await self.tests.async_get_all_questions(test_uuid)
                return self._create_test_response(test_uuid, test_response.test_status, test_response.test_type, questions)

            if asyncio.get_event_loop().time() - start_time > MAX_WAIT_TIME:
                logger.error("Test creation timed out for %s", test_uuid)
                raise TimeoutError("Test creation timed out")

            await asyncio.sleep(POLLING_INTERVAL)

    def _transform_question(self, api_question: APITestQuestionResponse) -> Question:
        """
        Transform an API question to the user-friendly Question model.

        :param api_question: API question response.
        :type api_question: APITestQuestionResponse
        :return: Transformed question.
        :rtype: Question
        """
        return Question(
            question_uuid=api_question.question_uuid,
            question_text=api_question.question_text,
        )

    def _transform_test_status(self, api_test_status: Literal['record_created', 'scoring', 'finished', 'failed']) -> Literal['pending', 'completed', 'failed']:
        """
        Transform an API test status to the user-friendly test status.

        :param api_test_status: API test status.
        :type api_test_status: Literal['record_created', 'scoring', 'finished', 'failed']
        :return: Transformed test status.
        :rtype: Literal['pending', 'completed', 'failed']
        """
        status_mapping = {
            'record_created': 'pending',
            'generating_questions': 'pending',
            'finished': 'completed',
            'failed': 'failed'
        }
        return status_mapping[api_test_status]

    # ----------------
    # Scores
    # ----------------

    def score_test(self, test_uuid: uuid.UUID, student_response_json: str, wait_for_completion: bool = True, overwrite_questions: bool = False) -> Union[ScoreTestResponse, CreateScoreAsyncResponse]:
        """
        Score a test synchronously and optionally wait for completion.

        :param test_uuid: UUID of the test.
        :type test_uuid: uuid.UUID
        :param student_response_json: JSON string of student responses.
        :type student_response_json: str
        :param wait_for_completion: Whether to wait for the score to complete, defaults to True.
        :type wait_for_completion: bool, optional
        :return: Score response.
        :rtype: Union[ScoreTestResponse, CreateScoreAsyncResponse]
        """
        logger.info("Scoring test: %s", test_uuid)
        score_data = self._prepare_score_data(
            test_uuid, student_response_json, overwrite_questions)

        if wait_for_completion:
            logger.info(
                "Scoring test and waiting for completion: %s", test_uuid)
            score_response = self._create_and_wait_for_score(score_data)
        else:
            logger.info("Creating score run without waiting: %s", test_uuid)
            response = self.scores.create(score_data)
            score_response = CreateScoreAsyncResponse(
                score_run_uuid=response.score_run_uuid)

        logger.info("Score run created: %s", score_response.score_run_uuid)
        return score_response

    async def score_test_async(self, test_uuid: uuid.UUID, student_response_json: str, wait_for_completion: bool = False, overwrite_questions: bool = False) -> Union[ScoreTestResponse, CreateScoreAsyncResponse]:
        """
        Score a test asynchronously and optionally wait for completion.

        :param test_uuid: UUID of the test.
        :type test_uuid: uuid.UUID
        :param student_response_json: JSON string of student responses.
        :type student_response_json: str
        :param wait_for_completion: Whether to wait for the score to complete, defaults to False.
        :type wait_for_completion: bool, optional
        :return: Score response.
        :rtype: Union[ScoreTestResponse, CreateScoreAsyncResponse]
        :param overwrite_questions: Whether to overwrite the questions, defaults to False. Should only be used for testing purposes.
        :type overwrite_questions: bool, optional
        """
        logger.info("Scoring test asynchronously: %s", test_uuid)
        score_data = self._prepare_score_data(
            test_uuid, student_response_json, overwrite_questions)

        if wait_for_completion:
            logger.info(
                "Scoring test and waiting for completion: %s", test_uuid)
            score_response = await self._create_and_wait_for_score_async(score_data)
        else:
            logger.info("Creating score run asynchronously: %s", test_uuid)
            response = await self.scores.async_create(score_data)
            score_response = CreateScoreAsyncResponse(
                score_run_uuid=response.score_run_uuid)

        logger.info("Score run created asynchronously: %s",
                    score_response.score_run_uuid)
        return score_response

    def get_score_run(self, score_run_uuid: uuid.UUID) -> ScoreTestResponse:
        """
        Get the current status of a score run, and answers with scores if it is completed.
        """
        logger.info("Getting score run for: %s", score_run_uuid)
        score_run_response = self.scores.get(score_run_uuid)
        scores = None
        if score_run_response.score_run_status == "finished":
            scores = self.scores.get_all_scores(score_run_uuid)
        return self._process_score_run_response(score_run_response, scores)

    async def get_score_run_async(self, score_run_uuid: uuid.UUID) -> ScoreTestResponse:
        """
        Get the current status of a score run asynchronously, and answers with scores if it is completed.
        """
        logger.info("Getting score run asynchronously for: %s", score_run_uuid)
        score_run_response = await self.scores.async_get(score_run_uuid)
        scores = None
        if score_run_response.score_run_status == "finished":
            scores = await self.scores.async_get_all_scores(score_run_uuid)
        return self._process_score_run_response(score_run_response, scores)

    def _prepare_score_data(self, test_uuid: uuid.UUID, student_response_json: str, overwrite_questions: bool = False) -> APIMakeScoreRequest:
        try:
            student_responses = json.loads(student_response_json)
            validated_responses = [APIAnswerRequest(
                **response) for response in student_responses]
        except json.JSONDecodeError as json_error:
            raise ValueError(
                "Invalid JSON format for student responses") from json_error

        if not validated_responses:
            raise ValueError("At least one student response must be provided")

        return APIMakeScoreRequest(
            test_uuid=test_uuid,
            score_run_model=SCORE_MODEL_NAME,
            answers=validated_responses,
            overwrite_questions=overwrite_questions
        )

    def _create_and_wait_for_score(self, score_data: APIMakeScoreRequest) -> ScoreTestResponse:
        score_response = self.scores.create(score_data)
        score_run_uuid = score_response.score_run_uuid
        logger.info("Score run initiated: %s", score_run_uuid)

        start_time = time.time()
        while True:
            score_response = self.scores.get(score_run_uuid)
            logger.debug("Score run %s status: %s", score_run_uuid,
                         self._transform_score_status(score_response.score_run_status))

            if score_response.score_run_status == "failed":
                logger.error("Score run failed for %s", score_run_uuid)
                raise ScoreRunError(f"Score run failed for {score_run_uuid}")

            if score_response.score_run_status == "finished":
                scores = self.scores.get_all_scores(score_run_uuid)
                return self._process_score_run_response(score_response, scores)

            if time.time() - start_time > MAX_WAIT_TIME:
                logger.error("Score run timed out for %s", score_run_uuid)
                raise TimeoutError("Score run timed out")

            time.sleep(POLLING_INTERVAL)

    async def _create_and_wait_for_score_async(self, score_data: APIMakeScoreRequest) -> ScoreTestResponse:
        score_response = await self.scores.async_create(score_data)
        score_run_uuid = score_response.score_run_uuid
        logger.info("Score run initiated: %s", score_run_uuid)

        start_time = asyncio.get_event_loop().time()
        while True:
            score_response = await self.scores.async_get(score_run_uuid)
            logger.debug("Score run %s status: %s", score_run_uuid,
                         self._transform_score_status(score_response.score_run_status))

            if score_response.score_run_status == "failed":
                logger.error("Score run failed for %s", score_run_uuid)
                raise ScoreRunError(f"Score run failed for {score_run_uuid}")

            if score_response.score_run_status == "finished":
                scores = await self.scores.async_get_all_scores(score_run_uuid)
                return self._process_score_run_response(score_response, scores)

            if asyncio.get_event_loop().time() - start_time > MAX_WAIT_TIME:
                logger.error("Score run timed out for %s", score_run_uuid)
                raise TimeoutError("Score run timed out")

            await asyncio.sleep(POLLING_INTERVAL)

    def _process_score_run_response(self, score_run_response, scores=None) -> ScoreTestResponse:
        score_run_status = self._transform_score_status(
            score_run_response.score_run_status)
        answers = None
        if score_run_response.score_run_status == "finished":
            answers = [self._transform_answer(answer)
                       for answer in (scores or [])]

        logger.debug("Score run status for %s: %s",
                     score_run_response.score_run_uuid, score_run_status)
        return ScoreTestResponse(
            test_uuid=score_run_response.test_uuid,
            score_run_uuid=score_run_response.score_run_uuid,
            score_run_status=score_run_status,
            answers=answers
        )

    def _transform_score_status(self, api_score_status: Literal['record_created', 'generating_scores', 'finished', 'failed']) -> Literal['pending', 'completed', 'failed']:
        """
        Transform an API score status to the user-friendly score status.
        """
        status_mapping = {
            'record_created': 'pending',
            'scoring': 'pending',
            'finished': 'completed',
            'failed': 'failed'
        }
        return status_mapping[api_score_status]

    def _transform_answer(self, api_answer: APIScoredAnswerResponse) -> ScoredAnswer:
        """
        Transform an API answer to the user-friendly Answer model.
        """
        return ScoredAnswer(
            question_uuid=api_answer.question_uuid,
            question_text=api_answer.question_text,
            answer_uuid=api_answer.answer_uuid,
            answer_text=api_answer.answer_text,
            is_safe=api_answer.is_safe,
            confidence=api_answer.confidence,
            explanation=api_answer.explanation
        )

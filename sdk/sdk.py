"""
Aymara AI SDK
"""
import os
import time
import logging
import uuid
import json
from typing import Literal
from sdk.api.tests import TestsAPI
from sdk.api.scores import ScoresAPI
from sdk.errors import ScoreRunError, TestCreationError
from sdk.types import CreateTestAsyncResponse, GetTestResponse, MakeTestParams, CreateTestResponse, Question, ScoreTestResponse, ScoredAnswer
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
    """

    def __init__(self, api_key: str | None = None,
                 base_url: str = "https://api.aymara.ai"):
        if api_key is None:
            api_key = os.getenv("AYMARA_API_KEY")
        if api_key is None:
            logger.error("API key is not set")
            raise ValueError("API key is not set")

        self.http_client = HTTPClient(base_url, api_key)
        self.tests = TestsAPI(self.http_client)
        self.scores = ScoresAPI(self.http_client)
        logger.info("AymaraAI client initialized with base URL: %s", base_url)

    # ----------------
    # Tests
    # ----------------

    def create_test(self,
                    test_name: str,
                    test_policy: str,
                    student_description: str,
                    test_language: str = TEST_LANGUAGE,
                    n_test_questions: int = NUM_QUESTIONS,
                    test_type: Literal['safety',
                                       'hallucination', 'jailbreak'] = TEST_TYPE
                    ) -> CreateTestResponse:
        """
        Create a test synchronously and wait for completion.
        """
        test_data = MakeTestParams(test_name=test_name, test_type=test_type, test_language=test_language,
                                   student_description=student_description, test_policy=test_policy,
                                   n_test_questions=n_test_questions)
        logger.info("Creating test synchronously: %s", test_data.test_name)
        test_response = self._create_and_wait_for_test(test_data)
        logger.info("Test created successfully: %s", test_response.test_uuid)

        return test_response

    def create_test_async(self,
                          test_name: str,
                          test_policy: str,
                          student_description: str,
                          test_language: str = TEST_LANGUAGE,
                          n_test_questions: int = NUM_QUESTIONS,
                          test_type: Literal['safety',
                                             'hallucination', 'jailbreak'] = TEST_TYPE,) -> CreateTestAsyncResponse:
        """
        Create a test asynchronously.
        """
        logger.info("Creating test asynchronously: %s", test_name)
        create_test_payload = APIMakeTestRequest(
            test_name=test_name,
            test_type=test_type,
            test_language=test_language,
            n_test_questions=n_test_questions,
            student_description=student_description,
            test_policy=test_policy,
            writer_model_name=WRITER_MODEL_NAME,
        )

        response = self.tests.create(create_test_payload)
        logger.info("Test created asynchronously: %s", response.test_uuid)
        return CreateTestAsyncResponse(test_uuid=response.test_uuid)

    def get_test(self, test_uuid: uuid.UUID) -> GetTestResponse:
        """
        Get the current status of a test, and questions if it is completed.
        """
        logger.info("Getting test for: %s", test_uuid)
        test_response = self.tests.get(test_uuid)
        test_status = self._transform_test_status(test_response.test_status)
        if test_response.test_status == "finished":
            questions = self.tests.get_all_questions(test_uuid)
            questions = [self._transform_question(
                question) for question in questions]

        logger.info("Test status for %s: %s", test_uuid, test_status)
        return GetTestResponse(
            test_uuid=test_uuid,
            test_name=test_response.test_name,
            test_status=test_status,
            test_type=test_response.test_type,
            questions=questions if test_status == "completed" else None
        )

    def _create_and_wait_for_test(self, test_data: MakeTestParams) -> CreateTestResponse:
        create_test_payload = APIMakeTestRequest(
            test_name=test_data.test_name,
            test_type=test_data.test_type,
            test_language=test_data.test_language,
            n_test_questions=test_data.n_test_questions,
            student_description=test_data.student_description,
            test_policy=test_data.test_policy,
            writer_model_name=WRITER_MODEL_NAME,
        )

        create_response = self.tests.create(create_test_payload)
        test_uuid = create_response.test_uuid
        logger.info("Test creation initiated: %s", test_uuid)

        start_time = time.time()
        while True:
            test_response = self.tests.get(test_uuid)
            logger.debug("Test %s status: %s", test_uuid,
                         test_response.test_status)

            if test_response.test_status == "failed":
                logger.error("Test creation failed for %s", test_uuid)
                raise TestCreationError(
                    f"Test creation failed for {test_uuid}")

            if test_response.test_status == "finished":
                logger.info("Test creation completed for %s", test_uuid)
                questions = self.tests.get_all_questions(test_uuid)
                return CreateTestResponse(
                    test_uuid=test_uuid,
                    test_status=self._transform_test_status(
                        test_response.test_status),
                    test_type=test_response.test_type,
                    questions=[self._transform_question(
                        question) for question in questions]
                )

            if time.time() - start_time > MAX_WAIT_TIME:
                logger.error("Test creation timed out for %s", test_uuid)
                raise TimeoutError("Test creation timed out")

            time.sleep(POLLING_INTERVAL)

    def _transform_question(self, api_question: APITestQuestionResponse) -> Question:
        """
        Transform an API question to the user-friendly Question model.
        """
        return Question(
            question_uuid=api_question.question_uuid,
            question_text=api_question.question_text,
        )

    def _transform_test_status(self, api_test_status: Literal['record_created', 'scoring', 'finished', 'failed']) -> Literal['pending', 'completed', 'failed']:
        """
        Transform an API test status to the user-friendly test status.
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

    def score_test(self, test_uuid: uuid.UUID, student_response_json: str) -> ScoreTestResponse:
        """
        Score a test
        """

        logger.info("Scoring test synchronously: %s", test_uuid)
        # Validate the student response JSON is in the correct format
        try:
            student_responses = json.loads(student_response_json)
            validated_responses = [APIAnswerRequest(
                **response) for response in student_responses]
        except json.JSONDecodeError as json_error:
            raise ValueError(
                "Invalid JSON format for student responses") from json_error

        # Ensure at least one response is provided
        if not validated_responses:
            raise ValueError("At least one student response must be provided")

        score_test_payload = APIMakeScoreRequest(
            test_uuid=test_uuid,
            score_run_model=SCORE_MODEL_NAME,
            answers=validated_responses
        )

        score_response = self.scores.create(score_test_payload)
        logger.info("Score run initiated: %s", score_response.score_run_uuid)
        start_time = time.time()
        while True:
            score_response = self.scores.get(score_response.score_run_uuid)
            logger.debug("Score run %s status: %s", score_response.score_run_uuid,
                         score_response.score_run_status)

            if score_response.score_run_status == "failed":
                logger.error("Score run failed for %s",
                             score_response.score_run_uuid)
                raise ScoreRunError(
                    f"Score run failed for {score_response.score_run_uuid}")

            if score_response.score_run_status == "finished":
                answers = self.scores.get_all_scores(
                    score_response.score_run_uuid)
                answers = [self._transform_answer(
                    answer) for answer in answers]
                logger.info("Score run completed for %s",
                            score_response.score_run_uuid)

                return ScoreTestResponse(
                    test_uuid=test_uuid,
                    score_run_uuid=score_response.score_run_uuid,
                    score_run_status=self._transform_score_status(
                        score_response.score_run_status),
                    answers=answers
                )

            if time.time() - start_time > MAX_WAIT_TIME:
                logger.error("Score run timed out for %s",
                             score_response.score_run_uuid)
                raise TimeoutError("Score run timed out")

            time.sleep(POLLING_INTERVAL)

    def _transform_score_status(self, api_score_status: Literal['record_created',
                                                                'generating_scores', 'finished', 'failed']) -> Literal['pending', 'completed', 'failed']:
        """
        Transform an API score status to the user-friendly score status.
        """
        status_mapping = {
            'record_created': 'pending',
            'generating_scores': 'pending',
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

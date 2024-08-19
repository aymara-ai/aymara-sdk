import pytest
import time
import asyncio
import logging
import os
from examples.demo_student import OpenAIStudent

from aymara_ai.sdk import AymaraAI
from aymara_ai.types import CreateScoreAsyncResponse, CreateTestAsyncResponse, GetTestResponse, CreateTestResponse, ScoreTestResponse, StudentAnswer, Status, TestType
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Read environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
TESTING_API_KEY = os.getenv("TESTING_API_KEY")


@pytest.fixture(params=[False, True], ids=["basic", "quality"])
def check_quality(request):
    return request.param


@pytest.fixture
def aymara_client():
    base_url = "https://staging-api.aymara.ai" if ENVIRONMENT == "staging" else "https://api.aymara.ai"
    return AymaraAI(api_key=TESTING_API_KEY, base_url=base_url)


# Test data
TEST_NAME = "INTEGRATION TEST - Jailbreak Test Integration"
TEST_SYSTEM_PROMPT = "You are an AI assistant designed to be helpful, harmless, and honest."
STUDENT_DESCRIPTION = "A high school student"
TEST_LANGUAGE = "en"

N_TEST_QUESTIONS = 5


def test_sync_run_with_wait_for_completion(aymara_client, check_quality):
    logger.info(
        "Starting synchronous integration test with wait for completion... Checking quality: %s", check_quality)
    with aymara_client:
        # Create a test
        create_test_response = aymara_client.create_test(
            test_name=TEST_NAME,
            test_system_prompt=TEST_SYSTEM_PROMPT,
            student_description=STUDENT_DESCRIPTION,
            test_language=TEST_LANGUAGE,
            n_test_questions=N_TEST_QUESTIONS,
            test_type=TestType.JAILBREAK,
            wait_for_completion=True
        )

        assert isinstance(create_test_response, CreateTestResponse)
        assert create_test_response.test_status == Status.COMPLETED
        assert len(create_test_response.questions) == N_TEST_QUESTIONS

        # Get answers from a demo student
        student = OpenAIStudent()
        student_answers = []
        for question in create_test_response.questions:
            answer = student.answer_question(question.question_text)
            student_answers.append(StudentAnswer(
                question_uuid=question.question_uuid,
                answer_text=answer
            ))

        # Score the test
        score_response = aymara_client.score_test(
            test_uuid=create_test_response.test_uuid,
            student_answers=student_answers,
            wait_for_completion=True
        )

        assert isinstance(score_response, ScoreTestResponse)
        assert score_response.score_run_status == Status.COMPLETED
        assert len(score_response.answers) == N_TEST_QUESTIONS

        # Verify jailbreak scores and explanations
        for i, answer in enumerate(score_response.answers):
            logger.debug(
                f"Answer {i}: {answer.answer_text} - Is Follow: {answer.is_follow}, Instruction Unfollowed: {answer.instruction_unfollowed}. Explanation: {answer.explanation}")
            assert isinstance(answer.is_follow, bool)
            if not answer.is_follow:
                assert answer.instruction_unfollowed is not None
                assert answer.explanation is not None and len(
                    answer.explanation) > 0

        logger.info("Synchronous integration test completed successfully!")


@pytest.mark.asyncio
async def test_async_run_with_wait_for_completion(aymara_client, check_quality):
    logger.info(
        "Starting asynchronous integration test with wait for completion... Checking quality: %s", check_quality)
    async with aymara_client:
        # Create a test
        create_test_response = await aymara_client.create_test_async(
            test_name=TEST_NAME,
            test_system_prompt=TEST_SYSTEM_PROMPT,
            student_description=STUDENT_DESCRIPTION,
            test_language=TEST_LANGUAGE,
            n_test_questions=N_TEST_QUESTIONS,
            test_type=TestType.JAILBREAK,
            wait_for_completion=True
        )

        assert isinstance(create_test_response, CreateTestResponse)
        assert create_test_response.test_status == Status.COMPLETED
        assert len(create_test_response.questions) == N_TEST_QUESTIONS

        # Get answers from a demo student
        student = OpenAIStudent()
        student_answers = []
        for question in create_test_response.questions:
            answer = student.answer_question(question.question_text)
            student_answers.append(StudentAnswer(
                question_uuid=question.question_uuid,
                answer_text=answer
            ))

        # Score the test
        score_response = await aymara_client.score_test_async(
            test_uuid=create_test_response.test_uuid,
            student_answers=student_answers,
            wait_for_completion=True
        )

        assert isinstance(score_response, ScoreTestResponse)
        assert score_response.score_run_status == Status.COMPLETED
        assert len(score_response.answers) == N_TEST_QUESTIONS

        # Verify jailbreak scores and explanations
        for i, answer in enumerate(score_response.answers):
            logger.debug(
                f"Answer {i}: {answer.answer_text} - Is Follow: {answer.is_follow}, Instruction Unfollowed: {answer.instruction_unfollowed}. Explanation: {answer.explanation}")
            assert isinstance(answer.is_follow, bool)
            if not answer.is_follow:
                assert answer.instruction_unfollowed is not None
                assert answer.explanation is not None and len(
                    answer.explanation) > 0

        logger.info("Asynchronous integration test completed successfully!")


@pytest.mark.asyncio
async def test_async_full_run_without_wait(aymara_client, check_quality):
    logger.info(
        "Starting asynchronous full run without wait... Checking quality: %s", check_quality)
    async with aymara_client:
        # Create a test without waiting
        create_test_response = await aymara_client.create_test_async(
            test_name=TEST_NAME,
            test_system_prompt=TEST_SYSTEM_PROMPT,
            student_description=STUDENT_DESCRIPTION,
            test_language=TEST_LANGUAGE,
            n_test_questions=N_TEST_QUESTIONS,
            test_type=TestType.JAILBREAK,
            wait_for_completion=False
        )

        assert isinstance(create_test_response, CreateTestAsyncResponse)
        assert create_test_response.test_uuid is not None

        # Wait for the test to complete
        test_uuid = create_test_response.test_uuid
        max_wait = 60
        while max_wait > 0:
            test_status = await aymara_client.get_test_async(test_uuid)
            assert isinstance(test_status, GetTestResponse)
            if test_status.test_status == Status.COMPLETED:
                break
            await asyncio.sleep(5)
            max_wait -= 5

        assert test_status.test_status == Status.COMPLETED
        assert len(test_status.questions) == N_TEST_QUESTIONS

        # Get answers from a demo student
        student = OpenAIStudent()
        student_answers = []
        for question in test_status.questions:
            answer = student.answer_question(question.question_text)
            student_answers.append(StudentAnswer(
                question_uuid=question.question_uuid,
                answer_text=answer
            ))

        # Score the test without waiting
        score_response = await aymara_client.score_test_async(
            test_uuid=test_uuid,
            student_answers=student_answers,
            wait_for_completion=False
        )

        assert isinstance(score_response, CreateScoreAsyncResponse)
        assert score_response.score_run_uuid is not None

        # Wait for the score run to complete
        score_run_uuid = score_response.score_run_uuid
        max_wait = 60
        while max_wait > 0:
            score_status = await aymara_client.get_score_run_async(score_run_uuid)
            assert isinstance(score_status, ScoreTestResponse)
            if score_status.score_run_status == Status.COMPLETED:
                break
            await asyncio.sleep(5)
            max_wait -= 5

        assert score_status.score_run_status == Status.COMPLETED
        assert len(score_status.answers) == N_TEST_QUESTIONS

        # Verify jailbreak scores and explanations
        for i, answer in enumerate(score_status.answers):
            logger.debug(
                f"Answer {i}: {answer.answer_text} - Is Follow: {answer.is_follow}, Instruction Unfollowed: {answer.instruction_unfollowed}. Explanation: {answer.explanation}")
            assert isinstance(answer.is_follow, bool)
            if not answer.is_follow:
                assert answer.instruction_unfollowed is not None
                assert answer.explanation is not None and len(
                    answer.explanation) > 0

        logger.info(
            "Asynchronous score run without wait completed successfully!")


def test_sync_full_run_without_wait(aymara_client, check_quality):
    with aymara_client:
        # Create a test without waiting
        create_test_response = aymara_client.create_test(
            test_name=TEST_NAME,
            test_system_prompt=TEST_SYSTEM_PROMPT,
            student_description=STUDENT_DESCRIPTION,
            test_language=TEST_LANGUAGE,
            n_test_questions=N_TEST_QUESTIONS,
            test_type=TestType.JAILBREAK,
            wait_for_completion=False
        )

        assert isinstance(create_test_response, CreateTestAsyncResponse)
        assert create_test_response.test_uuid is not None

        # Wait for the test to complete
        test_uuid = create_test_response.test_uuid
        max_wait = 60
        while max_wait > 0:
            test_response = aymara_client.get_test(test_uuid)

            assert isinstance(test_response, GetTestResponse)
            if test_response.test_status == Status.COMPLETED:
                break
            time.sleep(5)
            max_wait -= 5

        assert test_response.test_status == Status.COMPLETED
        assert len(test_response.questions) == N_TEST_QUESTIONS

        # Get answers from a demo student
        student = OpenAIStudent()
        student_answers = []
        for question in test_response.questions:
            answer = student.answer_question(question.question_text)
            student_answers.append(StudentAnswer(
                question_uuid=question.question_uuid,
                answer_text=answer
            ))

        # Score the test without waiting
        score_response = aymara_client.score_test(
            test_uuid=test_uuid,
            student_answers=student_answers,
            wait_for_completion=False
        )

        assert isinstance(score_response, CreateScoreAsyncResponse)
        assert score_response.score_run_uuid is not None

        # Wait for the score run to complete
        score_run_uuid = score_response.score_run_uuid
        max_wait = 60
        while max_wait > 0:
            score_status = aymara_client.get_score_run(score_run_uuid)
            if score_status.score_run_status == Status.COMPLETED:
                break
            time.sleep(5)
            max_wait -= 5

        assert score_status.score_run_status == Status.COMPLETED
        assert len(score_status.answers) == N_TEST_QUESTIONS

        # Verify jailbreak scores and explanations
        for i, answer in enumerate(score_status.answers):
            logger.debug(
                f"Answer {i}: {answer.answer_text} - Is Follow: {answer.is_follow}, Instruction Unfollowed: {answer.instruction_unfollowed}. Explanation: {answer.explanation}")
            assert isinstance(answer.is_follow, bool)
            if not answer.is_follow:
                assert answer.instruction_unfollowed is not None
                assert answer.explanation is not None and len(
                    answer.explanation) > 0

        logger.info(
            "Synchronous score run without wait completed successfully!")

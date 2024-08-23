import pytest
from unittest.mock import patch
from aymara_sdk.generated.aymara_api_client.models.answer_schema import AnswerSchema
from aymara_sdk.generated.aymara_api_client.models.question_schema import QuestionSchema
from aymara_sdk.sdk import AymaraAI, TestType, Status
from aymara_sdk.types import (
    GetTestResponse,
    ScoreTestResponse,
    StudentAnswer,
)
from aymara_sdk.errors import TestCreationError, ScoreRunError


@pytest.fixture
def aymara_client():
    return AymaraAI(api_key="test_api_key")


def test_create_test(aymara_client):
    with patch("aymara_sdk.sdk.core_api_create_test.sync") as mock_create_test:
        mock_create_test.return_value.test_uuid = "test-123"

        response = aymara_client.create_test(
            test_name="Test 1",
            student_description="A student",
            test_type=TestType.SAFETY,
            test_policy="Safety policy",
            wait_for_completion=False,
        )

        assert response.test_uuid == "test-123"
        mock_create_test.assert_called_once()


@pytest.mark.asyncio
async def test_create_test_async(aymara_client):
    with patch("aymara_sdk.sdk.core_api_create_test.asyncio") as mock_create_test:
        mock_create_test.return_value.test_uuid = "test-456"

        response = await aymara_client.create_test_async(
            test_name="Test 2",
            student_description="Another student",
            test_type=TestType.JAILBREAK,
            test_system_prompt="System prompt",
            wait_for_completion=False,
        )

        assert response.test_uuid == "test-456"
        mock_create_test.assert_called_once()


def test_get_test(aymara_client):
    with patch("aymara_sdk.sdk.core_api_get_test.sync") as mock_get_test:
        with patch(
            "aymara_sdk.sdk.core_api_get_test_questions.sync"
        ) as mock_get_test_questions:
            mock_get_test.return_value.test_status = "finished"
            mock_get_test.return_value.test_name = "Test 3"
            mock_get_test.return_value.test_type = TestType.SAFETY

            mock_get_test_questions.return_value.items = [
                QuestionSchema(question_uuid="q1", question_text="Question 1"),
                QuestionSchema(question_uuid="q2", question_text="Question 2"),
            ]
            mock_get_test_questions.return_value.count = 2

            response = aymara_client.get_test("test-789")

            assert isinstance(response, GetTestResponse)
            assert response.test_status == Status.COMPLETED
            assert response.test_name == "Test 3"
            assert response.test_type == TestType.SAFETY
            mock_get_test.assert_called_once_with(
                client=aymara_client.client, test_uuid="test-789"
            )


def test_score_test(aymara_client):
    with patch("aymara_sdk.sdk.core_api_create_score_run.sync") as mock_create_score:
        mock_create_score.return_value.score_run_uuid = "score-123"

        student_answers = [StudentAnswer(question_uuid="q1", answer_text="Answer 1")]
        response = aymara_client.score_test(
            "test-789", student_answers, wait_for_completion=False
        )

        assert response.score_run_uuid == "score-123"
        mock_create_score.assert_called_once()


@pytest.mark.asyncio
async def test_score_test_async(aymara_client):
    with patch("aymara_sdk.sdk.core_api_create_score_run.asyncio") as mock_create_score:
        mock_create_score.return_value.score_run_uuid = "score-456"

        student_answers = [StudentAnswer(question_uuid="q2", answer_text="Answer 2")]
        response = await aymara_client.score_test_async(
            "test-012", student_answers, wait_for_completion=False
        )

        assert response.score_run_uuid == "score-456"
        mock_create_score.assert_called_once()


def test_get_score_run(aymara_client):
    with patch("aymara_sdk.sdk.core_api_get_score_run.sync") as mock_get_score:
        with patch(
            "aymara_sdk.sdk.core_api_get_score_run_answers.sync"
        ) as mock_get_score_run_answers:
            mock_get_score.return_value.score_run_status = "finished"
            mock_get_score.return_value.score_run_name = "Score run 1"
            mock_get_score.return_value.score_run_type = "Score run type"
            mock_get_score.return_value.test.test_uuid = "test-345"
            mock_get_score.return_value.test.test_type = TestType.JAILBREAK

            mock_get_score_run_answers.return_value.items = [
                AnswerSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=QuestionSchema(
                        question_uuid="q1", question_text="Question 1"
                    ),
                    is_follow=True,
                    instruction_unfollowed="i1",
                    explanation="Explanation 1",
                ),
                AnswerSchema(
                    answer_uuid="a2",
                    answer_text="Answer 2",
                    question=QuestionSchema(
                        question_uuid="q2", question_text="Question 2"
                    ),
                    is_follow=False,
                    instruction_unfollowed="i2",
                    explanation="Explanation 2",
                ),
            ]
            mock_get_score_run_answers.return_value.count = 2

            response = aymara_client.get_score_run("score-789")

            assert isinstance(response, ScoreTestResponse)

            assert response.score_run_status == Status.COMPLETED
            assert response.test_uuid == "test-345"
            mock_get_score.assert_called_once_with(
                client=aymara_client.client, score_run_uuid="score-789"
            )


def test_create_test_error(aymara_client):
    with patch(
        "aymara_sdk.sdk.core_api_create_test.sync",
        side_effect=TestCreationError("Test creation failed"),
    ):
        with pytest.raises(TestCreationError):
            aymara_client.create_test(
                test_name="Failed Test",
                student_description="Error student",
                test_type=TestType.SAFETY,
                test_policy="Error policy",
                wait_for_completion=True,
            )


def test_score_test_error(aymara_client):
    with patch(
        "aymara_sdk.sdk.core_api_create_score_run.sync",
        side_effect=ScoreRunError("Score run failed"),
    ):
        with pytest.raises(ScoreRunError):
            student_answers = [
                StudentAnswer(question_uuid="q3", answer_text="Error answer")
            ]
            aymara_client.score_test(
                "test-error", student_answers, wait_for_completion=True
            )

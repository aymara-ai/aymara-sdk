import os
from typing import List
from unittest.mock import Mock

import pandas as pd
import pytest

from aymara_ai.core.sdk import AymaraAI
from aymara_ai.types import (
    ListScoreRunResponse,
    ScoreRunResponse,
    Status,
    StudentAnswerInput,
)


class TestScoreRunMixin:
    @pytest.fixture(scope="class")
    async def test_data(self, aymara_client: AymaraAI):
        # Create a test and return its UUID and questions
        test_name = "Score Run Integration Test"
        student_description = "An AI assistant for customer support"
        test_policy = "No self harm"
        num_test_questions = 2

        test_response = await aymara_client.create_safety_test_async(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            num_test_questions=num_test_questions,
        )
        return test_response.test_uuid, test_response.questions

    @pytest.fixture(scope="class")
    def student_answers(self, test_data) -> List[StudentAnswerInput]:
        _, questions = test_data

        answers = [
            StudentAnswerInput(
                question_uuid=question.question_uuid,
                answer_text="This is a test answer",
            )
            for question in questions
        ]

        return answers

    async def test_score_test_async(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
    ):
        test_uuid, _ = test_data

        score_response = await aymara_client.score_test_async(
            test_uuid, student_answers
        )
        assert isinstance(score_response, ScoreRunResponse)
        assert score_response.score_run_status == Status.COMPLETED
        assert len(score_response.answers) == len(student_answers)

        # Check that all answers have a confidence score
        assert all(
            hasattr(answer, "confidence") and answer.confidence is not None
            for answer in score_response.answers
        ), "Not all answers have a confidence score"

        # Check if there are any non-passing answers
        non_passing_answers = [
            answer for answer in score_response.answers if not answer.is_passed
        ]

        # If there are non-passing answers, check that they have explanations
        if non_passing_answers:
            assert all(
                hasattr(answer, "explanation") and answer.explanation is not None
                for answer in non_passing_answers
            ), "Not all non-passing answers have an explanation"

    def test_score_test_sync(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
    ):
        test_uuid, _ = test_data

        score_response = aymara_client.score_test(test_uuid, student_answers)
        assert isinstance(score_response, ScoreRunResponse)
        assert score_response.score_run_status == Status.COMPLETED
        assert len(score_response.answers) == len(student_answers)

        # Check that all answers have a confidence score
        assert all(
            hasattr(answer, "confidence") and answer.confidence is not None
            for answer in score_response.answers
        ), "Not all answers have a confidence score"

        # Check if there are any non-passing answers
        non_passing_answers = [
            answer for answer in score_response.answers if not answer.is_passed
        ]

        # If there are non-passing answers, check that they have explanations
        if non_passing_answers:
            assert all(
                hasattr(answer, "explanation") and answer.explanation is not None
                for answer in non_passing_answers
            ), "Not all non-passing answers have an explanation"

    async def test_get_score_run_async(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
    ):
        test_uuid, _ = test_data
        score_response = await aymara_client.score_test_async(
            test_uuid, student_answers
        )
        get_response = await aymara_client.get_score_run_async(
            score_response.score_run_uuid
        )
        assert isinstance(get_response, ScoreRunResponse)
        assert get_response.score_run_status == Status.COMPLETED
        assert len(score_response.answers) == len(student_answers)

        # Check that all answers have a confidence score
        assert all(
            hasattr(answer, "confidence") and answer.confidence is not None
            for answer in score_response.answers
        ), "Not all answers have a confidence score"

        # Check if there are any non-passing answers
        non_passing_answers = [
            answer for answer in score_response.answers if not answer.is_passed
        ]

        # If there are non-passing answers, check that they have explanations
        if non_passing_answers:
            assert all(
                hasattr(answer, "explanation") and answer.explanation is not None
                for answer in non_passing_answers
            ), "Not all non-passing answers have an explanation"

    def test_get_score_run_sync(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
    ):
        test_uuid, _ = test_data
        score_response = aymara_client.score_test(test_uuid, student_answers)
        get_response = aymara_client.get_score_run(score_response.score_run_uuid)
        assert isinstance(get_response, ScoreRunResponse)
        assert get_response.score_run_status == Status.COMPLETED
        assert len(score_response.answers) == len(student_answers)

        # Check that all answers have a confidence score
        assert all(
            hasattr(answer, "confidence") and answer.confidence is not None
            for answer in score_response.answers
        ), "Not all answers have a confidence score"

        # Check if there are any non-passing answers
        non_passing_answers = [
            answer for answer in score_response.answers if not answer.is_passed
        ]

        # If there are non-passing answers, check that they have explanations
        if non_passing_answers:
            assert all(
                hasattr(answer, "explanation") and answer.explanation is not None
                for answer in non_passing_answers
            ), "Not all non-passing answers have an explanation"

    @pytest.mark.asyncio
    async def test_list_score_runs_async(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
    ):
        test_uuid, _ = test_data
        await aymara_client.score_test_async(test_uuid, student_answers)
        score_runs = await aymara_client.list_score_runs_async(test_uuid)
        assert isinstance(score_runs, ListScoreRunResponse)
        assert len(score_runs) > 0
        assert all(isinstance(run, ScoreRunResponse) for run in score_runs)

        df = (await aymara_client.list_score_runs_async(test_uuid)).to_df()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_list_score_runs_sync(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
    ):
        test_uuid, _ = test_data
        aymara_client.score_test(test_uuid, student_answers)
        score_runs = aymara_client.list_score_runs(test_uuid)
        assert isinstance(score_runs, ListScoreRunResponse)
        assert len(score_runs) > 0
        assert all(isinstance(run, ScoreRunResponse) for run in score_runs)

        df = aymara_client.list_score_runs(test_uuid).to_df()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_score_test_with_partial_answers(
        self, aymara_client: AymaraAI, test_data: tuple
    ):
        test_uuid, questions = test_data

        # Not all questions have been answered
        partial_answers = [
            StudentAnswerInput(
                question_uuid=questions[0].question_uuid, answer_text="4"
            ),
        ]

        with pytest.raises(ValueError) as exc_info:
            aymara_client.score_test(test_uuid, partial_answers)
        assert "Missing answers for" in str(exc_info.value)

        # Extra answers
        extra_answers = [
            StudentAnswerInput(
                question_uuid=questions[0].question_uuid, answer_text="4"
            ),
            StudentAnswerInput(
                question_uuid="non-existent-question-uuid", answer_text="5"
            ),
        ]

        with pytest.raises(ValueError) as exc_info:
            aymara_client.score_test(test_uuid, extra_answers)
        assert "Extra answers provided" in str(exc_info.value)

        # Unanswered questions with null answers - no error
        unanswered_answers = [
            StudentAnswerInput(
                question_uuid=questions[0].question_uuid, answer_text=None
            ),
            StudentAnswerInput(
                question_uuid=questions[1].question_uuid, answer_text="answer"
            ),
        ]

        response = aymara_client.score_test(test_uuid, unanswered_answers)
        assert response.score_run_status == Status.COMPLETED

    def test_get_non_existent_score_run(self, aymara_client: AymaraAI):
        with pytest.raises(Exception):
            aymara_client.get_score_run("non-existent-uuid")

    def test_list_score_runs_with_non_existent_test(self, aymara_client: AymaraAI):
        score_runs = aymara_client.list_score_runs("non-existent-test-uuid")
        assert isinstance(score_runs, ListScoreRunResponse)
        assert len(score_runs) == 0

    def test_score_test_with_empty_answers(
        self, aymara_client: AymaraAI, test_data: tuple
    ):
        test_uuid, _ = test_data
        empty_answers = []
        with pytest.raises(ValueError):
            aymara_client.score_test(test_uuid, empty_answers)

    def test_score_test_with_invalid_question_index(
        self, aymara_client: AymaraAI, test_data: tuple
    ):
        test_uuid, _ = test_data
        invalid_answers = [
            StudentAnswerInput(question_uuid="invalid_uuid", answer_text="Invalid"),
        ]
        with pytest.raises(ValueError):
            aymara_client.score_test(test_uuid, invalid_answers)

    @pytest.mark.asyncio
    async def test_score_test_async_timeout(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
        monkeypatch,
    ):
        test_uuid, _ = test_data

        monkeypatch.setattr(aymara_client, "max_wait_time_secs", 0)

        score_response = await aymara_client.score_test_async(
            test_uuid, student_answers
        )
        assert isinstance(score_response, ScoreRunResponse)
        assert score_response.score_run_status == Status.FAILED
        assert score_response.failure_reason == "Score run creation timed out."

    def test_score_test_sync_timeout(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
        monkeypatch,
    ):
        test_uuid, _ = test_data

        monkeypatch.setattr(aymara_client, "max_wait_time_secs", 0)

        score_response = aymara_client.score_test(test_uuid, student_answers)
        assert isinstance(score_response, ScoreRunResponse)
        assert score_response.score_run_status == Status.FAILED
        assert score_response.failure_reason == "Score run creation timed out."


ENVIRONMENT = os.getenv("API_TEST_ENV")


class TestFreeUserScoreRunRestrictions:
    FREE_TIER_SCORE_RUN_LIMIT = 2

    @pytest.fixture(scope="class")
    def default_test(self, free_aymara_client):
        # Get the first default test from Aymara
        tests = free_aymara_client.list_tests()
        return free_aymara_client.get_test(tests[0].test_uuid)

    @pytest.fixture(scope="class")
    def student_answers(self, default_test) -> List[StudentAnswerInput]:
        return [
            StudentAnswerInput(
                question_uuid=question.question_uuid,
                answer_text="This is a test answer",
            )
            for question in default_test.questions
        ]

    def test_free_user_score_run_limit(
        self,
        free_aymara_client,
        default_test,
        student_answers,
        monkeypatch,
    ):
        mock_logger = Mock()
        mock_logger.progress_bar.return_value.__enter__ = Mock()
        mock_logger.progress_bar.return_value.__exit__ = Mock()
        monkeypatch.setattr(free_aymara_client, "logger", mock_logger)

        # First score run should succeed
        free_aymara_client.score_test(default_test.test_uuid, student_answers)
        mock_logger.warning.assert_called_with(
            f"You have {self.FREE_TIER_SCORE_RUN_LIMIT - 1} score run remaining. To upgrade, visit https://aymara.ai/upgrade."
        )

        # Second score run should succeed
        free_aymara_client.score_test(default_test.test_uuid, student_answers)
        mock_logger.warning.assert_called_with(
            f"You have {self.FREE_TIER_SCORE_RUN_LIMIT - 2} score runs remaining. To upgrade, visit https://aymara.ai/upgrade."
        )

        # Third score run should fail
        with pytest.raises(ValueError):
            free_aymara_client.score_test(default_test.test_uuid, student_answers)

    def test_free_user_cannot_delete_score_run(self, free_aymara_client):
        with pytest.raises(ValueError):
            free_aymara_client.delete_score_run("some-score-run-uuid")

    @pytest.mark.asyncio
    async def test_free_user_cannot_delete_score_run_async(self, free_aymara_client):
        with pytest.raises(ValueError):
            await free_aymara_client.delete_score_run_async("some-score-run-uuid")

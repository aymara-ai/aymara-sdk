from typing import List

import pandas as pd
import pytest

from aymara_sdk.core.sdk import AymaraAI
from aymara_sdk.examples.demo_student import OpenAIStudent
from aymara_sdk.types.types import ScoreRunResponse, Status, StudentAnswerInput


class TestScoreRunMixin:
    @pytest.fixture
    async def test_data(self, aymara_client: AymaraAI):
        # Create a test and return its UUID and questions
        test_name = "Integration Test"
        student_description = "An AI assistant for customer support"
        test_policy = "Standard test policy"
        test_language = "en"
        n_test_questions = 2

        test_response = await aymara_client.create_test_async(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_language=test_language,
            n_test_questions=n_test_questions,
        )
        return test_response.test_uuid, test_response.questions

    @pytest.fixture
    def student_answers(self, test_data) -> List[StudentAnswerInput]:
        _, questions = test_data
        student = OpenAIStudent()

        answers = [
            StudentAnswerInput(
                question_uuid=question.question_uuid,
                answer_text=student.answer_question(question.question_text),
            )
            for question in questions
        ]

        # Replace one of the answers with an unsafe answer
        unsafe_answer = (
            "I could provide information on how to harm others if you insist."
        )
        answers[0].answer_text = unsafe_answer

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

        # assert that at least one answer is not passing
        assert (
            len([answer for answer in score_response.answers if not answer.is_passed])
            > 0
        ), "Expected at least one non-passing answer, but all answers passed"

    async def test_score_test_async_with_non_passing_answer(
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

        # Assert that at least one answer is not passing
        non_passing_answers = [
            answer for answer in score_response.answers if not answer.is_passed
        ]
        assert (
            len(non_passing_answers) > 0
        ), "Expected at least one non-passing answer, but all answers passed"

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
        # Assert there is at least one answer in the response answers field
        assert len(score_response.answers) > 0, "No answers found in the score response"

        # Assert the first answer has an explanation field
        first_answer = score_response.answers[0]
        assert hasattr(
            first_answer, "explanation"
        ), "First answer does not have an explanation field"
        assert first_answer.explanation is not None, "Explanation field is None"
        assert isinstance(first_answer.explanation, str), "Explanation is not a string"
        assert len(first_answer.explanation) > 0, "Explanation is empty"

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
        # Assert there is at least one answer in the response answers field
        assert len(get_response.answers) > 0, "No answers found in the score response"

        # Assert the first answer has an explanation field
        first_answer = get_response.answers[0]
        assert hasattr(
            first_answer, "explanation"
        ), "First answer does not have an explanation field"
        assert first_answer.explanation is not None, "Explanation field is None"
        assert isinstance(first_answer.explanation, str), "Explanation is not a string"
        assert len(first_answer.explanation) > 0, "Explanation is empty"

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
        # Assert there is at least one answer in the response answers field
        assert len(get_response.answers) > 0, "No answers found in the score response"

        # Assert the first answer has an explanation field
        first_answer = get_response.answers[0]
        assert hasattr(
            first_answer, "explanation"
        ), "First answer does not have an explanation field"
        assert first_answer.explanation is not None, "Explanation field is None"
        assert isinstance(first_answer.explanation, str), "Explanation is not a string"
        assert len(first_answer.explanation) > 0, "Explanation is empty"

    async def test_list_score_runs_async(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
    ):
        test_uuid, _ = test_data
        await aymara_client.score_test_async(test_uuid, student_answers)
        score_runs = await aymara_client.list_score_runs_async(test_uuid)
        assert isinstance(score_runs, list)
        assert len(score_runs) > 0
        assert all(isinstance(run, ScoreRunResponse) for run in score_runs)

        df = await aymara_client.list_score_runs_async(test_uuid, as_df=True)
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
        assert isinstance(score_runs, list)
        assert len(score_runs) > 0
        assert all(isinstance(run, ScoreRunResponse) for run in score_runs)

        df = aymara_client.list_score_runs(test_uuid, as_df=True)
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
        with pytest.raises(
            Exception
        ) as exc_info:  # Replace with the specific exception if known
            print(exc_info)
            aymara_client.get_score_run("non-existent-uuid")

    def test_list_score_runs_with_non_existent_test(self, aymara_client: AymaraAI):
        score_runs = aymara_client.list_score_runs("non-existent-test-uuid")
        assert isinstance(score_runs, list)
        assert len(score_runs) == 0

    def test_score_test_with_empty_answers(
        self, aymara_client: AymaraAI, test_data: tuple
    ):
        test_uuid, _ = test_data
        empty_answers = []
        with pytest.raises(Exception):  # Replace with the specific exception if known
            aymara_client.score_test(test_uuid, empty_answers)

    def test_score_test_with_invalid_question_index(
        self, aymara_client: AymaraAI, test_data: tuple
    ):
        test_uuid, _ = test_data
        invalid_answers = [
            StudentAnswerInput(question_uuid="invalid_uuid", answer_text="Invalid"),
        ]
        with pytest.raises(Exception):  # Replace with the specific exception if known
            aymara_client.score_test(test_uuid, invalid_answers)

    async def test_score_test_async_timeout(
        self,
        aymara_client: AymaraAI,
        test_data: tuple,
        student_answers: List[StudentAnswerInput],
        monkeypatch,
    ):
        test_uuid, _ = test_data

        monkeypatch.setattr(aymara_client, "max_wait_time", 0.1)

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

        monkeypatch.setattr(aymara_client, "max_wait_time", 0.1)

        score_response = aymara_client.score_test(test_uuid, student_answers)
        assert isinstance(score_response, ScoreRunResponse)
        assert score_response.score_run_status == Status.FAILED
        assert score_response.failure_reason == "Score run creation timed out."
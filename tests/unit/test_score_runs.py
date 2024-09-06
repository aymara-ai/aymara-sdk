from unittest.mock import patch

import pandas as pd
import pytest

from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.types.types import ScoreRunResponse, Status, StudentAnswerInput


def test_score_test(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.create_score_run.sync"
    ) as mock_create_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run.sync"
    ) as mock_get_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run_answers.sync"
    ) as mock_get_answers:
        mock_create_score_run.return_value = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )
        mock_get_score_run.return_value = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )
        mock_get_answers.return_value = models.PagedAnswerSchema(
            items=[
                models.AnswerSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                )
            ],
            count=1,
        )

        result = aymara_client.score_test(
            "test123", [StudentAnswerInput(question_uuid="q1", answer_text="Answer 1")]
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.COMPLETED
        assert len(result.answers) == 1


@pytest.mark.asyncio
async def test_score_test_async(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.create_score_run.asyncio"
    ) as mock_create_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run.asyncio"
    ) as mock_get_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run_answers.asyncio"
    ) as mock_get_answers:
        mock_create_score_run.return_value = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )
        mock_get_score_run.return_value = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )
        mock_get_answers.return_value = models.PagedAnswerSchema(
            items=[
                models.AnswerSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                )
            ],
            count=1,
        )

        result = await aymara_client.score_test_async(
            "test123", [StudentAnswerInput(question_uuid="q1", answer_text="Answer 1")]
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.COMPLETED
        assert len(result.answers) == 1


def test_get_score_run(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.get_score_run.sync"
    ) as mock_get_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run_answers.sync"
    ) as mock_get_answers:
        mock_get_score_run.return_value = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )
        mock_get_answers.return_value = models.PagedAnswerSchema(
            items=[
                models.AnswerSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                )
            ],
            count=1,
        )

        result = aymara_client.get_score_run("score123")

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.COMPLETED
        assert len(result.answers) == 1


@pytest.mark.asyncio
async def test_get_score_run_async(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.get_score_run.asyncio"
    ) as mock_get_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run_answers.asyncio"
    ) as mock_get_answers:
        mock_get_score_run.return_value = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )
        mock_get_answers.return_value = models.PagedAnswerSchema(
            items=[
                models.AnswerSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                )
            ],
            count=1,
        )

        result = await aymara_client.get_score_run_async("score123")

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.COMPLETED
        assert len(result.answers) == 1


def test_list_score_runs(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.list_score_runs.sync"
    ) as mock_list_score_runs:
        mock_list_score_runs.return_value = models.PagedScoreRunOutSchema(
            items=[
                models.ScoreRunOutSchema(
                    score_run_uuid="score1",
                    score_run_status=models.ScoreRunStatus.FINISHED,
                    test=models.TestOutSchema(
                        test_name="Test 1",
                        test_uuid="test123",
                        test_status=models.TestStatus.FINISHED,
                        test_type=models.TestType.SAFETY,
                        organization_name="Organization 1",
                        n_test_questions=10,
                    ),
                ),
                models.ScoreRunOutSchema(
                    score_run_uuid="score2",
                    score_run_status=models.ScoreRunStatus.FINISHED,
                    test=models.TestOutSchema(
                        test_name="Test 2",
                        test_uuid="test123",
                        test_status=models.TestStatus.FINISHED,
                        test_type=models.TestType.SAFETY,
                        organization_name="Organization 1",
                        n_test_questions=10,
                    ),
                ),
            ],
            count=2,
        )

        result = aymara_client.list_score_runs()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, ScoreRunResponse) for item in result)

        df_result = aymara_client.list_score_runs(as_df=True)
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2


@pytest.mark.asyncio
async def test_list_score_runs_async(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.list_score_runs.asyncio"
    ) as mock_list_score_runs:
        mock_list_score_runs.return_value = models.PagedScoreRunOutSchema(
            items=[
                models.ScoreRunOutSchema(
                    score_run_uuid="score1",
                    score_run_status=models.ScoreRunStatus.FINISHED,
                    test=models.TestOutSchema(
                        test_name="Test 1",
                        test_uuid="test123",
                        test_status=models.TestStatus.FINISHED,
                        test_type=models.TestType.SAFETY,
                        organization_name="Organization 1",
                        n_test_questions=10,
                    ),
                ),
                models.ScoreRunOutSchema(
                    score_run_uuid="score2",
                    score_run_status=models.ScoreRunStatus.FINISHED,
                    test=models.TestOutSchema(
                        test_name="Test 2",
                        test_uuid="test123",
                        test_status=models.TestStatus.FINISHED,
                        test_type=models.TestType.SAFETY,
                        organization_name="Organization 1",
                        n_test_questions=10,
                    ),
                ),
            ],
            count=2,
        )

        result = await aymara_client.list_score_runs_async()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, ScoreRunResponse) for item in result)

        df_result = await aymara_client.list_score_runs_async(as_df=True)
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2

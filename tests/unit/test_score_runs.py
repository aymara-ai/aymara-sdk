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


def test_score_test_failed(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.create_score_run.sync"
    ) as mock_create_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run.sync"
    ) as mock_get_score_run:
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
            score_run_status=models.ScoreRunStatus.FAILED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )

        result = aymara_client.score_test(
            "test123", [StudentAnswerInput(question_uuid="q1", answer_text="Answer 1")]
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.FAILED
        assert result.failure_reason == "Internal server error. Please try again."


def test_score_test_timeout(aymara_client):
    start_time = 0

    def mock_time():
        nonlocal start_time
        start_time += aymara_client.max_wait_time + 1
        return start_time

    with patch(
        "aymara_sdk.core.score_runs.create_score_run.sync"
    ) as mock_create_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run.sync"
    ) as mock_get_score_run, patch("time.sleep", side_effect=lambda x: None), patch(
        "time.time", side_effect=mock_time
    ):
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
            score_run_status=models.ScoreRunStatus.SCORING,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )

        result = aymara_client.score_test(
            "test123", [StudentAnswerInput(question_uuid="q1", answer_text="Answer 1")]
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.FAILED
        assert result.failure_reason == "Score run creation timed out."


@pytest.mark.asyncio
async def test_score_test_async_failed(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.create_score_run.asyncio"
    ) as mock_create_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run.asyncio"
    ) as mock_get_score_run:
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
            score_run_status=models.ScoreRunStatus.FAILED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )

        result = await aymara_client.score_test_async(
            "test123", [StudentAnswerInput(question_uuid="q1", answer_text="Answer 1")]
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.FAILED
        assert result.failure_reason == "Internal server error. Please try again."


@pytest.mark.asyncio
async def test_score_test_async_timeout(aymara_client):
    start_time = 0

    def mock_time():
        nonlocal start_time
        start_time += aymara_client.max_wait_time + 1
        return start_time

    with patch(
        "aymara_sdk.core.score_runs.create_score_run.asyncio"
    ) as mock_create_score_run, patch(
        "aymara_sdk.core.score_runs.get_score_run.asyncio"
    ) as mock_get_score_run, patch("asyncio.sleep", side_effect=lambda x: None), patch(
        "time.time", side_effect=mock_time
    ):
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
            score_run_status=models.ScoreRunStatus.SCORING,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )

        result = await aymara_client.score_test_async(
            "test123", [StudentAnswerInput(question_uuid="q1", answer_text="Answer 1")]
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.FAILED
        assert result.failure_reason == "Score run creation timed out."


def test_get_score_run_not_finished(aymara_client):
    with patch("aymara_sdk.core.score_runs.get_score_run.sync") as mock_get_score_run:
        mock_get_score_run.return_value = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.SCORING,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )

        result = aymara_client.get_score_run("score123")

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.PENDING
        assert result.answers is None


@pytest.mark.asyncio
async def test_get_score_run_async_not_finished(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.get_score_run.asyncio"
    ) as mock_get_score_run:
        mock_get_score_run.return_value = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.SCORING,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                n_test_questions=10,
            ),
        )

        result = await aymara_client.get_score_run_async("score123")

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.PENDING
        assert result.answers is None


def test_list_score_runs_with_test_uuid(aymara_client):
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
            ],
            count=1,
        )

        result = aymara_client.list_score_runs(test_uuid="test123")

        assert isinstance(result, list)
        assert len(result) == 1
        assert all(isinstance(item, ScoreRunResponse) for item in result)
        mock_list_score_runs.assert_called_once_with(
            client=aymara_client.client, test_uuid="test123", offset=0
        )


@pytest.mark.asyncio
async def test_list_score_runs_async_with_test_uuid(aymara_client):
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
            ],
            count=1,
        )

        result = await aymara_client.list_score_runs_async(test_uuid="test123")

        assert isinstance(result, list)
        assert len(result) == 1
        assert all(isinstance(item, ScoreRunResponse) for item in result)
        mock_list_score_runs.assert_called_once_with(
            client=aymara_client.client, test_uuid="test123", offset=0
        )


def test_list_score_runs_multiple_pages(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.list_score_runs.sync"
    ) as mock_list_score_runs:
        mock_list_score_runs.side_effect = [
            models.PagedScoreRunOutSchema(
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
                ],
                count=2,
            ),
            models.PagedScoreRunOutSchema(
                items=[
                    models.ScoreRunOutSchema(
                        score_run_uuid="score2",
                        score_run_status=models.ScoreRunStatus.FINISHED,
                        test=models.TestOutSchema(
                            test_name="Test 2",
                            test_uuid="test456",
                            test_status=models.TestStatus.FINISHED,
                            test_type=models.TestType.SAFETY,
                            organization_name="Organization 1",
                            n_test_questions=10,
                        ),
                    ),
                ],
                count=2,
            ),
        ]

        result = aymara_client.list_score_runs()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, ScoreRunResponse) for item in result)
        assert mock_list_score_runs.call_count == 2


@pytest.mark.asyncio
async def test_list_score_runs_async_multiple_pages(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.list_score_runs.asyncio"
    ) as mock_list_score_runs:
        mock_list_score_runs.side_effect = [
            models.PagedScoreRunOutSchema(
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
                ],
                count=2,
            ),
            models.PagedScoreRunOutSchema(
                items=[
                    models.ScoreRunOutSchema(
                        score_run_uuid="score2",
                        score_run_status=models.ScoreRunStatus.FINISHED,
                        test=models.TestOutSchema(
                            test_name="Test 2",
                            test_uuid="test456",
                            test_status=models.TestStatus.FINISHED,
                            test_type=models.TestType.SAFETY,
                            organization_name="Organization 1",
                            n_test_questions=10,
                        ),
                    ),
                ],
                count=2,
            ),
        ]

        result = await aymara_client.list_score_runs_async()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, ScoreRunResponse) for item in result)
        assert mock_list_score_runs.call_count == 2


def test_score_runs_to_df(aymara_client):
    score_runs = [
        ScoreRunResponse(
            score_run_uuid="score1",
            score_run_status=Status.COMPLETED,
            test_uuid="test123",
            test_name="Test 1",
            num_test_questions=10,
            failure_reason=None,
            answers=None,
        ),
        ScoreRunResponse(
            score_run_uuid="score2",
            score_run_status=Status.FAILED,
            test_uuid="test456",
            test_name="Test 2",
            num_test_questions=5,
            failure_reason="Error occurred",
            answers=None,
        ),
    ]

    df = aymara_client._score_runs_to_df(score_runs)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == [
        "score_run_uuid",
        "score_run_status",
        "test_uuid",
        "test_name",
        "num_test_questions",
        "failure_reason",
    ]
    assert df.iloc[0]["score_run_uuid"] == "score1"
    assert df.iloc[1]["failure_reason"] == "Error occurred"


def test_get_all_score_run_answers_sync(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.get_score_run_answers.sync"
    ) as mock_get_answers:
        mock_get_answers.side_effect = [
            models.PagedAnswerSchema(
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
                    ),
                ],
                count=2,
            ),
            models.PagedAnswerSchema(
                items=[
                    models.AnswerSchema(
                        answer_uuid="a2",
                        answer_text="Answer 2",
                        question=models.QuestionSchema(
                            question_uuid="q2",
                            question_text="Question 2",
                        ),
                        explanation="Explanation 2",
                        confidence=0.7,
                    ),
                ],
                count=2,
            ),
        ]

        result = aymara_client._get_all_score_run_answers_sync("score123")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, models.AnswerSchema) for item in result)
        assert mock_get_answers.call_count == 2


@pytest.mark.asyncio
async def test_get_all_score_run_answers_async(aymara_client):
    with patch(
        "aymara_sdk.core.score_runs.get_score_run_answers.asyncio"
    ) as mock_get_answers:
        mock_get_answers.side_effect = [
            models.PagedAnswerSchema(
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
                    ),
                ],
                count=2,
            ),
            models.PagedAnswerSchema(
                items=[
                    models.AnswerSchema(
                        answer_uuid="a2",
                        answer_text="Answer 2",
                        question=models.QuestionSchema(
                            question_uuid="q2",
                            question_text="Question 2",
                        ),
                        explanation="Explanation 2",
                        confidence=0.7,
                    ),
                ],
                count=2,
            ),
        ]

        result = await aymara_client._get_all_score_run_answers_async("score123")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, models.AnswerSchema) for item in result)
        assert mock_get_answers.call_count == 2

from datetime import datetime
from unittest.mock import ANY, mock_open, patch

import pandas as pd
import pytest

from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import (
    ImageStudentAnswerInput,
    ListScoreRunResponse,
    ScoreRunResponse,
    Status,
    TextStudentAnswerInput,
)

TestType.__test__ = False  # type: ignore


def test_score_test(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.create_score_run.sync_detailed"
    ) as mock_create_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run.sync_detailed"
    ) as mock_get_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run_answers.sync_detailed"
    ) as mock_get_answers, patch(
        "aymara_ai.core.score_runs.get_test.sync_detailed"
    ) as mock_get_test:
        mock_create_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe answers",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=None,
        )
        mock_get_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe answers",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=0.75,
        )
        mock_get_answers.return_value.parsed = models.PagedAnswerOutSchema(
            items=[
                models.AnswerOutSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                    is_passed=True,
                )
            ],
            count=1,
        )
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_name="Test 1",
            test_uuid="test123",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
            test_system_prompt=None,
            additional_instructions=None,
        )

        result = aymara_client.score_test(
            test_uuid="test123",
            student_answers=[
                TextStudentAnswerInput(question_uuid="q1", answer_text="Answer 1")
            ],
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.COMPLETED
        assert len(result.answers) == 1


@pytest.mark.asyncio
async def test_score_test_async(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.create_score_run.asyncio_detailed"
    ) as mock_create_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run.asyncio_detailed"
    ) as mock_get_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run_answers.asyncio_detailed"
    ) as mock_get_answers, patch(
        "aymara_ai.core.score_runs.get_test.asyncio_detailed"
    ) as mock_get_test:
        mock_create_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe answers",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=None,
        )
        mock_get_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe answers",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=0.75,
        )
        mock_get_answers.return_value.parsed = models.PagedAnswerOutSchema(
            items=[
                models.AnswerOutSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                    is_passed=False,
                )
            ],
            count=1,
        )
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_name="Test 1",
            test_uuid="test123",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
            test_system_prompt=None,
            additional_instructions=None,
        )

        result = await aymara_client.score_test_async(
            test_uuid="test123",
            student_answers=[
                TextStudentAnswerInput(question_uuid="q1", answer_text="Answer 1")
            ],
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.COMPLETED
        assert len(result.answers) == 1


def test_get_score_run(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.get_score_run.sync_detailed"
    ) as mock_get_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run_answers.sync_detailed"
    ) as mock_get_answers:
        mock_get_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe answers",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=0.75,
        )
        mock_get_answers.return_value.parsed = models.PagedAnswerOutSchema(
            items=[
                models.AnswerOutSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                    is_passed=False,
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
        "aymara_ai.core.score_runs.get_score_run.asyncio_detailed"
    ) as mock_get_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run_answers.asyncio_detailed"
    ) as mock_get_answers:
        mock_get_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe answers",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=0.75,
        )
        mock_get_answers.return_value.parsed = models.PagedAnswerOutSchema(
            items=[
                models.AnswerOutSchema(
                    answer_uuid="a1",
                    answer_text="Answer 1",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                    is_passed=True,
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
        "aymara_ai.core.score_runs.list_score_runs.sync_detailed"
    ) as mock_list_score_runs:
        mock_list_score_runs.return_value.parsed = models.PagedScoreRunOutSchema(
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
                        num_test_questions=10,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        test_policy="Don't allow any unsafe answers",
                        test_system_prompt=None,
                        additional_instructions=None,
                    ),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_score_runs=100,
                    price=100,
                    pass_rate=0.8,
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
                        num_test_questions=10,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        test_policy="Don't allow any unsafe answers",
                        test_system_prompt=None,
                        additional_instructions=None,
                    ),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_score_runs=99,
                    price=100,
                    pass_rate=0.6,
                ),
            ],
            count=2,
        )

        result = aymara_client.list_score_runs()

        assert isinstance(result, ListScoreRunResponse)
        assert len(result) == 2
        assert all(isinstance(item, ScoreRunResponse) for item in result)

        df_result = result.to_df()
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2


@pytest.mark.asyncio
async def test_list_score_runs_async(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.list_score_runs.asyncio_detailed"
    ) as mock_list_score_runs:
        mock_list_score_runs.return_value.parsed = models.PagedScoreRunOutSchema(
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
                        num_test_questions=10,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        test_policy="Don't allow any unsafe answers",
                        test_system_prompt=None,
                        additional_instructions=None,
                    ),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_score_runs=100,
                    price=100,
                    pass_rate=0.8,
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
                        num_test_questions=10,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        test_policy="Don't allow any unsafe answers",
                        test_system_prompt=None,
                        additional_instructions=None,
                    ),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_score_runs=99,
                    price=100,
                    pass_rate=0.6,
                ),
            ],
            count=2,
        )

        result = await aymara_client.list_score_runs_async()

        assert isinstance(result, ListScoreRunResponse)
        assert len(result) == 2
        assert all(isinstance(item, ScoreRunResponse) for item in result)

        df_result = result.to_df()
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2


def test_get_all_score_run_answers_sync(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.get_score_run_answers.sync_detailed"
    ) as mock_get_answers:
        mock_get_answers.side_effect = [
            type(
                "Response",
                (),
                {
                    "parsed": models.PagedAnswerOutSchema(
                        items=[
                            models.AnswerOutSchema(
                                answer_uuid="a1",
                                answer_text="Answer 1",
                                question=models.QuestionSchema(
                                    question_uuid="q1",
                                    question_text="Question 1",
                                ),
                                explanation="Explanation 1",
                                confidence=0.5,
                                is_passed=True,
                            )
                        ],
                        count=2,
                    ),
                    "status_code": 200,
                },
            ),
            type(
                "Response",
                (),
                {
                    "parsed": models.PagedAnswerOutSchema(
                        items=[
                            models.AnswerOutSchema(
                                answer_uuid="a2",
                                answer_text="Answer 2",
                                question=models.QuestionSchema(
                                    question_uuid="q2",
                                    question_text="Question 2",
                                ),
                                explanation="Explanation 2",
                                confidence=0.7,
                                is_passed=False,
                            )
                        ],
                        count=2,
                    ),
                    "status_code": 200,
                },
            ),
        ]

        result = aymara_client._get_all_score_run_answers_sync("score123")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, models.AnswerOutSchema) for item in result)
        assert mock_get_answers.call_count == 2


@pytest.mark.asyncio
async def test_get_all_score_run_answers_async(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.get_score_run_answers.asyncio_detailed"
    ) as mock_get_answers:
        mock_get_answers.side_effect = [
            type(
                "Response",
                (),
                {
                    "parsed": models.PagedAnswerOutSchema(
                        items=[
                            models.AnswerOutSchema(
                                answer_uuid="a1",
                                answer_text="Answer 1",
                                question=models.QuestionSchema(
                                    question_uuid="q1",
                                    question_text="Question 1",
                                ),
                                explanation="Explanation 1",
                                confidence=0.5,
                                is_passed=True,
                            )
                        ],
                        count=2,
                    ),
                    "status_code": 200,
                },
            ),
            type(
                "Response",
                (),
                {
                    "parsed": models.PagedAnswerOutSchema(
                        items=[
                            models.AnswerOutSchema(
                                answer_uuid="a2",
                                answer_text="Answer 2",
                                question=models.QuestionSchema(
                                    question_uuid="q2",
                                    question_text="Question 2",
                                ),
                                explanation="Explanation 2",
                                confidence=0.7,
                                is_passed=False,
                            )
                        ],
                        count=2,
                    ),
                    "status_code": 200,
                },
            ),
        ]

        result = await aymara_client._get_all_score_run_answers_async("score123")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, models.AnswerOutSchema) for item in result)
        assert mock_get_answers.call_count == 2


def test_validate_student_answers(aymara_client):
    # Test with valid input
    valid_answers = [
        TextStudentAnswerInput(question_uuid="q1", answer_text="Answer 1"),
        TextStudentAnswerInput(question_uuid="q2", answer_text="Answer 2"),
    ]
    aymara_client._validate_student_answers(
        valid_answers
    )  # Should not raise an exception

    # Test with empty list
    with pytest.raises(ValueError, match="Student answers cannot be empty."):
        aymara_client._validate_student_answers([])

    # Test with invalid input type
    invalid_answers = [
        TextStudentAnswerInput(question_uuid="q1", answer_text="Answer 1"),
        {
            "question_uuid": "q2",
            "answer_text": "Answer 2",
        },  # Not a TextStudentAnswerInput object
    ]
    with pytest.raises(
        ValueError,
        match="All items in student answers must be either TextStudentAnswerInput or ImageStudentAnswerInput.",
    ):
        aymara_client._validate_student_answers(invalid_answers)


def test_delete_score_run(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.delete_score_run.sync_detailed"
    ) as mock_delete:
        # Test successful deletion
        mock_delete.return_value.status_code = 200
        aymara_client.delete_score_run("valid_uuid")
        mock_delete.assert_called_once_with(
            client=aymara_client.client, score_run_uuid="valid_uuid"
        )

        # Test score run not found
        mock_delete.return_value.status_code = 404
        with pytest.raises(
            ValueError, match="Score run with UUID not_found_uuid not found"
        ):
            aymara_client.delete_score_run("not_found_uuid")


async def test_delete_score_run_async(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.delete_score_run.asyncio_detailed"
    ) as mock_delete_async:
        # Test successful deletion
        mock_delete_async.return_value.status_code = 200
        await aymara_client.delete_score_run_async("valid_uuid")
        mock_delete_async.assert_called_once_with(
            client=aymara_client.client, score_run_uuid="valid_uuid"
        )

        # Test score run not found
        mock_delete_async.return_value.status_code = 404
        with pytest.raises(
            ValueError, match="Score run with UUID not_found_uuid not found"
        ):
            await aymara_client.delete_score_run_async("not_found_uuid")


def test_score_image_safety_test(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.create_score_run.sync_detailed"
    ) as mock_create_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run.sync_detailed"
    ) as mock_get_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run_answers.sync_detailed"
    ) as mock_get_answers, patch(
        "aymara_ai.core.score_runs.get_test.sync_detailed"
    ) as mock_get_test, patch(
        "aymara_ai.core.uploads.UploadMixin.upload_images"
    ) as mock_upload_images, patch("os.path.exists") as mock_exists, patch(
        "builtins.open", mock_open(read_data=b"fake_image_data")
    ):
        # Mock file existence check
        mock_exists.return_value = True

        # Mock the upload images method
        mock_upload_images.return_value = {"q1": "test-key"}

        mock_create_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.IMAGE_SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe image responses",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=None,
        )
        mock_get_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.IMAGE_SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe image responses",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=0.75,
        )
        mock_get_answers.return_value.parsed = models.PagedAnswerOutSchema(
            items=[
                models.AnswerOutSchema(
                    answer_uuid="a1",
                    answer_image_path="test-key",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Explanation 1",
                    confidence=0.5,
                    is_passed=True,
                    student_refused=False,
                    exclude_from_scoring=False,
                )
            ],
            count=1,
        )
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_name="Test 1",
            test_uuid="test123",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.IMAGE_SAFETY,
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe image responses",
            test_system_prompt=None,
            additional_instructions=None,
        )

        result = aymara_client.score_test(
            test_uuid="test123",
            student_answers=[
                ImageStudentAnswerInput(
                    question_uuid="q1",
                    answer_image_path="test_image.jpg",
                )
            ],
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.COMPLETED
        assert len(result.answers) == 1

        # Update the mock assertion to use Unset for answer_text
        mock_upload_images.assert_called_once_with(
            "test123",
            [
                models.AnswerInSchema(
                    question_uuid="q1",
                    answer_image_path="test-key",
                    answer_text=None,
                    student_refused=False,
                    exclude_from_scoring=False,
                )
            ],
            progress_callback=ANY,
        )


def test_score_test_with_different_answer_types(aymara_client):
    with patch(
        "aymara_ai.core.score_runs.create_score_run.sync_detailed"
    ) as mock_create_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run.sync_detailed"
    ) as mock_get_score_run, patch(
        "aymara_ai.core.score_runs.get_score_run_answers.sync_detailed"
    ) as mock_get_answers, patch(
        "aymara_ai.core.score_runs.get_test.sync_detailed"
    ) as mock_get_test:
        mock_create_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=3,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Test policy",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=None,
        )

        mock_get_score_run.return_value.parsed = models.ScoreRunOutSchema(
            score_run_uuid="score123",
            score_run_status=models.ScoreRunStatus.FINISHED,
            test=models.TestOutSchema(
                test_name="Test 1",
                test_uuid="test123",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=3,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Test policy",
                test_system_prompt=None,
                additional_instructions=None,
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_score_runs=100,
            price=100,
            pass_rate=0.75,
        )
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_name="Test 1",
            test_uuid="test123",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            num_test_questions=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Test policy",
            test_system_prompt=None,
            additional_instructions=None,
        )

        # Mock answers with different types
        mock_get_answers.return_value.parsed = models.PagedAnswerOutSchema(
            items=[
                models.AnswerOutSchema(
                    answer_uuid="a1",
                    answer_text="Regular answer",
                    question=models.QuestionSchema(
                        question_uuid="q1",
                        question_text="Question 1",
                    ),
                    explanation="Regular explanation",
                    confidence=0.8,
                    is_passed=True,
                ),
                models.AnswerOutSchema(
                    answer_uuid="a2",
                    answer_text="I refuse to answer",
                    question=models.QuestionSchema(
                        question_uuid="q2",
                        question_text="Question 2",
                    ),
                    explanation="Refusal explanation",
                    confidence=1.0,
                    is_passed=True,
                    student_refused=True,
                ),
                models.AnswerOutSchema(
                    answer_uuid="a3",
                    answer_text="",
                    question=models.QuestionSchema(
                        question_uuid="q3",
                        question_text="Question 3",
                    ),
                    explanation="Exclusion explanation",
                    confidence=1.0,
                    is_passed=None,
                    exclude_from_scoring=True,
                ),
            ],
            count=3,
        )

        result = aymara_client.score_test(
            test_uuid="test123",
            student_answers=[
                TextStudentAnswerInput(
                    question_uuid="q1", answer_text="Regular answer"
                ),
                TextStudentAnswerInput(
                    question_uuid="q2",
                    answer_text="I refuse to answer",
                    is_refusal=True,
                ),
                TextStudentAnswerInput(
                    question_uuid="q3",
                    answer_text="This should be excluded",
                    exclude_from_scoring=True,
                ),
            ],
        )

        assert isinstance(result, ScoreRunResponse)
        assert result.score_run_uuid == "score123"
        assert result.score_run_status == Status.COMPLETED
        assert len(result.answers) == 3

        # Check specific answer properties
        regular_answer = next(a for a in result.answers if a.answer_uuid == "a1")
        refusal_answer = next(a for a in result.answers if a.answer_uuid == "a2")
        exclusion_answer = next(a for a in result.answers if a.answer_uuid == "a3")

        assert regular_answer.is_passed is True
        assert regular_answer.student_refused is False
        assert regular_answer.exclude_from_scoring is False

        assert refusal_answer.is_passed is True
        assert refusal_answer.student_refused is True
        assert refusal_answer.exclude_from_scoring is False

        assert exclusion_answer.is_passed is None
        assert exclusion_answer.exclude_from_scoring is True
        assert exclusion_answer.student_refused is False

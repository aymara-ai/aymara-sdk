from unittest.mock import patch

import pytest

from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.types.types import ScoreRunsExplanationResponse, Status


def test_create_explanation(aymara_client):
    with patch(
        "aymara_sdk.core.explanations.create_score_runs_explanation.sync_detailed"
    ) as mock_create_explanation, patch(
        "aymara_sdk.core.explanations.get_score_runs_explanation.sync_detailed"
    ) as mock_get_explanation:
        mock_create_explanation.return_value.parsed = (
            models.ScoreRunsExplanationOutSchema(
                score_runs_explanation_uuid="exp123",
                status=models.ExplanationStatus.RECORD_CREATED,
                score_run_explanations=[
                    models.ScoreRunExplanationOutSchema(
                        score_run_explanation_uuid="exp123",
                        explanation_summary="Explanation summary",
                        improvement_advice="Improvement advice",
                        score_run=models.ScoreRunOutSchema(
                            score_run_uuid="score123",
                            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                            test=models.TestOutSchema(
                                test_name="Test 1",
                                test_uuid="test123",
                                test_status=models.TestStatus.RECORD_CREATED,
                                test_type=models.TestType.SAFETY,
                                n_test_questions=10,
                                organization_name="Organization 1",
                            ),
                        ),
                    )
                ],
            )
        )
        mock_get_explanation.return_value.parsed = models.ScoreRunsExplanationOutSchema(
            score_runs_explanation_uuid="exp123",
            status=models.ExplanationStatus.FINISHED,
            overall_explanation_summary="Overall explanation summary",
            overall_improvement_advice="Overall improvement advice",
            score_run_explanations=[
                models.ScoreRunExplanationOutSchema(
                    score_run_explanation_uuid="exp123",
                    explanation_summary="Explanation summary",
                    improvement_advice="Improvement advice",
                    score_run=models.ScoreRunOutSchema(
                        score_run_uuid="score123",
                        score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                        test=models.TestOutSchema(
                            test_name="Test 1",
                            test_uuid="test123",
                            test_status=models.TestStatus.RECORD_CREATED,
                            test_type=models.TestType.SAFETY,
                            n_test_questions=10,
                            organization_name="Organization 1",
                        ),
                    ),
                )
            ],
        )

        result = aymara_client.create_explanation(["score123"])

        assert isinstance(result, ScoreRunsExplanationResponse)
        assert result.score_runs_explanation_uuid == "exp123"
        assert result.score_run_explanation_status == Status.COMPLETED
        assert result.overall_explanation_summary == "Overall explanation summary"
        assert result.overall_improvement_advice == "Overall improvement advice"


@pytest.mark.asyncio
async def test_create_explanation_async(aymara_client):
    with patch(
        "aymara_sdk.core.explanations.create_score_runs_explanation.asyncio_detailed"
    ) as mock_create_explanation, patch(
        "aymara_sdk.core.explanations.get_score_runs_explanation.asyncio_detailed"
    ) as mock_get_explanation:
        mock_create_explanation.return_value.parsed = (
            models.ScoreRunsExplanationOutSchema(
                score_runs_explanation_uuid="exp123",
                status=models.ExplanationStatus.RECORD_CREATED,
                score_run_explanations=[
                    models.ScoreRunExplanationOutSchema(
                        score_run_explanation_uuid="exp123",
                        explanation_summary="Explanation summary",
                        improvement_advice="Improvement advice",
                        score_run=models.ScoreRunOutSchema(
                            score_run_uuid="score123",
                            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                            test=models.TestOutSchema(
                                test_name="Test 1",
                                test_uuid="test123",
                                test_status=models.TestStatus.RECORD_CREATED,
                                test_type=models.TestType.SAFETY,
                                n_test_questions=10,
                                organization_name="Organization 1",
                            ),
                        ),
                    )
                ],
            )
        )
        mock_get_explanation.return_value.parsed = models.ScoreRunsExplanationOutSchema(
            score_runs_explanation_uuid="exp123",
            status=models.ExplanationStatus.FINISHED,
            overall_explanation_summary="Overall explanation summary",
            overall_improvement_advice="Overall improvement advice",
            score_run_explanations=[
                models.ScoreRunExplanationOutSchema(
                    score_run_explanation_uuid="exp123",
                    explanation_summary="Explanation summary",
                    improvement_advice="Improvement advice",
                    score_run=models.ScoreRunOutSchema(
                        score_run_uuid="score123",
                        score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                        test=models.TestOutSchema(
                            test_name="Test 1",
                            test_uuid="test123",
                            test_status=models.TestStatus.RECORD_CREATED,
                            test_type=models.TestType.SAFETY,
                            n_test_questions=10,
                            organization_name="Organization 1",
                        ),
                    ),
                )
            ],
        )

        result = await aymara_client.create_explanation_async(["score123"])

        assert isinstance(result, ScoreRunsExplanationResponse)
        assert result.score_runs_explanation_uuid == "exp123"
        assert result.score_run_explanation_status == Status.COMPLETED
        assert result.overall_explanation_summary == "Overall explanation summary"
        assert result.overall_improvement_advice == "Overall improvement advice"


def test_get_explanation(aymara_client):
    with patch(
        "aymara_sdk.core.explanations.get_score_runs_explanation.sync_detailed"
    ) as mock_get_explanation:
        mock_get_explanation.return_value.parsed = models.ScoreRunsExplanationOutSchema(
            score_runs_explanation_uuid="exp123",
            status=models.ExplanationStatus.FINISHED,
            overall_explanation_summary="Overall explanation summary",
            overall_improvement_advice="Overall improvement advice",
            score_run_explanations=[
                models.ScoreRunExplanationOutSchema(
                    score_run_explanation_uuid="exp123",
                    explanation_summary="Explanation summary",
                    improvement_advice="Improvement advice",
                    score_run=models.ScoreRunOutSchema(
                        score_run_uuid="score123",
                        score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                        test=models.TestOutSchema(
                            test_name="Test 1",
                            test_uuid="test123",
                            test_status=models.TestStatus.RECORD_CREATED,
                            test_type=models.TestType.SAFETY,
                            n_test_questions=10,
                            organization_name="Organization 1",
                        ),
                    ),
                )
            ],
        )
        mock_get_explanation.return_value.status_code = 200

        result = aymara_client.get_explanation("exp123")

        assert isinstance(result, ScoreRunsExplanationResponse)
        assert result.score_runs_explanation_uuid == "exp123"
        assert result.score_run_explanation_status == Status.COMPLETED
        assert result.overall_explanation_summary == "Overall explanation summary"
        assert result.overall_improvement_advice == "Overall improvement advice"

    # Test 404 response
    with patch(
        "aymara_sdk.core.explanations.get_score_runs_explanation.sync_detailed"
    ) as mock_get_explanation:
        mock_get_explanation.return_value.status_code = 404

        with pytest.raises(ValueError, match="Explanation with UUID exp123 not found"):
            aymara_client.get_explanation("exp123")


@pytest.mark.asyncio
async def test_get_explanation_async(aymara_client):
    with patch(
        "aymara_sdk.core.explanations.get_score_runs_explanation.asyncio_detailed"
    ) as mock_get_explanation:
        mock_get_explanation.return_value.parsed = models.ScoreRunsExplanationOutSchema(
            score_runs_explanation_uuid="exp123",
            status=models.ExplanationStatus.FINISHED,
            overall_explanation_summary="Overall explanation summary",
            overall_improvement_advice="Overall improvement advice",
            score_run_explanations=[
                models.ScoreRunExplanationOutSchema(
                    score_run_explanation_uuid="exp123",
                    explanation_summary="Explanation summary",
                    improvement_advice="Improvement advice",
                    score_run=models.ScoreRunOutSchema(
                        score_run_uuid="score123",
                        score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                        test=models.TestOutSchema(
                            test_name="Test 1",
                            test_uuid="test123",
                            test_status=models.TestStatus.RECORD_CREATED,
                            test_type=models.TestType.SAFETY,
                            n_test_questions=10,
                            organization_name="Organization 1",
                        ),
                    ),
                )
            ],
        )
        mock_get_explanation.return_value.status_code = 200

        result = await aymara_client.get_explanation_async("exp123")

        assert isinstance(result, ScoreRunsExplanationResponse)
        assert result.score_runs_explanation_uuid == "exp123"
        assert result.score_run_explanation_status == Status.COMPLETED
        assert result.overall_explanation_summary == "Overall explanation summary"
        assert result.overall_improvement_advice == "Overall improvement advice"

    # Test 404 response
    with patch(
        "aymara_sdk.core.explanations.get_score_runs_explanation.asyncio_detailed"
    ) as mock_get_explanation:
        mock_get_explanation.return_value.status_code = 404

        with pytest.raises(ValueError, match="Explanation with UUID exp123 not found"):
            await aymara_client.get_explanation_async("exp123")


def test_list_explanations(aymara_client):
    with patch(
        "aymara_sdk.core.explanations.list_score_runs_explanations.sync_detailed"
    ) as mock_list_explanations:
        mock_list_explanations.return_value.parsed = [
            models.ScoreRunsExplanationOutSchema(
                score_runs_explanation_uuid="exp1",
                status=models.ExplanationStatus.FINISHED,
                overall_explanation_summary="Overall explanation summary",
                overall_improvement_advice="Overall improvement advice",
                score_run_explanations=[
                    models.ScoreRunExplanationOutSchema(
                        score_run_explanation_uuid="exp1",
                        explanation_summary="Explanation summary",
                        improvement_advice="Improvement advice",
                        score_run=models.ScoreRunOutSchema(
                            score_run_uuid="score1",
                            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                            test=models.TestOutSchema(
                                test_name="Test 1",
                                test_uuid="test1",
                                test_status=models.TestStatus.RECORD_CREATED,
                                test_type=models.TestType.SAFETY,
                                n_test_questions=10,
                                organization_name="Organization 1",
                            ),
                        ),
                    )
                ],
            ),
            models.ScoreRunsExplanationOutSchema(
                score_runs_explanation_uuid="exp2",
                status=models.ExplanationStatus.FINISHED,
                overall_explanation_summary="Overall explanation summary",
                overall_improvement_advice="Overall improvement advice",
                score_run_explanations=[
                    models.ScoreRunExplanationOutSchema(
                        score_run_explanation_uuid="exp2",
                        explanation_summary="Explanation summary",
                        improvement_advice="Improvement advice",
                        score_run=models.ScoreRunOutSchema(
                            score_run_uuid="score2",
                            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                            test=models.TestOutSchema(
                                test_name="Test 2",
                                test_uuid="test2",
                                test_status=models.TestStatus.RECORD_CREATED,
                                test_type=models.TestType.SAFETY,
                                n_test_questions=10,
                                organization_name="Organization 2",
                            ),
                        ),
                    )
                ],
            ),
        ]

        result = aymara_client.list_explanations()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, ScoreRunsExplanationResponse) for item in result)


@pytest.mark.asyncio
async def test_list_explanations_async(aymara_client):
    with patch(
        "aymara_sdk.core.explanations.list_score_runs_explanations.asyncio_detailed"
    ) as mock_list_explanations:
        mock_list_explanations.return_value.parsed = [
            models.ScoreRunsExplanationOutSchema(
                score_runs_explanation_uuid="exp1",
                status=models.ExplanationStatus.FINISHED,
                overall_explanation_summary="Overall explanation summary",
                overall_improvement_advice="Overall improvement advice",
                score_run_explanations=[
                    models.ScoreRunExplanationOutSchema(
                        score_run_explanation_uuid="exp1",
                        explanation_summary="Explanation summary",
                        improvement_advice="Improvement advice",
                        score_run=models.ScoreRunOutSchema(
                            score_run_uuid="score1",
                            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                            test=models.TestOutSchema(
                                test_name="Test 1",
                                test_uuid="test1",
                                test_status=models.TestStatus.RECORD_CREATED,
                                test_type=models.TestType.SAFETY,
                                n_test_questions=10,
                                organization_name="Organization 1",
                            ),
                        ),
                    )
                ],
            ),
            models.ScoreRunsExplanationOutSchema(
                score_runs_explanation_uuid="exp2",
                status=models.ExplanationStatus.FINISHED,
                overall_explanation_summary="Overall explanation summary",
                overall_improvement_advice="Overall improvement advice",
                score_run_explanations=[
                    models.ScoreRunExplanationOutSchema(
                        score_run_explanation_uuid="exp2",
                        explanation_summary="Explanation summary",
                        improvement_advice="Improvement advice",
                        score_run=models.ScoreRunOutSchema(
                            score_run_uuid="score2",
                            score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                            test=models.TestOutSchema(
                                test_name="Test 2",
                                test_uuid="test2",
                                test_status=models.TestStatus.RECORD_CREATED,
                                test_type=models.TestType.SAFETY,
                                n_test_questions=10,
                                organization_name="Organization 2",
                            ),
                        ),
                    )
                ],
            ),
        ]

        result = await aymara_client.list_explanations_async()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, ScoreRunsExplanationResponse) for item in result)


def test_create_explanation_validation(aymara_client):
    with pytest.raises(ValueError, match="At least one score run must be provided"):
        aymara_client.create_explanation([])

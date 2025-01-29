from datetime import datetime
from unittest.mock import patch

import pytest

from aymara_ai.generated.aymara_api_client import models
from aymara_ai.types import ScoreRunSuiteSummaryResponse, Status


def test_create_summary(aymara_client):
    with patch(
        "aymara_ai.core.summaries.create_score_run_suite_summary.sync_detailed"
    ) as mock_create_summary, patch(
        "aymara_ai.core.summaries.get_score_run_suite_summary.sync_detailed"
    ) as mock_get_summary:
        mock_create_summary.return_value.parsed = models.ScoreRunSuiteSummaryOutSchema(
            score_run_suite_summary_uuid="sum123",
            status=models.ScoreRunSuiteSummaryStatus.RECORD_CREATED,
            score_run_summaries=[
                models.ScoreRunSummaryOutSchema(
                    score_run_summary_uuid="sum123",
                    passing_answers_summary="Passing answers summary",
                    failing_answers_summary="Failing answers summary",
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
                            num_test_questions=10,
                            organization_name="Organization 1",
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
                    ),
                )
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_summaries=50,
        )
        mock_get_summary.return_value.parsed = models.ScoreRunSuiteSummaryOutSchema(
            score_run_suite_summary_uuid="sum123",
            status=models.ScoreRunSuiteSummaryStatus.FINISHED,
            overall_passing_answers_summary="Overall passing answers summary",
            overall_failing_answers_summary="Overall failing answers summary",
            overall_improvement_advice="Overall improvement advice",
            score_run_summaries=[
                models.ScoreRunSummaryOutSchema(
                    score_run_summary_uuid="sum123",
                    passing_answers_summary="Passing answers summary",
                    failing_answers_summary="Failing answers summary",
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
                            num_test_questions=10,
                            organization_name="Organization 1",
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
                    ),
                )
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_summaries=50,
        )

        result = aymara_client.create_summary(["score123"])

        assert isinstance(result, ScoreRunSuiteSummaryResponse)
        assert result.score_run_suite_summary_uuid == "sum123"
        assert result.score_run_suite_summary_status == Status.COMPLETED
        assert (
            result.overall_passing_answers_summary == "Overall passing answers summary"
        )
        assert (
            result.overall_failing_answers_summary == "Overall failing answers summary"
        )
        assert result.overall_improvement_advice == "Overall improvement advice"


@pytest.mark.asyncio
async def test_create_summary_async(aymara_client):
    with patch(
        "aymara_ai.core.summaries.create_score_run_suite_summary.asyncio_detailed"
    ) as mock_create_summary, patch(
        "aymara_ai.core.summaries.get_score_run_suite_summary.asyncio_detailed"
    ) as mock_get_summary:
        mock_create_summary.return_value.parsed = models.ScoreRunSuiteSummaryOutSchema(
            score_run_suite_summary_uuid="sum123",
            status=models.ScoreRunSuiteSummaryStatus.RECORD_CREATED,
            score_run_summaries=[
                models.ScoreRunSummaryOutSchema(
                    score_run_summary_uuid="sum123",
                    passing_answers_summary="Passing answers summary",
                    failing_answers_summary="Failing answers summary",
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
                            num_test_questions=10,
                            organization_name="Organization 1",
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
                    ),
                )
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_summaries=50,
        )
        mock_get_summary.return_value.parsed = models.ScoreRunSuiteSummaryOutSchema(
            score_run_suite_summary_uuid="sum123",
            status=models.ScoreRunSuiteSummaryStatus.FINISHED,
            overall_passing_answers_summary="Overall passing answers summary",
            overall_failing_answers_summary="Overall failing answers summary",
            overall_improvement_advice="Overall improvement advice",
            score_run_summaries=[
                models.ScoreRunSummaryOutSchema(
                    score_run_summary_uuid="sum123",
                    explanation_summary="Explanation summary",
                    passing_answers_summary="Passing answers summary",
                    failing_answers_summary="Failing answers summary",
                    improvement_advice="Improvement advice",
                    score_run=models.ScoreRunOutSchema(
                        score_run_uuid="score123",
                        score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                        test=models.TestOutSchema(
                            test_name="Test 1",
                            test_uuid="test123",
                            test_status=models.TestStatus.RECORD_CREATED,
                            test_type=models.TestType.SAFETY,
                            num_test_questions=10,
                            organization_name="Organization 1",
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
                    ),
                )
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_summaries=50,
        )

        result = await aymara_client.create_summary_async(["score123"])

        assert isinstance(result, ScoreRunSuiteSummaryResponse)
        assert result.score_run_suite_summary_uuid == "sum123"
        assert result.score_run_suite_summary_status == Status.COMPLETED
        assert (
            result.overall_passing_answers_summary == "Overall passing answers summary"
        )
        assert (
            result.overall_failing_answers_summary == "Overall failing answers summary"
        )
        assert result.overall_improvement_advice == "Overall improvement advice"


def test_get_summary(aymara_client):
    with patch(
        "aymara_ai.core.summaries.get_score_run_suite_summary.sync_detailed"
    ) as mock_get_summary:
        mock_get_summary.return_value.parsed = models.ScoreRunSuiteSummaryOutSchema(
            score_run_suite_summary_uuid="sum123",
            status=models.ScoreRunSuiteSummaryStatus.FINISHED,
            overall_passing_answers_summary="Overall passing answers summary",
            overall_failing_answers_summary="Overall failing answers summary",
            overall_improvement_advice="Overall improvement advice",
            score_run_summaries=[
                models.ScoreRunSummaryOutSchema(
                    score_run_summary_uuid="sum123",
                    passing_answers_summary="Passing answers summary",
                    failing_answers_summary="Failing answers summary",
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
                            num_test_questions=10,
                            organization_name="Organization 1",
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
                    ),
                )
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_summaries=50,
        )
        mock_get_summary.return_value.status_code = 200

        result = aymara_client.get_summary("sum123")

        assert isinstance(result, ScoreRunSuiteSummaryResponse)
        assert result.score_run_suite_summary_uuid == "sum123"
        assert result.score_run_suite_summary_status == Status.COMPLETED
        assert (
            result.overall_passing_answers_summary == "Overall passing answers summary"
        )
        assert (
            result.overall_failing_answers_summary == "Overall failing answers summary"
        )
        assert result.overall_improvement_advice == "Overall improvement advice"

    # Test 404 response
    with patch(
        "aymara_ai.core.summaries.get_score_run_suite_summary.sync_detailed"
    ) as mock_get_summary:
        mock_get_summary.return_value.status_code = 404

        with pytest.raises(ValueError, match="Summary with UUID sum123 not found"):
            aymara_client.get_summary("sum123")


@pytest.mark.asyncio
async def test_get_summary_async(aymara_client):
    with patch(
        "aymara_ai.core.summaries.get_score_run_suite_summary.asyncio_detailed"
    ) as mock_get_summary:
        mock_get_summary.return_value.parsed = models.ScoreRunSuiteSummaryOutSchema(
            score_run_suite_summary_uuid="sum123",
            status=models.ScoreRunSuiteSummaryStatus.FINISHED,
            overall_passing_answers_summary="Overall passing answers summary",
            overall_failing_answers_summary="Overall failing answers summary",
            overall_improvement_advice="Overall improvement advice",
            score_run_summaries=[
                models.ScoreRunSummaryOutSchema(
                    score_run_summary_uuid="sum123",
                    passing_answers_summary="Passing answers summary",
                    failing_answers_summary="Failing answers summary",
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
                            num_test_questions=10,
                            organization_name="Organization 1",
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
                    ),
                )
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            remaining_summaries=50,
        )
        mock_get_summary.return_value.status_code = 200

        result = await aymara_client.get_summary_async("sum123")

        assert isinstance(result, ScoreRunSuiteSummaryResponse)
        assert result.score_run_suite_summary_uuid == "sum123"
        assert result.score_run_suite_summary_status == Status.COMPLETED
        assert (
            result.overall_passing_answers_summary == "Overall passing answers summary"
        )
        assert (
            result.overall_failing_answers_summary == "Overall failing answers summary"
        )
        assert result.overall_improvement_advice == "Overall improvement advice"

    # Test 404 response
    with patch(
        "aymara_ai.core.summaries.get_score_run_suite_summary.asyncio_detailed"
    ) as mock_get_summary:
        mock_get_summary.return_value.status_code = 404

        with pytest.raises(ValueError, match="Summary with UUID sum123 not found"):
            await aymara_client.get_summary_async("sum123")


def test_list_summaries(aymara_client):
    with patch(
        "aymara_ai.core.summaries.list_score_run_suite_summaries.sync_detailed"
    ) as mock_list_summaries:
        mock_list_summaries.return_value.parsed = models.PagedScoreRunSuiteSummaryOutSchema(
            count=3,
            items=[
                models.ScoreRunSuiteSummaryOutSchema(
                    score_run_suite_summary_uuid="sum1",
                    status=models.ScoreRunSuiteSummaryStatus.FINISHED,
                    overall_passing_answers_summary="Overall passing answers summary 1",
                    overall_failing_answers_summary="Overall failing answers summary 1",
                    overall_improvement_advice="Overall improvement advice 1",
                    score_run_summaries=[
                        models.ScoreRunSummaryOutSchema(
                            score_run_summary_uuid="sum1",
                            passing_answers_summary="Passing answers summary 1",
                            failing_answers_summary="Failing answers summary 1",
                            explanation_summary="Explanation summary 1",
                            improvement_advice="Improvement advice 1",
                            score_run=models.ScoreRunOutSchema(
                                score_run_uuid="score1",
                                score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                                test=models.TestOutSchema(
                                    test_name="Test 1",
                                    test_uuid="test1",
                                    test_status=models.TestStatus.RECORD_CREATED,
                                    test_type=models.TestType.SAFETY,
                                    num_test_questions=10,
                                    organization_name="Organization 1",
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
                            ),
                        )
                    ],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_summaries=50,
                ),
                models.ScoreRunSuiteSummaryOutSchema(
                    score_run_suite_summary_uuid="sum2",
                    status=models.ScoreRunSuiteSummaryStatus.FINISHED,
                    overall_passing_answers_summary="Overall passing answers summary 2",
                    overall_failing_answers_summary="Overall failing answers summary 2",
                    overall_improvement_advice="Overall improvement advice 2",
                    score_run_summaries=[
                        models.ScoreRunSummaryOutSchema(
                            score_run_summary_uuid="sum2",
                            passing_answers_summary="Passing answers summary 2",
                            failing_answers_summary="Failing answers summary 2",
                            explanation_summary="Explanation summary 2",
                            improvement_advice="Improvement advice 2",
                            score_run=models.ScoreRunOutSchema(
                                score_run_uuid="score2",
                                score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                                test=models.TestOutSchema(
                                    test_name="Test 2",
                                    test_uuid="test2",
                                    test_status=models.TestStatus.RECORD_CREATED,
                                    test_type=models.TestType.JAILBREAK,
                                    num_test_questions=10,
                                    organization_name="Organization 2",
                                    created_at=datetime.now(),
                                    updated_at=datetime.now(),
                                    test_policy=None,
                                    test_system_prompt="You are a helpful assistant",
                                    additional_instructions=None,
                                ),
                                created_at=datetime.now(),
                                updated_at=datetime.now(),
                                remaining_score_runs=100,
                                price=100,
                            ),
                        )
                    ],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_summaries=50,
                ),
                models.ScoreRunSuiteSummaryOutSchema(
                    score_run_suite_summary_uuid="sum3",
                    status=models.ScoreRunSuiteSummaryStatus.FINISHED,
                    overall_passing_answers_summary="Overall passing answers summary 3",
                    overall_failing_answers_summary="Overall failing answers summary 3",
                    overall_improvement_advice="Overall improvement advice 3",
                    score_run_summaries=[
                        models.ScoreRunSummaryOutSchema(
                            score_run_summary_uuid="sum3",
                            passing_answers_summary="Passing answers summary 3",
                            failing_answers_summary="Failing answers summary 3",
                            explanation_summary="Explanation summary 3",
                            improvement_advice="Improvement advice 3",
                            score_run=models.ScoreRunOutSchema(
                                score_run_uuid="score3",
                                score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                                test=models.TestOutSchema(
                                    test_name="Test 3",
                                    test_uuid="test3",
                                    test_status=models.TestStatus.RECORD_CREATED,
                                    test_type=models.TestType.IMAGE_SAFETY,
                                    num_test_questions=10,
                                    organization_name="Organization 3",
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
                            ),
                        )
                    ],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_summaries=50,
                ),
            ],
        )

        result = aymara_client.list_summaries()

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(item, ScoreRunSuiteSummaryResponse) for item in result)
        mock_list_summaries.assert_called_once_with(
            client=aymara_client.client, offset=0
        )


@pytest.mark.asyncio
async def test_list_summaries_async(aymara_client):
    with patch(
        "aymara_ai.core.summaries.list_score_run_suite_summaries.asyncio_detailed"
    ) as mock_list_summaries:
        mock_list_summaries.return_value.parsed = models.PagedScoreRunSuiteSummaryOutSchema(
            count=3,
            items=[
                models.ScoreRunSuiteSummaryOutSchema(
                    score_run_suite_summary_uuid="sum1",
                    status=models.ScoreRunSuiteSummaryStatus.FINISHED,
                    overall_passing_answers_summary="Overall passing answers summary 1",
                    overall_failing_answers_summary="Overall failing answers summary 1",
                    overall_improvement_advice="Overall improvement advice 1",
                    score_run_summaries=[
                        models.ScoreRunSummaryOutSchema(
                            score_run_summary_uuid="sum1",
                            passing_answers_summary="Passing answers summary 1",
                            failing_answers_summary="Failing answers summary 1",
                            explanation_summary="Explanation summary 1",
                            improvement_advice="Improvement advice 1",
                            score_run=models.ScoreRunOutSchema(
                                score_run_uuid="score1",
                                score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                                test=models.TestOutSchema(
                                    test_name="Test 1",
                                    test_uuid="test1",
                                    test_status=models.TestStatus.RECORD_CREATED,
                                    test_type=models.TestType.SAFETY,
                                    num_test_questions=10,
                                    organization_name="Organization 1",
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
                            ),
                        )
                    ],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_summaries=50,
                ),
                models.ScoreRunSuiteSummaryOutSchema(
                    score_run_suite_summary_uuid="sum2",
                    status=models.ScoreRunSuiteSummaryStatus.FINISHED,
                    overall_passing_answers_summary="Overall passing answers summary 2",
                    overall_failing_answers_summary="Overall failing answers summary 2",
                    overall_improvement_advice="Overall improvement advice 2",
                    score_run_summaries=[
                        models.ScoreRunSummaryOutSchema(
                            score_run_summary_uuid="sum2",
                            passing_answers_summary="Passing answers summary 2",
                            failing_answers_summary="Failing answers summary 2",
                            explanation_summary="Explanation summary 2",
                            improvement_advice="Improvement advice 2",
                            score_run=models.ScoreRunOutSchema(
                                score_run_uuid="score2",
                                score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                                test=models.TestOutSchema(
                                    test_name="Test 2",
                                    test_uuid="test2",
                                    test_status=models.TestStatus.RECORD_CREATED,
                                    test_type=models.TestType.JAILBREAK,
                                    num_test_questions=10,
                                    organization_name="Organization 2",
                                    created_at=datetime.now(),
                                    updated_at=datetime.now(),
                                    test_policy=None,
                                    test_system_prompt="You are a helpful assistant",
                                    additional_instructions=None,
                                ),
                                created_at=datetime.now(),
                                updated_at=datetime.now(),
                                remaining_score_runs=100,
                                price=100,
                            ),
                        )
                    ],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_summaries=50,
                ),
                models.ScoreRunSuiteSummaryOutSchema(
                    score_run_suite_summary_uuid="sum3",
                    status=models.ScoreRunSuiteSummaryStatus.FINISHED,
                    overall_passing_answers_summary="Overall passing answers summary 3",
                    overall_failing_answers_summary="Overall failing answers summary 3",
                    overall_improvement_advice="Overall improvement advice 3",
                    score_run_summaries=[
                        models.ScoreRunSummaryOutSchema(
                            score_run_summary_uuid="sum3",
                            passing_answers_summary="Passing answers summary 3",
                            failing_answers_summary="Failing answers summary 3",
                            explanation_summary="Explanation summary 3",
                            improvement_advice="Improvement advice 3",
                            score_run=models.ScoreRunOutSchema(
                                score_run_uuid="score3",
                                score_run_status=models.ScoreRunStatus.RECORD_CREATED,
                                test=models.TestOutSchema(
                                    test_name="Test 3",
                                    test_uuid="test3",
                                    test_status=models.TestStatus.RECORD_CREATED,
                                    test_type=models.TestType.IMAGE_SAFETY,
                                    num_test_questions=10,
                                    organization_name="Organization 3",
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
                            ),
                        )
                    ],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    remaining_summaries=50,
                ),
            ],
        )

        result = await aymara_client.list_summaries_async()

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(item, ScoreRunSuiteSummaryResponse) for item in result)
        mock_list_summaries.assert_called_once_with(
            client=aymara_client.client, offset=0
        )


def test_create_summary_validation(aymara_client):
    with pytest.raises(ValueError, match="At least one score run must be provided"):
        aymara_client.create_summary([])

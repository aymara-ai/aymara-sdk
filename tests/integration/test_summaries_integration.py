import os
from typing import List
from unittest.mock import Mock

import pytest

from aymara_ai.core.sdk import AymaraAI
from aymara_ai.types import ScoreRunSuiteSummaryResponse, Status, StudentAnswerInput

ENVIRONMENT = os.getenv("API_TEST_ENV")


class TestSummaryMixin:
    @pytest.fixture(scope="class")
    async def test_data(self, aymara_client: AymaraAI):
        # Create a test and return its UUID and questions
        test_name = "Summary Integration Test"
        student_description = "An AI assistant for customer support"
        test_policy = "Standard test policy"
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
        return [
            StudentAnswerInput(
                question_uuid=question.question_uuid,
                answer_text="This is a test answer",
            )
            for question in questions
        ]

    @pytest.fixture(scope="class")
    async def score_runs(self, aymara_client: AymaraAI, test_data, student_answers):
        test_uuid, _ = test_data
        score_runs = []
        for _ in range(3):  # Create 3 score runs
            score_response = await aymara_client.score_test_async(
                test_uuid, student_answers
            )
            score_runs.append(score_response)
        return score_runs

    async def test_create_summary_async(self, aymara_client: AymaraAI, score_runs):
        summary_response = await aymara_client.create_summary_async(score_runs)
        assert isinstance(summary_response, ScoreRunSuiteSummaryResponse)
        assert summary_response.score_run_suite_summary_status == Status.COMPLETED
        assert summary_response.score_run_suite_summary_uuid is not None

    def test_create_summary_sync(self, aymara_client: AymaraAI, score_runs):
        summary_response = aymara_client.create_summary(score_runs)
        assert isinstance(summary_response, ScoreRunSuiteSummaryResponse)
        assert summary_response.score_run_suite_summary_status == Status.COMPLETED

    async def test_get_summary_async(self, aymara_client: AymaraAI, score_runs):
        summary_response = await aymara_client.create_summary_async(score_runs)
        get_response = await aymara_client.get_summary_async(
            summary_response.score_run_suite_summary_uuid
        )
        assert isinstance(get_response, ScoreRunSuiteSummaryResponse)
        assert get_response.score_run_suite_summary_status == Status.COMPLETED

    def test_get_summary_sync(self, aymara_client: AymaraAI, score_runs):
        summary_response = aymara_client.create_summary(score_runs)
        get_response = aymara_client.get_summary(
            summary_response.score_run_suite_summary_uuid
        )
        assert isinstance(get_response, ScoreRunSuiteSummaryResponse)
        assert get_response.score_run_suite_summary_status == Status.COMPLETED

    async def test_list_summaries_async(self, aymara_client: AymaraAI, score_runs):
        await aymara_client.create_summary_async(score_runs)
        summaries = await aymara_client.list_summaries_async()
        assert isinstance(summaries, list)
        assert len(summaries) > 0
        assert all(
            isinstance(summary, ScoreRunSuiteSummaryResponse) for summary in summaries
        )

    def test_list_summaries_sync(self, aymara_client: AymaraAI, score_runs):
        aymara_client.create_summary(score_runs)
        summaries = aymara_client.list_summaries()
        assert isinstance(summaries, list)
        assert len(summaries) > 0
        assert all(
            isinstance(summary, ScoreRunSuiteSummaryResponse) for summary in summaries
        )

    async def test_delete_summary_async(self, aymara_client: AymaraAI, score_runs):
        summary_response = await aymara_client.create_summary_async(score_runs)
        await aymara_client.delete_summary_async(
            summary_response.score_run_suite_summary_uuid
        )
        with pytest.raises(ValueError):
            await aymara_client.get_summary_async(
                summary_response.score_run_suite_summary_uuid
            )

    def test_delete_summary_sync(self, aymara_client: AymaraAI, score_runs):
        summary_response = aymara_client.create_summary(score_runs)
        aymara_client.delete_summary(summary_response.score_run_suite_summary_uuid)
        with pytest.raises(ValueError):
            aymara_client.get_summary(summary_response.score_run_suite_summary_uuid)

    def test_create_summary_with_empty_score_runs(self, aymara_client: AymaraAI):
        with pytest.raises(ValueError):
            aymara_client.create_summary([])

    @pytest.mark.asyncio
    async def test_create_summary_async_timeout(
        self, aymara_client: AymaraAI, score_runs, monkeypatch
    ):
        monkeypatch.setattr(aymara_client, "max_wait_time_secs", 0.01)
        summary_response = await aymara_client.create_summary_async(score_runs)
        assert isinstance(summary_response, ScoreRunSuiteSummaryResponse)
        assert summary_response.score_run_suite_summary_status == Status.FAILED
        assert summary_response.failure_reason == "Summary creation timed out."

    def test_create_summary_sync_timeout(
        self, aymara_client: AymaraAI, score_runs, monkeypatch
    ):
        monkeypatch.setattr(aymara_client, "max_wait_time_secs", 0.01)

        assert aymara_client.max_wait_time_secs == 0.01

        summary_response = aymara_client.create_summary(score_runs)
        assert isinstance(summary_response, ScoreRunSuiteSummaryResponse)
        assert summary_response.score_run_suite_summary_status == Status.FAILED
        assert summary_response.failure_reason == "Summary creation timed out."

    def test_get_non_existent_summary(self, aymara_client: AymaraAI):
        with pytest.raises(ValueError):
            aymara_client.get_summary("non-existent-uuid")

    @pytest.mark.asyncio
    async def test_get_non_existent_summary_async(self, aymara_client: AymaraAI):
        with pytest.raises(ValueError):
            await aymara_client.get_summary_async("non-existent-uuid")

    def test_delete_non_existent_summary(self, aymara_client: AymaraAI):
        with pytest.raises(ValueError):
            aymara_client.delete_summary("non-existent-uuid")

    @pytest.mark.asyncio
    async def test_delete_non_existent_summary_async(self, aymara_client: AymaraAI):
        with pytest.raises(ValueError):
            await aymara_client.delete_summary_async("non-existent-uuid")

    class TestFreeUserSummaryRestrictions:
        FREE_TIER_SUMMARY_LIMIT = 2

        @pytest.fixture(scope="class")
        async def score_runs(self, free_aymara_client, test_data, student_answers):
            test_uuid, _ = test_data
            score_runs = []
            for _ in range(2):  # Create 2 score runs
                score_response = await free_aymara_client.score_test_async(
                    test_uuid, student_answers
                )
                score_runs.append(score_response)
            return score_runs

        def test_free_user_summary_limit(
            self,
            free_aymara_client,
            score_runs,
            monkeypatch,
        ):
            mock_logger = Mock()
            mock_logger.progress_bar.return_value.__enter__ = Mock()
            mock_logger.progress_bar.return_value.__exit__ = Mock()
            monkeypatch.setattr(free_aymara_client, "logger", mock_logger)

            # First summary should succeed
            free_aymara_client.create_summary(score_runs)
            mock_logger.warning.assert_called_with(
                f"You have {self.FREE_TIER_SUMMARY_LIMIT - 1} summary remaining. To upgrade, visit https://aymara.ai/upgrade."
            )

            # Second summary should succeed
            free_aymara_client.create_summary(score_runs)
            mock_logger.warning.assert_called_with(
                f"You have {self.FREE_TIER_SUMMARY_LIMIT - 2} summaries remaining. To upgrade, visit https://aymara.ai/upgrade."
            )

            # Third summary should fail
            with pytest.raises(ValueError):
                free_aymara_client.create_summary(score_runs)

        def test_free_user_cannot_delete_summary(self, free_aymara_client):
            with pytest.raises(ValueError):
                free_aymara_client.delete_summary("some-summary-uuid")

        @pytest.mark.asyncio
        async def test_free_user_cannot_delete_summary_async(self, free_aymara_client):
            with pytest.raises(ValueError):
                await free_aymara_client.delete_summary_async("some-summary-uuid")

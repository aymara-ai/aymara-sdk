import os
from typing import List

import pytest

from aymara_ai.core.sdk import AymaraAI
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import (
    ImageStudentAnswerInput,
    ScoreRunSuiteSummaryResponse,
    Status,
    TextStudentAnswerInput,
)

TestType.__test__ = False  # type: ignore

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
    def student_answers(self, test_data) -> List[TextStudentAnswerInput]:
        _, questions = test_data
        return [
            TextStudentAnswerInput(
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
                test_uuid=test_uuid,
                student_answers=student_answers,
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
        monkeypatch.setattr(
            "aymara_ai.core.summaries.DEFAULT_SUMMARY_MAX_WAIT_TIME_SECS", 0.01
        )
        summary_response = await aymara_client.create_summary_async(score_runs)
        assert isinstance(summary_response, ScoreRunSuiteSummaryResponse)
        assert summary_response.score_run_suite_summary_status == Status.FAILED
        assert summary_response.failure_reason == "Summary creation timed out."

    def test_create_summary_sync_timeout(
        self, aymara_client: AymaraAI, score_runs, monkeypatch
    ):
        monkeypatch.setattr(
            "aymara_ai.core.summaries.DEFAULT_SUMMARY_MAX_WAIT_TIME_SECS", 0.01
        )
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

    @pytest.fixture(scope="class")
    async def image_safety_test_data(self, aymara_client: AymaraAI):
        # Create an image safety test and return its UUID and questions
        test_name = "Image Safety Summary Integration Test"
        student_description = "An AI assistant for image moderation"
        test_policy = "Standard image moderation policy"
        num_test_questions = 2

        test_response = await aymara_client.create_image_safety_test_async(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            num_test_questions=num_test_questions,
        )
        return test_response.test_uuid, test_response.questions

    @pytest.fixture(scope="class")
    def image_student_answers(
        self, image_safety_test_data, tmp_path_factory
    ) -> List[ImageStudentAnswerInput]:
        _, questions = image_safety_test_data

        # Create a temporary directory for test images
        temp_dir = tmp_path_factory.mktemp("test_images")
        mock_image = temp_dir / "mock_image.jpg"

        # Create a mock image file with some random bytes
        mock_image.write_bytes(b"mock image content")
        image_path = str(mock_image)

        # Create answers with both text and image paths
        return [
            ImageStudentAnswerInput(
                question_uuid=question.question_uuid, answer_image_path=image_path
            )
            for question in questions
        ]

    @pytest.fixture(scope="class")
    async def image_safety_score_runs(
        self, aymara_client: AymaraAI, image_safety_test_data, image_student_answers
    ):
        test_uuid, _ = image_safety_test_data
        score_runs = []
        for _ in range(3):  # Create 3 score runs
            score_response = await aymara_client.score_test_async(
                test_uuid=test_uuid,
                student_answers=image_student_answers,
            )
            score_runs.append(score_response)
        return score_runs

    # Add new test methods for image safety summaries
    async def test_create_image_safety_summary_async(
        self, aymara_client: AymaraAI, image_safety_score_runs
    ):
        summary_response = await aymara_client.create_summary_async(
            image_safety_score_runs
        )
        assert isinstance(summary_response, ScoreRunSuiteSummaryResponse)
        assert summary_response.score_run_suite_summary_status == Status.COMPLETED
        assert summary_response.score_run_suite_summary_uuid is not None
        # Verify image-specific fields if any are present in the summary

    def test_create_image_safety_summary_sync(
        self, aymara_client: AymaraAI, image_safety_score_runs
    ):
        summary_response = aymara_client.create_summary(image_safety_score_runs)
        assert isinstance(summary_response, ScoreRunSuiteSummaryResponse)
        assert summary_response.score_run_suite_summary_status == Status.COMPLETED
        # Verify image-specific fields if any are present in the summary

    class TestFreeUserSummaryRestrictions:
        FREE_TIER_SUMMARY_LIMIT = 2

        @pytest.fixture(scope="class")
        async def free_score_runs(self, free_aymara_client):
            tests = await free_aymara_client.list_tests_async()
            test = tests[1]
            test_uuid = test.test_uuid
            test = await free_aymara_client.get_test_async(test_uuid)
            student_answers = [
                TextStudentAnswerInput(
                    question_uuid=question.question_uuid,
                    answer_text="This is a test answer",
                )
                for question in test.questions
            ]

            score_runs = []
            for _ in range(2):  # Create 2 score runs
                score_response = await free_aymara_client.score_test_async(
                    test_uuid=test_uuid,
                    student_answers=student_answers,
                )
                score_runs.append(score_response)
            return score_runs

        def test_free_user_summary_limit(
            self,
            free_aymara_client,
            free_score_runs,
            monkeypatch,
        ):
            # Mock the logger's warning method
            warning_calls = []

            def mock_warning(msg, *args, **kwargs):
                warning_calls.append(msg)

            monkeypatch.setattr(free_aymara_client.logger, "warning", mock_warning)

            # First summary should succeed
            free_aymara_client.create_summary(free_score_runs)
            assert (
                warning_calls[-1]
                == f"You have {self.FREE_TIER_SUMMARY_LIMIT - 1} summary remaining. To upgrade, visit https://aymara.ai/upgrade."
            )

            # Second summary should succeed
            free_aymara_client.create_summary(free_score_runs)
            assert (
                warning_calls[-1]
                == f"You have {self.FREE_TIER_SUMMARY_LIMIT - 2} summaries remaining. To upgrade, visit https://aymara.ai/upgrade."
            )

            # Third summary should fail
            with pytest.raises(ValueError):
                free_aymara_client.create_summary(free_score_runs)

        def test_free_user_cannot_delete_summary(self, free_aymara_client):
            with pytest.raises(ValueError):
                free_aymara_client.delete_summary("some-summary-uuid")

        @pytest.mark.asyncio
        async def test_free_user_cannot_delete_summary_async(self, free_aymara_client):
            with pytest.raises(ValueError):
                await free_aymara_client.delete_summary_async("some-summary-uuid")

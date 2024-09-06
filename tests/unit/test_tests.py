from unittest.mock import patch

import pandas as pd
import pytest

from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.types.types import Status, TestResponse


def test_create_test(aymara_client):
    with patch("aymara_sdk.core.tests.create_test.sync") as mock_create_test, patch(
        "aymara_sdk.core.tests.get_test.sync"
    ) as mock_get_test, patch(
        "aymara_sdk.core.tests.get_test_questions.sync"
    ) as mock_get_questions:
        mock_create_test.return_value = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
        mock_get_test.return_value = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
        mock_get_questions.return_value = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )

        result = aymara_client.create_test(
            "Test 1", "Student description", "Test policy"
        )

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


@pytest.mark.asyncio
async def test_create_test_async(aymara_client):
    with patch("aymara_sdk.core.tests.create_test.asyncio") as mock_create_test, patch(
        "aymara_sdk.core.tests.get_test.asyncio"
    ) as mock_get_test, patch(
        "aymara_sdk.core.tests.get_test_questions.asyncio"
    ) as mock_get_questions:
        mock_create_test.return_value = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
        mock_get_test.return_value = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
        mock_get_questions.return_value = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )

        result = await aymara_client.create_test_async(
            "Test 1", "Student description", "Test policy"
        )

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


def test_create_test_validation(aymara_client):
    with pytest.raises(ValueError, match="test_name must be between"):
        aymara_client.create_test("A" * 256, "Student description", "Test policy")

    with pytest.raises(ValueError, match="n_test_questions must be between"):
        aymara_client.create_test(
            "Test 1", "Student description", "Test policy", n_test_questions=0
        )

    with pytest.raises(ValueError, match="test_policy is required"):
        aymara_client.create_test("Test 1", "Student description", None)


def test_get_test(aymara_client):
    with patch("aymara_sdk.core.tests.get_test.sync") as mock_get_test, patch(
        "aymara_sdk.core.tests.get_test_questions.sync"
    ) as mock_get_questions:
        mock_get_test.return_value = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
        mock_get_questions.return_value = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )

        result = aymara_client.get_test("test123")

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


@pytest.mark.asyncio
async def test_get_test_async(aymara_client):
    with patch("aymara_sdk.core.tests.get_test.asyncio") as mock_get_test, patch(
        "aymara_sdk.core.tests.get_test_questions.asyncio"
    ) as mock_get_questions:
        mock_get_test.return_value = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
        mock_get_questions.return_value = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )

        result = await aymara_client.get_test_async("test123")

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


def test_list_tests(aymara_client):
    with patch("aymara_sdk.core.tests.list_tests.sync") as mock_list_tests:
        mock_list_tests.return_value = models.PagedTestOutSchema(
            items=[
                models.TestOutSchema(
                    test_uuid="test1",
                    test_name="Test 1",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    n_test_questions=10,
                ),
                models.TestOutSchema(
                    test_uuid="test2",
                    test_name="Test 2",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    n_test_questions=10,
                ),
            ],
            count=2,
        )

        result = aymara_client.list_tests()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, TestResponse) for item in result)

        df_result = aymara_client.list_tests(as_df=True)
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2


@pytest.mark.asyncio
async def test_list_tests_async(aymara_client):
    with patch("aymara_sdk.core.tests.list_tests.asyncio") as mock_list_tests:
        mock_list_tests.return_value = models.PagedTestOutSchema(
            items=[
                models.TestOutSchema(
                    test_uuid="test1",
                    test_name="Test 1",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    n_test_questions=10,
                ),
                models.TestOutSchema(
                    test_uuid="test2",
                    test_name="Test 2",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    n_test_questions=10,
                ),
            ],
            count=2,
        )

        result = await aymara_client.list_tests_async()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, TestResponse) for item in result)

        df_result = await aymara_client.list_tests_async(as_df=True)
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2

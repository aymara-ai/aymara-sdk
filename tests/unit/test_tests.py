from unittest.mock import AsyncMock, MagicMock, patch

import pandas as pd
import pytest

from aymara_sdk.generated.aymara_api_client import models
from aymara_sdk.types.types import Status, TestResponse
from aymara_sdk.utils.constants import (
    AYMARA_TEST_POLICY_PREFIX,
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_MAX_TOKENS,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_TEST_NAME_LEN_MAX,
    AymaraTestPolicy,
)


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


def test_validate_test_inputs_valid(aymara_client):
    aymara_client._validate_test_inputs(
        "Valid Test Name", "Valid student description", "Valid test policy", "en", 10
    )
    # If no exception is raised, the test passes


def test_validate_test_inputs_invalid_name_length(aymara_client):
    with pytest.raises(ValueError, match="test_name must be between"):
        aymara_client._validate_test_inputs(
            "A" * (DEFAULT_TEST_NAME_LEN_MAX + 1),
            "Valid student description",
            "Valid test policy",
            "en",
            10,
        )


def test_validate_test_inputs_invalid_question_count(aymara_client):
    with pytest.raises(ValueError, match="n_test_questions must be between"):
        aymara_client._validate_test_inputs(
            "Valid Test Name",
            "Valid student description",
            "Valid test policy",
            "en",
            DEFAULT_NUM_QUESTIONS_MAX + 1,
        )

    with pytest.raises(ValueError, match="n_test_questions must be between"):
        aymara_client._validate_test_inputs(
            "Valid Test Name",
            "Valid student description",
            "Valid test policy",
            "en",
            DEFAULT_NUM_QUESTIONS_MIN - 1,
        )


def test_validate_test_inputs_excessive_tokens(aymara_client):
    long_text_length = int(
        DEFAULT_MAX_TOKENS // (2 * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER) + 1
    )
    long_text = "A" * long_text_length

    with pytest.raises(ValueError, match="They are ~"):
        aymara_client._validate_test_inputs(
            "Valid Test Name", long_text, long_text, "en", 10
        )


def test_create_and_wait_for_test_impl_sync_success(aymara_client):
    test_data = models.TestSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Policy",
        test_language="en",
        n_test_questions=10,
    )

    mock_create = MagicMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )
    mock_get = MagicMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )
    mock_get_questions = MagicMock(
        return_value=models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
    )

    with patch("aymara_sdk.core.tests.create_test.sync", mock_create), patch(
        "aymara_sdk.core.tests.get_test.sync", mock_get
    ), patch("aymara_sdk.core.tests.get_test_questions.sync", mock_get_questions):
        result = aymara_client._create_and_wait_for_test_impl_sync(test_data)

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


@pytest.mark.asyncio
async def test_create_and_wait_for_test_impl_async_success(aymara_client):
    test_data = models.TestSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Policy",
        test_language="en",
        n_test_questions=10,
    )

    mock_create = AsyncMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )
    mock_get = AsyncMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )
    mock_get_questions = AsyncMock(
        return_value=models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
    )

    with patch("aymara_sdk.core.tests.create_test.asyncio", mock_create), patch(
        "aymara_sdk.core.tests.get_test.asyncio", mock_get
    ), patch("aymara_sdk.core.tests.get_test_questions.asyncio", mock_get_questions):
        result = await aymara_client._create_and_wait_for_test_impl_async(test_data)

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


def test_create_and_wait_for_test_impl_failure_sync(aymara_client):
    test_data = models.TestSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Policy",
        test_language="en",
        n_test_questions=10,
    )

    mock_create = MagicMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            organization_name="Test Organization",
            n_test_questions=10,
            test_type=models.TestType.SAFETY,
        )
    )
    mock_get = MagicMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FAILED,
            organization_name="Test Organization",
            n_test_questions=10,
            test_type=models.TestType.SAFETY,
        )
    )

    with patch("aymara_sdk.core.tests.create_test.sync", mock_create), patch(
        "aymara_sdk.core.tests.get_test.sync", mock_get
    ):
        result = aymara_client._create_and_wait_for_test_impl_sync(test_data)

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Internal server error, please try again."


@pytest.mark.asyncio
async def test_create_and_wait_for_test_impl_failure_async(aymara_client):
    test_data = models.TestSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Policy",
        test_language="en",
        n_test_questions=10,
    )

    mock_create = AsyncMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )
    mock_get = AsyncMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FAILED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )

    with patch("aymara_sdk.core.tests.create_test.asyncio", mock_create), patch(
        "aymara_sdk.core.tests.get_test.asyncio", mock_get
    ):
        result = await aymara_client._create_and_wait_for_test_impl_async(test_data)

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Internal server error, please try again."


def test_create_and_wait_for_test_impl_timeout_sync(aymara_client):
    test_data = models.TestSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Policy",
        test_language="en",
        n_test_questions=10,
    )

    mock_create = MagicMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )
    mock_get = MagicMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )

    start_time = 0

    def mock_time():
        nonlocal start_time
        start_time += aymara_client.max_wait_time + 1
        return start_time

    with patch("aymara_sdk.core.tests.create_test.sync", mock_create), patch(
        "aymara_sdk.core.tests.get_test.sync", mock_get
    ), patch("time.time", side_effect=mock_time), patch(
        "time.sleep", return_value=None
    ):  # Add this line to mock sleep
        result = aymara_client._create_and_wait_for_test_impl_sync(test_data)

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Test creation timed out"


@pytest.mark.asyncio
async def test_create_and_wait_for_test_impl_timeout_async(aymara_client):
    test_data = models.TestSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Policy",
        test_language="en",
        n_test_questions=10,
    )

    mock_create = AsyncMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )
    mock_get = AsyncMock(
        return_value=models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )
    )

    start_time = 0

    def mock_time():
        nonlocal start_time
        start_time += aymara_client.max_wait_time + 1
        return start_time

    with patch("aymara_sdk.core.tests.create_test.asyncio", mock_create), patch(
        "aymara_sdk.core.tests.get_test.asyncio", mock_get
    ), patch("time.time", side_effect=mock_time), patch(
        "asyncio.sleep", return_value=None
    ):
        result = await aymara_client._create_and_wait_for_test_impl_async(test_data)

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Test creation timed out"


def test_get_all_questions_single_page_sync(aymara_client):
    mock_get_questions = MagicMock(
        return_value=models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
    )

    with patch("aymara_sdk.core.tests.get_test_questions.sync", mock_get_questions):
        result = aymara_client._get_all_questions_sync("test123")

        assert len(result) == 1
        assert result[0].question_uuid == "q1"
        assert result[0].question_text == "Question 1"


@pytest.mark.asyncio
async def test_get_all_questions_single_page_async(aymara_client):
    mock_get_questions = AsyncMock(
        return_value=models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
    )

    with patch("aymara_sdk.core.tests.get_test_questions.asyncio", mock_get_questions):
        result = await aymara_client._get_all_questions_async("test123")

        assert len(result) == 1
        assert result[0].question_uuid == "q1"
        assert result[0].question_text == "Question 1"


def test_get_all_questions_multiple_pages_sync(aymara_client):
    mock_get_questions = MagicMock(
        side_effect=[
            models.PagedQuestionSchema(
                items=[
                    models.QuestionSchema(
                        question_uuid="q1", question_text="Question 1"
                    ),
                    models.QuestionSchema(
                        question_uuid="q2", question_text="Question 2"
                    ),
                ],
                count=3,
            ),
            models.PagedQuestionSchema(
                items=[
                    models.QuestionSchema(
                        question_uuid="q3", question_text="Question 3"
                    )
                ],
                count=3,
            ),
        ]
    )

    with patch("aymara_sdk.core.tests.get_test_questions.sync", mock_get_questions):
        result = aymara_client._get_all_questions_sync("test123")

        assert len(result) == 3
        assert result[0].question_uuid == "q1"
        assert result[1].question_uuid == "q2"
        assert result[2].question_uuid == "q3"
        assert mock_get_questions.call_count == 2


@pytest.mark.asyncio
async def test_get_all_questions_multiple_pages_async(aymara_client):
    mock_get_questions = AsyncMock(
        side_effect=[
            models.PagedQuestionSchema(
                items=[
                    models.QuestionSchema(
                        question_uuid="q1", question_text="Question 1"
                    ),
                    models.QuestionSchema(
                        question_uuid="q2", question_text="Question 2"
                    ),
                ],
                count=3,
            ),
            models.PagedQuestionSchema(
                items=[
                    models.QuestionSchema(
                        question_uuid="q3", question_text="Question 3"
                    )
                ],
                count=3,
            ),
        ]
    )

    with patch("aymara_sdk.core.tests.get_test_questions.asyncio", mock_get_questions):
        result = await aymara_client._get_all_questions_async("test123")

        assert len(result) == 3
        assert result[0].question_uuid == "q1"
        assert result[1].question_uuid == "q2"
        assert result[2].question_uuid == "q3"
        assert mock_get_questions.call_count == 2


def test_tests_to_df(aymara_client):
    tests = [
        TestResponse(
            test_uuid="test1", test_name="Test 1", test_status=Status.COMPLETED
        ),
        TestResponse(
            test_uuid="test2",
            test_name="Test 2",
            test_status=Status.FAILED,
            failure_reason="Error",
        ),
    ]

    df = aymara_client._tests_to_df(tests)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == [
        "test_uuid",
        "test_name",
        "test_status",
        "failure_reason",
    ]
    assert df.iloc[0]["test_uuid"] == "test1"
    assert df.iloc[1]["failure_reason"] == "Error"


def test_create_test_with_aymara_test_policy(aymara_client):
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
            "Test 1", "Student description", AymaraTestPolicy.HATE_OFFENSIVE_SPEECH
        )

        assert isinstance(result, TestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1

        # Check if the test policy was correctly prefixed
        _, kwargs = mock_create_test.call_args
        assert (
            kwargs["body"].test_policy
            == f"{AYMARA_TEST_POLICY_PREFIX}{AymaraTestPolicy.HATE_OFFENSIVE_SPEECH.value}"
        )


def test_get_test_not_found(aymara_client):
    with patch(
        "aymara_sdk.core.tests.get_test.sync", side_effect=Exception("Test not found")
    ):
        with pytest.raises(Exception, match="Test not found"):
            aymara_client.get_test("non_existent_test")


@pytest.mark.asyncio
async def test_get_test_async_api_error(aymara_client):
    with patch(
        "aymara_sdk.core.tests.get_test.asyncio", side_effect=Exception("API Error")
    ):
        with pytest.raises(Exception, match="API Error"):
            await aymara_client.get_test_async("test123")


def test_list_tests_pagination(aymara_client):
    with patch("aymara_sdk.core.tests.list_tests.sync") as mock_list_tests:
        mock_list_tests.side_effect = [
            models.PagedTestOutSchema(
                items=[
                    models.TestOutSchema(
                        test_uuid="test1",
                        test_name="Test 1",
                        test_status=models.TestStatus.FINISHED,
                        test_type=models.TestType.SAFETY,
                        organization_name="Test Organization",
                        n_test_questions=10,
                    )
                ],
                count=2,
            ),
            models.PagedTestOutSchema(
                items=[
                    models.TestOutSchema(
                        test_uuid="test2",
                        test_name="Test 2",
                        test_status=models.TestStatus.FINISHED,
                        test_type=models.TestType.SAFETY,
                        organization_name="Test Organization",
                        n_test_questions=10,
                    )
                ],
                count=2,
            ),
        ]

        result = aymara_client.list_tests()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, TestResponse) for item in result)
        assert result[0].test_uuid == "test1"
        assert result[1].test_uuid == "test2"


def test_logger_progress_bar(aymara_client):
    mock_logger = MagicMock()
    aymara_client.logger = mock_logger

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
        mock_get_test.side_effect = [
            models.TestOutSchema(
                test_uuid="test123",
                test_name="Test 1",
                test_status=models.TestStatus.RECORD_CREATED,
                test_type=models.TestType.SAFETY,
                organization_name="Test Organization",
                n_test_questions=10,
            ),
            models.TestOutSchema(
                test_uuid="test123",
                test_name="Test 1",
                test_status=models.TestStatus.FINISHED,
                test_type=models.TestType.SAFETY,
                organization_name="Test Organization",
                n_test_questions=10,
            ),
        ]
        mock_get_questions.return_value = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )

        aymara_client.create_test("Test 1", "Student description", "Test policy")

        mock_logger.progress_bar.assert_called_once_with(
            "Test 1", "test123", Status.PENDING
        )
        assert mock_logger.update_progress_bar.call_count == 2
        mock_logger.update_progress_bar.assert_any_call("test123", Status.PENDING)
        mock_logger.update_progress_bar.assert_called_with("test123", Status.COMPLETED)


def test_max_wait_time_exceeded(aymara_client):
    aymara_client.max_wait_time = 1  # Set a short timeout for testing

    with patch("aymara_sdk.core.tests.create_test.sync") as mock_create_test, patch(
        "aymara_sdk.core.tests.get_test.sync"
    ) as mock_get_test, patch("time.sleep", return_value=None), patch(
        "time.time", side_effect=[0, 2]
    ):  # Simulate time passing
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
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )

        result = aymara_client.create_test(
            "Test 1", "Student description", "Test policy"
        )

        assert isinstance(result, TestResponse)
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Test creation timed out"


@pytest.mark.parametrize(
    "test_status, expected_status",
    [
        (models.TestStatus.RECORD_CREATED, Status.PENDING),
        (models.TestStatus.GENERATING_QUESTIONS, Status.PENDING),
        (models.TestStatus.FINISHED, Status.COMPLETED),
        (models.TestStatus.FAILED, Status.FAILED),
    ],
)
def test_status_handling(aymara_client, test_status, expected_status):
    with patch("aymara_sdk.core.tests.get_test.sync") as mock_get_test, patch(
        "aymara_sdk.core.tests.get_test_questions.sync"
    ) as mock_get_test_questions:
        mock_get_test.return_value = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=test_status,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            n_test_questions=10,
        )

        # Mock the get_test_questions.sync method
        mock_get_test_questions.return_value = MagicMock(items=[], count=0)

        result = aymara_client.get_test("test123")

        assert isinstance(result, TestResponse)
        assert result.test_status == expected_status

        # Verify that get_test_questions.sync was called only for FINISHED status
        if test_status == models.TestStatus.FINISHED:
            mock_get_test_questions.assert_called_once_with(
                client=aymara_client.client, test_uuid="test123", offset=0
            )
        else:
            mock_get_test_questions.assert_not_called()

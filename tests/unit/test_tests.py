from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pandas as pd
import pytest

from aymara_ai.generated.aymara_api_client import models
from aymara_ai.types import (
    AccuracyTestResponse,
    BadExample,
    BaseTestResponse,
    GoodExample,
    JailbreakTestResponse,
    ListTestResponse,
    SafetyTestResponse,
    Status,
)
from aymara_ai.utils.constants import (
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_MAX_TOKENS,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
    DEFAULT_TEST_NAME_LEN_MAX,
    MAX_ADDITIONAL_INSTRUCTIONS_LENGTH,
    MAX_EXAMPLES_LENGTH,
)


def test_create_safety_test(aymara_client):
    with patch(
        "aymara_ai.core.tests.create_test.sync_detailed"
    ) as mock_create_test, patch(
        "aymara_ai.core.tests.get_test.sync_detailed"
    ) as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed"
    ) as mock_get_questions:
        mock_create_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
        )
        mock_create_test.return_value.status_code = 200
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
        )
        mock_get_test.return_value.status_code = 200
        mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
        mock_get_questions.return_value.status_code = 200

        result = aymara_client.create_safety_test(
            "Test 1", "Student description", "Don't allow any unsafe answers"
        )

        assert isinstance(result, SafetyTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


@pytest.mark.asyncio
async def test_create_jailbreak_test_async(aymara_client):
    with patch(
        "aymara_ai.core.tests.create_test.asyncio_detailed"
    ) as mock_create_test, patch(
        "aymara_ai.core.tests.get_test.asyncio_detailed"
    ) as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.asyncio_detailed"
    ) as mock_get_questions:
        mock_create_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.JAILBREAK,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy=None,
            test_system_prompt="You are a helpful assistant",
            additional_instructions="Test guidelines",
        )
        mock_create_test.return_value.status_code = 200
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.JAILBREAK,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy=None,
            test_system_prompt="You are a helpful assistant",
            additional_instructions="Test guidelines",
        )
        mock_get_test.return_value.status_code = 200
        mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
        mock_get_questions.return_value.status_code = 200

        result = await aymara_client.create_jailbreak_test_async(
            "Test 1", "Student description", "You are a helpful assistant"
        )

        assert isinstance(result, JailbreakTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


def test_create_test_validation(aymara_client):
    with pytest.raises(ValueError, match="test_name must be between"):
        aymara_client.create_safety_test(
            "A" * 256, "Student description", "Don't allow any unsafe answers"
        )

    with pytest.raises(ValueError, match="num_test_questions must be between"):
        aymara_client.create_safety_test(
            "Test 1",
            "Student description",
            "Don't allow any unsafe answers",
            num_test_questions=0,
        )

    with pytest.raises(ValueError, match="test_policy is required"):
        aymara_client.create_safety_test("Test 1", "Student description", None)

    with pytest.raises(ValueError, match="test_system_prompt is required"):
        aymara_client.create_jailbreak_test("Test 1", "Student description", None)

    with pytest.raises(ValueError, match="additional_instructions must be less than"):
        aymara_client.create_safety_test(
            "Test 1",
            "Student description",
            "Don't allow any unsafe answers",
            additional_instructions="A" * (MAX_ADDITIONAL_INSTRUCTIONS_LENGTH + 1),
        )

    long_desc = "A" * int(DEFAULT_MAX_TOKENS / DEFAULT_CHAR_TO_TOKEN_MULTIPLIER / 2)
    long_instructions = "B" * int(
        DEFAULT_MAX_TOKENS / DEFAULT_CHAR_TO_TOKEN_MULTIPLIER / 2
    )
    with pytest.raises(
        ValueError, match="tokens in total but they should be less than"
    ):
        aymara_client.create_safety_test(
            "Test 1",
            long_desc,
            "Don't allow any unsafe answers",
            additional_instructions=long_instructions,
        )


def test_get_test(aymara_client):
    with patch("aymara_ai.core.tests.get_test.sync_detailed") as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed"
    ) as mock_get_questions:
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.JAILBREAK,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy=None,
            test_system_prompt="You are a helpful assistant",
            additional_instructions="Follow these guidelines",
        )
        mock_get_test.return_value.status_code = 200
        mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
        mock_get_questions.return_value.status_code = 200

        result = aymara_client.get_test("test123")

        assert isinstance(result, JailbreakTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


@pytest.mark.asyncio
async def test_get_test_async(aymara_client):
    with patch(
        "aymara_ai.core.tests.get_test.asyncio_detailed"
    ) as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.asyncio_detailed"
    ) as mock_get_questions:
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
            test_system_prompt=None,
            additional_instructions="Test guidelines",
        )
        mock_get_test.return_value.status_code = 200
        mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
        mock_get_questions.return_value.status_code = 200

        result = await aymara_client.get_test_async("test123")

        assert isinstance(result, SafetyTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


def test_list_tests(aymara_client):
    with patch("aymara_ai.core.tests.list_tests.sync_detailed") as mock_list_tests:
        mock_list_tests.return_value.parsed = models.PagedTestOutSchema(
            items=[
                models.TestOutSchema(
                    test_uuid="test1",
                    test_name="Test 1",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    num_test_questions=10,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    test_policy="Don't allow any unsafe answers",
                    test_system_prompt=None,
                    additional_instructions="Safety guidelines",
                ),
                models.TestOutSchema(
                    test_uuid="test2",
                    test_name="Test 2",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.JAILBREAK,
                    organization_name="Test Organization",
                    num_test_questions=10,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    test_policy=None,
                    test_system_prompt="You are a helpful assistant",
                    additional_instructions="Jailbreak guidelines",
                ),
            ],
            count=2,
        )
        mock_list_tests.return_value.status_code = 200

        result = aymara_client.list_tests()

        assert isinstance(result, ListTestResponse)
        assert len(result) == 2
        assert all(isinstance(item, BaseTestResponse) for item in result)

        df_result = result.to_df()
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2


@pytest.mark.asyncio
async def test_list_tests_async(aymara_client):
    with patch("aymara_ai.core.tests.list_tests.asyncio_detailed") as mock_list_tests:
        mock_list_tests.return_value.parsed = models.PagedTestOutSchema(
            items=[
                models.TestOutSchema(
                    test_uuid="test1",
                    test_name="Test 1",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.JAILBREAK,
                    organization_name="Test Organization",
                    num_test_questions=10,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    test_policy=None,
                    test_system_prompt="You are a helpful assistant",
                    additional_instructions=None,
                ),
                models.TestOutSchema(
                    test_uuid="test2",
                    test_name="Test 2",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    num_test_questions=10,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    test_policy="Don't allow any unsafe answers",
                    test_system_prompt=None,
                    additional_instructions=None,
                ),
            ],
            count=2,
        )
        mock_list_tests.return_value.status_code = 200

        result = await aymara_client.list_tests_async()

        assert isinstance(result, ListTestResponse)
        assert len(result) == 2
        assert all(isinstance(item, BaseTestResponse) for item in result)

        df_result = result.to_df()
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2


def test_validate_test_inputs_valid(aymara_client):
    aymara_client._validate_test_inputs(
        "Valid Test Name",
        "Valid student description",
        "Don't allow any unsafe answers",
        None,
        None,
        "en",
        10,
        models.TestType.SAFETY,
        additional_instructions="Valid additional instructions",
        good_examples=[
            GoodExample(question_text="Question 1", explanation="Explanation 1")
        ],
        bad_examples=[
            BadExample(question_text="Question 2", explanation="Explanation 2")
        ],
    )
    # If no exception is raised, the test passes


def test_validate_test_inputs_invalid_name_length(aymara_client):
    with pytest.raises(ValueError, match="test_name must be between"):
        aymara_client._validate_test_inputs(
            "A" * (DEFAULT_TEST_NAME_LEN_MAX + 1),
            "Valid student description",
            "Don't allow any unsafe answers",
            None,
            None,
            "en",
            10,
            models.TestType.SAFETY,
        )


def test_validate_test_inputs_invalid_question_count(aymara_client):
    with pytest.raises(ValueError, match="num_test_questions must be between"):
        aymara_client._validate_test_inputs(
            "Valid Test Name",
            "Valid student description",
            "Don't allow any unsafe answers",
            None,
            None,
            "en",
            DEFAULT_NUM_QUESTIONS_MAX + 1,
            models.TestType.SAFETY,
        )

    with pytest.raises(ValueError, match="num_test_questions must be between"):
        aymara_client._validate_test_inputs(
            "Valid Test Name",
            "Valid student description",
            "Don't allow any unsafe answers",
            None,
            None,
            "en",
            DEFAULT_NUM_QUESTIONS_MIN - 1,
            models.TestType.SAFETY,
        )


def test_validate_test_inputs_excessive_tokens(aymara_client):
    long_text_length = int(
        DEFAULT_MAX_TOKENS // (2 * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER) + 1
    )
    long_text = "A" * long_text_length

    with pytest.raises(ValueError, match="They are ~"):
        aymara_client._validate_test_inputs(
            "Valid Test Name",
            long_text,
            long_text,
            None,
            None,
            "en",
            10,
            models.TestType.SAFETY,
        )


def test_validate_test_inputs_excessive_examples(aymara_client):
    with pytest.raises(ValueError, match="examples must be less than"):
        aymara_client._validate_test_inputs(
            "Valid Test Name",
            "Valid student description",
            "Don't allow any unsafe answers",
            None,
            None,
            "en",
            10,
            models.TestType.SAFETY,
            good_examples=[
                GoodExample(question_text="Question 1", explanation="Explanation 1")
            ]
            * (MAX_EXAMPLES_LENGTH + 1),
        )


def test_create_and_wait_for_test_impl_sync_success(aymara_client):
    test_data = models.TestInSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Don't allow any unsafe answers",
        test_language="en",
        num_test_questions=10,
    )

    mock_create = MagicMock()
    mock_create.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.RECORD_CREATED,
        test_type=models.TestType.SAFETY,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy="Don't allow any unsafe answers",
        test_system_prompt=None,
        additional_instructions=None,
    )
    mock_create.return_value.status_code = 200

    mock_get = MagicMock()
    mock_get.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.FINISHED,
        test_type=models.TestType.SAFETY,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy="Don't allow any unsafe answers",
        test_system_prompt=None,
        additional_instructions=None,
    )
    mock_get.return_value.status_code = 200

    mock_get_questions = MagicMock()
    mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
        items=[models.QuestionSchema(question_uuid="q1", question_text="Question 1")],
        count=1,
    )
    mock_get_questions.return_value.status_code = 200

    with patch("aymara_ai.core.tests.create_test.sync_detailed", mock_create), patch(
        "aymara_ai.core.tests.get_test.sync_detailed", mock_get
    ), patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed", mock_get_questions
    ):
        result = aymara_client._create_and_wait_for_test_impl_sync(test_data, 60)

        assert isinstance(result, SafetyTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


@pytest.mark.asyncio
async def test_create_and_wait_for_test_impl_async_success(aymara_client):
    test_data = models.TestInSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        test_language="en",
        num_test_questions=10,
    )

    mock_create = AsyncMock()
    mock_create.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.RECORD_CREATED,
        test_type=models.TestType.JAILBREAK,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        additional_instructions=None,
    )
    mock_create.return_value.status_code = 200

    mock_get = AsyncMock()
    mock_get.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.FINISHED,
        test_type=models.TestType.JAILBREAK,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        additional_instructions=None,
    )
    mock_get.return_value.status_code = 200

    mock_get_questions = AsyncMock()
    mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
        items=[models.QuestionSchema(question_uuid="q1", question_text="Question 1")],
        count=1,
    )
    mock_get_questions.return_value.status_code = 200

    with patch("aymara_ai.core.tests.create_test.asyncio_detailed", mock_create), patch(
        "aymara_ai.core.tests.get_test.asyncio_detailed", mock_get
    ), patch(
        "aymara_ai.core.tests.get_test_questions.asyncio_detailed", mock_get_questions
    ):
        result = await aymara_client._create_and_wait_for_test_impl_async(test_data, 60)

        assert isinstance(result, JailbreakTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


def test_create_and_wait_for_test_impl_failure_sync(aymara_client):
    test_data = models.TestInSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Don't allow any unsafe answers",
        test_language="en",
        num_test_questions=10,
    )

    mock_create = MagicMock()
    mock_create.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.RECORD_CREATED,
        test_type=models.TestType.SAFETY,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy="Don't allow any unsafe answers",
        test_system_prompt=None,
        additional_instructions=None,
    )
    mock_create.return_value.status_code = 200

    mock_get = MagicMock()
    mock_get.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.FAILED,
        test_type=models.TestType.SAFETY,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy="Don't allow any unsafe answers",
        test_system_prompt=None,
        additional_instructions=None,
    )
    mock_get.return_value.status_code = 200

    with patch("aymara_ai.core.tests.create_test.sync_detailed", mock_create), patch(
        "aymara_ai.core.tests.get_test.sync_detailed", mock_get
    ):
        result = aymara_client._create_and_wait_for_test_impl_sync(test_data, 60)

        assert isinstance(result, SafetyTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Internal server error, please try again."


@pytest.mark.asyncio
async def test_create_and_wait_for_test_impl_failure_async(aymara_client):
    test_data = models.TestInSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        test_language="en",
        num_test_questions=10,
    )

    mock_create = AsyncMock()
    mock_create.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.RECORD_CREATED,
        test_type=models.TestType.JAILBREAK,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        additional_instructions=None,
    )
    mock_create.return_value.status_code = 200

    mock_get = AsyncMock()
    mock_get.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.FAILED,
        test_type=models.TestType.JAILBREAK,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        additional_instructions=None,
    )
    mock_get.return_value.status_code = 200

    with patch("aymara_ai.core.tests.create_test.asyncio_detailed", mock_create), patch(
        "aymara_ai.core.tests.get_test.asyncio_detailed", mock_get
    ):
        result = await aymara_client._create_and_wait_for_test_impl_async(test_data, 60)

        assert isinstance(result, JailbreakTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Internal server error, please try again."


def test_create_and_wait_for_test_impl_timeout_sync(aymara_client):
    test_data = models.TestInSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy="Don't allow any unsafe answers",
        test_language="en",
        num_test_questions=10,
    )

    mock_create = MagicMock()
    mock_create.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.RECORD_CREATED,
        test_type=models.TestType.SAFETY,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy="Don't allow any unsafe answers",
        test_system_prompt=None,
        additional_instructions=None,
    )
    mock_create.return_value.status_code = 200

    mock_get = MagicMock()
    mock_get.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.GENERATING_QUESTIONS,
        test_type=models.TestType.SAFETY,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy="Don't allow any unsafe answers",
        test_system_prompt=None,
        additional_instructions=None,
    )
    mock_get.return_value.status_code = 200

    mock_get_questions = MagicMock()
    mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
        items=[models.QuestionSchema(question_uuid="q1", question_text="Question 1")],
        count=1,
    )
    mock_get_questions.return_value.status_code = 200

    start_time = 0

    def mock_time():
        nonlocal start_time
        start_time += 61  # More than max_wait_time_secs
        return start_time

    with patch("aymara_ai.core.tests.create_test.sync_detailed", mock_create), patch(
        "aymara_ai.core.tests.get_test.sync_detailed", mock_get
    ), patch("time.time", side_effect=mock_time), patch(
        "time.sleep", return_value=None
    ):
        result = aymara_client._create_and_wait_for_test_impl_sync(test_data, 60)

        assert isinstance(result, SafetyTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Test creation timed out"


@pytest.mark.asyncio
async def test_create_and_wait_for_test_impl_timeout_async(aymara_client):
    test_data = models.TestInSchema(
        test_name="Test 1",
        student_description="Description",
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        test_language="en",
        num_test_questions=10,
    )

    mock_create = AsyncMock()
    mock_create.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.RECORD_CREATED,
        test_type=models.TestType.JAILBREAK,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        additional_instructions=None,
    )
    mock_create.return_value.status_code = 200

    mock_get = AsyncMock()
    mock_get.return_value.parsed = models.TestOutSchema(
        test_uuid="test123",
        test_name="Test 1",
        test_status=models.TestStatus.GENERATING_QUESTIONS,
        test_type=models.TestType.JAILBREAK,
        organization_name="Test Organization",
        num_test_questions=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        test_policy=None,
        test_system_prompt="You are a helpful assistant",
        additional_instructions=None,
    )
    mock_get.return_value.status_code = 200

    mock_get_questions = AsyncMock()
    mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
        items=[models.QuestionSchema(question_uuid="q1", question_text="Question 1")],
        count=1,
    )
    mock_get_questions.return_value.status_code = 200

    start_time = 0

    def mock_time():
        nonlocal start_time
        start_time += 61  # More than max_wait_time_secs
        return start_time

    with patch("aymara_ai.core.tests.create_test.asyncio_detailed", mock_create), patch(
        "aymara_ai.core.tests.get_test.asyncio_detailed", mock_get
    ), patch(
        "aymara_ai.core.tests.get_test_questions.asyncio_detailed", mock_get_questions
    ), patch("time.time", side_effect=mock_time), patch(
        "time.sleep", return_value=None
    ):
        result = await aymara_client._create_and_wait_for_test_impl_async(test_data, 60)

        assert isinstance(result, JailbreakTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Test creation timed out"


def test_get_all_questions_single_page_sync(aymara_client):
    mock_get_questions = MagicMock()
    mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
        items=[models.QuestionSchema(question_uuid="q1", question_text="Question 1")],
        count=1,
    )
    mock_get_questions.return_value.status_code = 200

    with patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed", mock_get_questions
    ):
        result = aymara_client._get_all_questions_sync("test123")

        assert len(result) == 1
        assert result[0].question_uuid == "q1"
        assert result[0].question_text == "Question 1"


@pytest.mark.asyncio
async def test_get_all_questions_single_page_async(aymara_client):
    mock_get_questions = AsyncMock()
    mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
        items=[models.QuestionSchema(question_uuid="q1", question_text="Question 1")],
        count=1,
    )
    mock_get_questions.return_value.status_code = 200

    with patch(
        "aymara_ai.core.tests.get_test_questions.asyncio_detailed", mock_get_questions
    ):
        result = await aymara_client._get_all_questions_async("test123")

        assert len(result) == 1
        assert result[0].question_uuid == "q1"
        assert result[0].question_text == "Question 1"


def test_get_all_questions_multiple_pages_sync(aymara_client):
    mock_get_questions = MagicMock()
    mock_get_questions.side_effect = [
        MagicMock(
            parsed=models.PagedQuestionSchema(
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
            status_code=200,
        ),
        MagicMock(
            parsed=models.PagedQuestionSchema(
                items=[
                    models.QuestionSchema(
                        question_uuid="q3", question_text="Question 3"
                    )
                ],
                count=3,
            ),
            status_code=200,
        ),
    ]

    with patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed", mock_get_questions
    ):
        result = aymara_client._get_all_questions_sync("test123")

        assert len(result) == 3
        assert result[0].question_uuid == "q1"
        assert result[1].question_uuid == "q2"
        assert result[2].question_uuid == "q3"
        assert mock_get_questions.call_count == 2


@pytest.mark.asyncio
async def test_get_all_questions_multiple_pages_async(aymara_client):
    mock_get_questions = AsyncMock()
    mock_get_questions.side_effect = [
        MagicMock(
            parsed=models.PagedQuestionSchema(
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
            status_code=200,
        ),
        MagicMock(
            parsed=models.PagedQuestionSchema(
                items=[
                    models.QuestionSchema(
                        question_uuid="q3", question_text="Question 3"
                    )
                ],
                count=3,
            ),
            status_code=200,
        ),
    ]

    with patch(
        "aymara_ai.core.tests.get_test_questions.asyncio_detailed", mock_get_questions
    ):
        result = await aymara_client._get_all_questions_async("test123")

        assert len(result) == 3
        assert result[0].question_uuid == "q1"
        assert result[1].question_uuid == "q2"
        assert result[2].question_uuid == "q3"
        assert mock_get_questions.call_count == 2


def test_list_tests_pagination(aymara_client):
    with patch("aymara_ai.core.tests.list_tests.sync_detailed") as mock_list_tests:
        mock_list_tests.return_value.parsed = models.PagedTestOutSchema(
            items=[
                models.TestOutSchema(
                    test_uuid="test1",
                    test_name="Test 1",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    num_test_questions=10,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    test_policy="Don't allow any unsafe answers",
                    test_system_prompt=None,
                    additional_instructions=None,
                ),
                models.TestOutSchema(
                    test_uuid="test2",
                    test_name="Test 2",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.JAILBREAK,
                    organization_name="Test Organization",
                    num_test_questions=10,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    test_policy=None,
                    test_system_prompt="You are a helpful assistant",
                    additional_instructions=None,
                ),
            ],
            count=2,
        )
        mock_list_tests.return_value.status_code = 200

        result = aymara_client.list_tests()

        assert isinstance(result, ListTestResponse)
        assert len(result) == 2
        assert all(isinstance(item, BaseTestResponse) for item in result)
        assert result[0].test_uuid == "test1"
        assert result[1].test_uuid == "test2"


def test_logger_progress_bar(aymara_client):
    mock_logger = MagicMock()
    aymara_client.logger = mock_logger

    with patch(
        "aymara_ai.core.tests.create_test.sync_detailed"
    ) as mock_create_test, patch(
        "aymara_ai.core.tests.get_test.sync_detailed"
    ) as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed"
    ) as mock_get_questions:
        mock_create_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
            test_system_prompt=None,
            additional_instructions="Test guidelines",
        )
        mock_create_test.return_value.status_code = 200
        mock_get_test.side_effect = [
            MagicMock(
                parsed=models.TestOutSchema(
                    test_uuid="test123",
                    test_name="Test 1",
                    test_status=models.TestStatus.RECORD_CREATED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    num_test_questions=10,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    test_policy="Don't allow any unsafe answers",
                    test_system_prompt=None,
                    additional_instructions="Test guidelines",
                ),
                status_code=200,
            ),
            MagicMock(
                parsed=models.TestOutSchema(
                    test_uuid="test123",
                    test_name="Test 1",
                    test_status=models.TestStatus.FINISHED,
                    test_type=models.TestType.SAFETY,
                    organization_name="Test Organization",
                    num_test_questions=10,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    test_policy="Don't allow any unsafe answers",
                    test_system_prompt=None,
                    additional_instructions="Test guidelines",
                ),
                status_code=200,
            ),
        ]
        mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
        mock_get_questions.return_value.status_code = 200

        aymara_client.create_safety_test(
            "Test 1",
            "Student description",
            "Test policy",
            max_wait_time_secs=DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
        )

        mock_logger.progress_bar.assert_called_once_with(
            "Test 1", "test123", Status.PENDING
        )
        assert mock_logger.update_progress_bar.call_count == 2
        mock_logger.update_progress_bar.assert_any_call("test123", Status.PENDING)
        mock_logger.update_progress_bar.assert_called_with("test123", Status.COMPLETED)


def test_max_wait_time_secs_exceeded(aymara_client):
    with patch(
        "aymara_ai.core.tests.create_test.sync_detailed"
    ) as mock_create_test, patch(
        "aymara_ai.core.tests.get_test.sync_detailed"
    ) as mock_get_test, patch("time.sleep", return_value=None), patch(
        "time.time", side_effect=[0, 2]
    ):  # Simulate time passing
        mock_create_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
            test_system_prompt=None,
            additional_instructions=None,
        )
        mock_create_test.return_value.status_code = 200
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.SAFETY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
            test_system_prompt=None,
            additional_instructions=None,
        )
        mock_get_test.return_value.status_code = 200

        result = aymara_client.create_safety_test(
            "Test 1",
            "Student description",
            "Test policy",
            max_wait_time_secs=1,  # Set a short timeout for testing
        )

        assert isinstance(result, SafetyTestResponse)
        assert result.test_status == Status.FAILED
        assert result.failure_reason == "Test creation timed out"


@pytest.mark.parametrize(
    "test_status, expected_status, test_type",
    [
        (models.TestStatus.RECORD_CREATED, Status.PENDING, models.TestType.SAFETY),
        (
            models.TestStatus.GENERATING_QUESTIONS,
            Status.PENDING,
            models.TestType.JAILBREAK,
        ),
        (models.TestStatus.FINISHED, Status.COMPLETED, models.TestType.SAFETY),
        (models.TestStatus.FAILED, Status.FAILED, models.TestType.JAILBREAK),
        (
            models.TestStatus.RECORD_CREATED,
            Status.PENDING,
            models.TestType.IMAGE_SAFETY,
        ),
        (models.TestStatus.FINISHED, Status.COMPLETED, models.TestType.IMAGE_SAFETY),
        (models.TestStatus.FAILED, Status.FAILED, models.TestType.IMAGE_SAFETY),
    ],
)
def test_status_handling(aymara_client, test_status, expected_status, test_type):
    with patch("aymara_ai.core.tests.get_test.sync_detailed") as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed"
    ) as mock_get_test_questions:
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=test_status,
            test_type=test_type,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers"
            if test_type == models.TestType.SAFETY
            or test_type == models.TestType.IMAGE_SAFETY
            else None,
            test_system_prompt="You are a helpful assistant"
            if test_type == models.TestType.JAILBREAK
            else None,
            additional_instructions="Test specific guidelines",
        )
        mock_get_test.return_value.status_code = 200

        # Mock the get_test_questions.sync method
        mock_get_test_questions.return_value.parsed = MagicMock(items=[], count=0)
        mock_get_test_questions.return_value.status_code = 200

        result = aymara_client.get_test("test123")

        assert isinstance(
            result,
            SafetyTestResponse
            if test_type == models.TestType.SAFETY
            or test_type == models.TestType.IMAGE_SAFETY
            else JailbreakTestResponse,
        )
        assert result.test_status == expected_status

        # Verify that get_test_questions.sync was called only for FINISHED status
        if test_status == models.TestStatus.FINISHED:
            mock_get_test_questions.assert_called_once_with(
                client=aymara_client.client, test_uuid="test123", offset=0
            )
        else:
            mock_get_test_questions.assert_not_called()


def test_delete_test(aymara_client):
    with patch("aymara_ai.core.tests.delete_test.sync_detailed") as mock_delete_test:
        mock_delete_test.return_value.status_code = 204  # No Content

        aymara_client.delete_test("test123")

        mock_delete_test.assert_called_once_with(
            client=aymara_client.client, test_uuid="test123"
        )


@pytest.mark.asyncio
async def test_delete_test_async(aymara_client):
    with patch(
        "aymara_ai.core.tests.delete_test.asyncio_detailed"
    ) as mock_delete_test_async:
        mock_delete_test_async.return_value.status_code = 204  # No Content

        await aymara_client.delete_test_async("test123")

        mock_delete_test_async.assert_called_once_with(
            client=aymara_client.client, test_uuid="test123"
        )


def test_create_image_safety_test(aymara_client):
    with patch(
        "aymara_ai.core.tests.create_test.sync_detailed"
    ) as mock_create_test, patch(
        "aymara_ai.core.tests.get_test.sync_detailed"
    ) as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed"
    ) as mock_get_questions:
        mock_create_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.IMAGE_SAFETY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe image responses",
            test_system_prompt=None,
            additional_instructions=None,
        )
        mock_create_test.return_value.status_code = 200
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.IMAGE_SAFETY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe image responses",
            test_system_prompt=None,
            additional_instructions=None,
        )
        mock_get_test.return_value.status_code = 200
        mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(question_uuid="q1", question_text="Question 1")
            ],
            count=1,
        )
        mock_get_questions.return_value.status_code = 200

        result = aymara_client.create_image_safety_test(
            "Test 1", "Student description", "Don't allow any unsafe image responses"
        )

        assert isinstance(result, SafetyTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert len(result.questions) == 1


def test_create_accuracy_test(aymara_client):
    with patch(
        "aymara_ai.core.tests.create_test.sync_detailed"
    ) as mock_create_test, patch(
        "aymara_ai.core.tests.get_test.sync_detailed"
    ) as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.sync_detailed"
    ) as mock_get_questions:
        mock_create_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.ACCURACY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy=None,
            test_system_prompt=None,
            knowledge_base="Test knowledge base content",
            additional_instructions=None,
        )
        mock_create_test.return_value.status_code = 200
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.ACCURACY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy=None,
            test_system_prompt=None,
            knowledge_base="Test knowledge base content",
            additional_instructions=None,
        )
        mock_get_test.return_value.status_code = 200
        mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(
                    question_uuid="q1",
                    question_text="Question 1",
                    accuracy_question_type="type_1",
                )
            ],
            count=1,
        )
        mock_get_questions.return_value.status_code = 200

        result = aymara_client.create_accuracy_test(
            "Test 1", "Student description", "Test knowledge base content"
        )

        assert isinstance(result, AccuracyTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert result.knowledge_base == "Test knowledge base content"
        assert len(result.questions) == 1


@pytest.mark.asyncio
async def test_create_accuracy_test_async(aymara_client):
    with patch(
        "aymara_ai.core.tests.create_test.asyncio_detailed"
    ) as mock_create_test, patch(
        "aymara_ai.core.tests.get_test.asyncio_detailed"
    ) as mock_get_test, patch(
        "aymara_ai.core.tests.get_test_questions.asyncio_detailed"
    ) as mock_get_questions:
        mock_create_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.RECORD_CREATED,
            test_type=models.TestType.ACCURACY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy=None,
            test_system_prompt=None,
            knowledge_base="Test knowledge base content",
            additional_instructions=None,
        )
        mock_create_test.return_value.status_code = 200
        mock_get_test.return_value.parsed = models.TestOutSchema(
            test_uuid="test123",
            test_name="Test 1",
            test_status=models.TestStatus.FINISHED,
            test_type=models.TestType.ACCURACY,
            organization_name="Test Organization",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy=None,
            test_system_prompt=None,
            knowledge_base="Test knowledge base content",
            additional_instructions=None,
        )
        mock_get_test.return_value.status_code = 200
        mock_get_questions.return_value.parsed = models.PagedQuestionSchema(
            items=[
                models.QuestionSchema(
                    question_uuid="q1",
                    question_text="Question 1",
                    accuracy_question_type="type_1",
                )
            ],
            count=1,
        )
        mock_get_questions.return_value.status_code = 200

        result = await aymara_client.create_accuracy_test_async(
            "Test 1", "Student description", "Test knowledge base content"
        )

        assert isinstance(result, AccuracyTestResponse)
        assert result.test_uuid == "test123"
        assert result.test_name == "Test 1"
        assert result.test_status == Status.COMPLETED
        assert result.knowledge_base == "Test knowledge base content"
        assert len(result.questions) == 1


def test_create_accuracy_test_validation(aymara_client):
    with pytest.raises(ValueError, match="test_name must be between"):
        aymara_client.create_accuracy_test(
            "A" * 256, "Student description", "Test knowledge base content"
        )

    with pytest.raises(ValueError, match="num_test_questions must be between"):
        aymara_client.create_accuracy_test(
            "Test 1",
            "Student description",
            "Test knowledge base content",
            num_test_questions_per_question_type=0,
        )

    with pytest.raises(ValueError, match="knowledge_base is required"):
        aymara_client.create_accuracy_test("Test 1", "Student description", None)

    long_desc = "A" * int(DEFAULT_MAX_TOKENS / DEFAULT_CHAR_TO_TOKEN_MULTIPLIER / 2)
    long_knowledge_base = "B" * int(
        DEFAULT_MAX_TOKENS / DEFAULT_CHAR_TO_TOKEN_MULTIPLIER / 2
    )
    with pytest.raises(
        ValueError, match="tokens in total but they should be less than"
    ):
        aymara_client.create_accuracy_test(
            "Test 1",
            long_desc,
            long_knowledge_base,
        )

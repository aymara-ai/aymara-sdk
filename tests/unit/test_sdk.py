import pytest
import uuid
import os
from unittest.mock import Mock, AsyncMock
from aymara_ai.sdk import AymaraAI
from aymara_ai._internal_types import APIMakeTestRequest
from aymara_ai.types import CreateTestAsyncResponse, CreateTestResponse, GetTestResponse, ScoreTestResponse, Status, StudentAnswer, TestType


def test_init_with_api_key():
    client = AymaraAI()


def test_init_without_api_key():
    # Clear the environment variable
    os.environ.pop("AYMARA_API_KEY", None)
    with pytest.raises(ValueError, match="API key is required"):
        AymaraAI()


def test_create_test(aymara_client):
    # Setup mock response
    mock_response = Mock()
    mock_response.test_uuid = uuid.uuid4()
    mock_response.test_status = "finished"
    mock_response.test_type = TestType.SAFETY
    mock_questions = [
        Mock(question_uuid=uuid.uuid4(), question_text="Test question")
    ]

    # Configure mock API calls
    aymara_client.tests = Mock()
    aymara_client.tests.create.return_value = mock_response
    aymara_client.tests.get.return_value = mock_response
    aymara_client.tests.get_all_questions.return_value = mock_questions

    # Call the method under test
    response = aymara_client.create_test(
        test_name="Test",
        student_description="Description",
        test_policy="Policy",
        test_type=TestType.SAFETY
    )

    # Assertions
    assert isinstance(response, CreateTestResponse)
    assert response.test_uuid == mock_response.test_uuid
    assert response.test_status == Status.COMPLETED
    assert response.test_type == TestType.SAFETY
    assert len(response.questions) == 1

    # Verify that the mock API methods were called
    aymara_client.tests.create.assert_called_once_with(
        APIMakeTestRequest(
            test_name="Test",
            student_description="Description",
            test_policy="Policy",
            test_type=TestType.SAFETY,
            test_language="en",
            n_test_questions=20,
            test_system_prompt=None,
            writer_model_name="gpt-4o-mini"
        )
    )
    aymara_client.tests.get.assert_called_once_with(mock_response.test_uuid)
    aymara_client.tests.get_all_questions.assert_called_once_with(
        mock_response.test_uuid)


@pytest.mark.asyncio
async def test_create_test_async(aymara_client):
    # Setup mock response
    mock_response = AsyncMock()
    mock_response.test_uuid = uuid.uuid4()

    # Configure mock API calls
    aymara_client.tests = AsyncMock()
    aymara_client.tests.async_create.return_value = mock_response

    # Call the method under test
    response = await aymara_client.create_test_async(
        test_name="Test",
        student_description="Description",
        test_policy="Policy",
        test_type=TestType.SAFETY
    )

    # Assertions
    assert isinstance(response, CreateTestAsyncResponse)
    assert response.test_uuid == mock_response.test_uuid

    # Verify that the mock API method was called
    aymara_client.tests.async_create.assert_called_once_with(
        APIMakeTestRequest(
            test_name="Test",
            student_description="Description",
            test_policy="Policy",
            test_type=TestType.SAFETY,
            test_language="en",
            n_test_questions=20,
            test_system_prompt=None,
            writer_model_name="gpt-4o-mini"
        )
    )


def test_get_test(aymara_client):
    # Setup mock response
    mock_response = Mock()
    mock_response.test_uuid = uuid.uuid4()
    mock_response.test_name = "Test Name"
    mock_response.test_status = "finished"
    mock_response.test_type = TestType.SAFETY
    mock_questions = [
        Mock(question_uuid=uuid.uuid4(), question_text="Test question")
    ]

    # Configure mock API calls
    aymara_client.tests = Mock()
    aymara_client.tests.get.return_value = mock_response
    aymara_client.tests.get_all_questions.return_value = mock_questions

    # Call the method under test
    response = aymara_client.get_test(mock_response.test_uuid)

    # Assertions
    assert isinstance(response, GetTestResponse)
    assert response.test_uuid == mock_response.test_uuid
    assert response.test_name == mock_response.test_name
    assert response.test_status == Status.COMPLETED
    assert response.test_type == TestType.SAFETY
    assert len(response.questions) == 1

    # Verify that the mock API methods were called
    aymara_client.tests.get.assert_called_once_with(mock_response.test_uuid)
    aymara_client.tests.get_all_questions.assert_called_once_with(
        mock_response.test_uuid)


@pytest.mark.asyncio
async def test_get_test_async(aymara_client):
    # Setup mock response
    mock_response = AsyncMock()
    mock_response.test_uuid = uuid.uuid4()
    mock_response.test_name = "Test Name"
    mock_response.test_status = "finished"
    mock_response.test_type = TestType.SAFETY
    mock_questions = [
        AsyncMock(question_uuid=uuid.uuid4(), question_text="Test question")
    ]

    # Configure mock API calls
    aymara_client.tests = AsyncMock()
    aymara_client.tests.async_get.return_value = mock_response
    aymara_client.tests.async_get_all_questions.return_value = mock_questions

    # Call the method under test
    response = await aymara_client.get_test_async(mock_response.test_uuid)

    # Assertions
    assert isinstance(response, GetTestResponse)
    assert response.test_uuid == mock_response.test_uuid
    assert response.test_name == mock_response.test_name
    assert response.test_status == Status.COMPLETED
    assert response.test_type == TestType.SAFETY
    assert len(response.questions) == 1

    # Verify that the mock API methods were called
    aymara_client.tests.async_get.assert_called_once_with(
        mock_response.test_uuid)
    aymara_client.tests.async_get_all_questions.assert_called_once_with(
        mock_response.test_uuid)


@pytest.mark.asyncio
async def test_score_test_async(aymara_client):
    # Setup mock responses
    mock_create_response = AsyncMock()
    mock_create_response.score_run_uuid = uuid.uuid4()

    mock_get_response = AsyncMock()
    mock_get_response.score_run_uuid = mock_create_response.score_run_uuid
    mock_get_response.test_uuid = uuid.uuid4()
    mock_get_response.score_run_status = "finished"
    mock_get_response.test_type = TestType.SAFETY

    mock_scores = [
        AsyncMock(
            question_uuid=uuid.uuid4(),
            question_text="Test question",
            answer_uuid=uuid.uuid4(),
            answer_text="Test answer",
            is_safe=True,
            confidence=0.9,
            explanation="Test explanation"
        )
    ]

    # Configure mock API calls
    aymara_client.scores = AsyncMock()
    aymara_client.scores.async_create.return_value = mock_create_response
    aymara_client.scores.async_get.return_value = mock_get_response
    aymara_client.scores.async_get_all_scores.return_value = mock_scores

    # Call the method under test
    test_uuid = uuid.uuid4()
    student_answers = [StudentAnswer(
        question_uuid=uuid.uuid4(), answer_text="Test answer")]
    response = await aymara_client.score_test_async(test_uuid, student_answers, wait_for_completion=True)

    # Assertions
    assert isinstance(response, ScoreTestResponse)
    assert response.test_uuid == mock_get_response.test_uuid
    assert response.score_run_uuid == mock_create_response.score_run_uuid
    assert response.score_run_status == Status.COMPLETED
    assert len(response.answers) == 1

    # Verify that the mock API methods were called
    aymara_client.scores.async_create.assert_called_once()
    aymara_client.scores.async_get.assert_called()
    aymara_client.scores.async_get_all_scores.assert_called_once_with(
        mock_create_response.score_run_uuid)


def test_get_score_run(aymara_client):
    # Setup mock responses
    mock_get_response = Mock()
    mock_get_response.score_run_uuid = uuid.uuid4()
    mock_get_response.test_uuid = uuid.uuid4()
    mock_get_response.score_run_status = "finished"
    mock_get_response.test_type = TestType.SAFETY

    mock_scores = [
        Mock(
            question_uuid=uuid.uuid4(),
            question_text="Test question",
            answer_uuid=uuid.uuid4(),
            answer_text="Test answer",
            is_safe=True,
            confidence=0.9,
            explanation="Test explanation"
        )
    ]

    # Configure mock API calls
    aymara_client.scores = Mock()
    aymara_client.scores.get.return_value = mock_get_response
    aymara_client.scores.get_all_scores.return_value = mock_scores

    # Call the method under test
    response = aymara_client.get_score_run(mock_get_response.score_run_uuid)

    # Assertions
    assert isinstance(response, ScoreTestResponse)
    assert response.test_uuid == mock_get_response.test_uuid
    assert response.score_run_uuid == mock_get_response.score_run_uuid
    assert response.score_run_status == Status.COMPLETED
    assert len(response.answers) == 1

    # Verify that the mock API methods were called
    aymara_client.scores.get.assert_called_once_with(
        mock_get_response.score_run_uuid)
    aymara_client.scores.get_all_scores.assert_called_once_with(
        mock_get_response.score_run_uuid)


@pytest.mark.asyncio
async def test_get_score_run_async(aymara_client):
    # Setup mock responses
    mock_get_response = AsyncMock()
    mock_get_response.score_run_uuid = uuid.uuid4()
    mock_get_response.test_uuid = uuid.uuid4()
    mock_get_response.test_type = TestType.SAFETY
    mock_get_response.score_run_status = "finished"

    mock_scores = [
        AsyncMock(
            question_uuid=uuid.uuid4(),
            question_text="Test question",
            answer_uuid=uuid.uuid4(),
            answer_text="Test answer",
            is_safe=True,
            confidence=0.9,
            explanation="Test explanation"
        )
    ]

    # Configure mock API calls
    aymara_client.scores = AsyncMock()
    aymara_client.scores.async_get.return_value = mock_get_response
    aymara_client.scores.async_get_all_scores.return_value = mock_scores

    # Call the method under test
    response = await aymara_client.get_score_run_async(mock_get_response.score_run_uuid)

    # Assertions
    assert isinstance(response, ScoreTestResponse)
    assert response.test_uuid == mock_get_response.test_uuid
    assert response.score_run_uuid == mock_get_response.score_run_uuid
    assert response.score_run_status == Status.COMPLETED
    assert len(response.answers) == 1

    # Verify that the mock API methods were called
    aymara_client.scores.async_get.assert_called_once_with(
        mock_get_response.score_run_uuid)
    aymara_client.scores.async_get_all_scores.assert_called_once_with(
        mock_get_response.score_run_uuid)


def test_score_test(aymara_client: AymaraAI):
    # Setup mock responses
    mock_create_response = Mock()
    mock_create_response.score_run_uuid = uuid.uuid4()

    mock_get_response = Mock()
    mock_get_response.score_run_uuid = mock_create_response.score_run_uuid
    mock_get_response.test_uuid = uuid.uuid4()
    mock_get_response.test_type = TestType.SAFETY
    mock_get_response.score_run_status = "finished"

    mock_scores = [
        Mock(
            question_uuid=uuid.uuid4(),
            question_text="Test question",
            answer_uuid=uuid.uuid4(),
            answer_text="Test answer",
            is_safe=True,
            confidence=0.9,
            explanation="Test explanation"
        )
    ]

    # Configure mock API calls
    aymara_client.scores = Mock()
    aymara_client.scores.create.return_value = mock_create_response
    aymara_client.scores.get.return_value = mock_get_response
    aymara_client.scores.get_all_scores.return_value = mock_scores

    # Call the method under test
    test_uuid = uuid.uuid4()
    student_answers = [StudentAnswer(
        question_uuid=uuid.uuid4(), answer_text="Test answer")]
    response = aymara_client.score_test(test_uuid, student_answers)

    # Assertions
    assert isinstance(response, ScoreTestResponse)
    assert response.test_uuid == mock_get_response.test_uuid
    assert response.score_run_uuid == mock_create_response.score_run_uuid
    assert response.score_run_status == Status.COMPLETED
    assert len(response.answers) == 1

    # Verify that the mock API methods were called
    aymara_client.scores.create.assert_called_once()
    aymara_client.scores.get.assert_called()
    aymara_client.scores.get_all_scores.assert_called_once_with(
        mock_create_response.score_run_uuid)

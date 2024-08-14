import uuid
from unittest.mock import Mock, AsyncMock
import pytest
from sdk.api.tests import TestsAPI
from sdk._internal_types import APIGetTestResponse, APIMakeTestRequest, APIMakeTestResponse


@pytest.fixture
def mock_http_client():
    return Mock()


@pytest.fixture
def tests_api(mock_http_client):
    return TestsAPI(mock_http_client)


def test_get(tests_api, mock_http_client):
    test_id = uuid.uuid4()
    mock_response = {
        "test_uuid": str(test_id),
        "test_status": "finished",
        "test_name": "Sample Test",
        "client_name": "Test Client",
        "test_type": "safety",
        "test_language": "en",
        "n_test_questions": 1,
        "writer_model_name": "gpt-4o-mini",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "questions": [
            {
                "question_uuid": str(uuid.uuid4()),
                "question_text": "Test question",
                "test_uuid": str(test_id),
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        ],
        "pagination": {"limit": 20, "has_next": False, "next_cursor": None},
        "message": None
    }
    mock_http_client.get.return_value = mock_response

    response = tests_api.get(test_id)

    assert isinstance(response, APIGetTestResponse)
    assert str(response.test_uuid) == str(test_id)
    assert response.test_status == "finished"
    assert len(response.questions) == 1
    mock_http_client.get.assert_called_once_with(
        f"v1/tests/{test_id}", params={"limit": 20}
    )


@pytest.mark.asyncio
async def test_async_get(tests_api, mock_http_client):
    test_id = uuid.uuid4()
    mock_response = {
        "test_uuid": str(test_id),
        "test_status": "finished",
        "test_name": "Sample Test",
        "client_name": "Test Client",
        "test_type": "safety",
        "test_language": "en",
        "n_test_questions": 1,
        "writer_model_name": "gpt-4o-mini",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "questions": [
            {
                "question_uuid": str(uuid.uuid4()),
                "question_text": "Test question",
                "test_uuid": str(test_id),
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        ],
        "pagination": {"limit": 20, "has_next": False, "next_cursor": None},
        "message": None
    }
    mock_http_client.async_get = AsyncMock(return_value=mock_response)

    response = await tests_api.async_get(test_id)

    assert isinstance(response, APIGetTestResponse)
    assert str(response.test_uuid) == str(test_id)
    assert response.test_status == "finished"
    assert len(response.questions) == 1
    mock_http_client.async_get.assert_called_once_with(
        f"v1/tests/{test_id}", params={"limit": 20}
    )


def test_get_all_questions(tests_api, mock_http_client):
    test_id = uuid.uuid4()
    mock_response = {
        "test_uuid": str(test_id),
        "test_status": "finished",
        "test_name": "Sample Test",
        "client_name": "Test Client",
        "test_type": "safety",
        "test_language": "en",
        "n_test_questions": 1,
        "writer_model_name": "gpt-4o-mini",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "questions": [
            {
                "question_uuid": str(uuid.uuid4()),
                "question_text": "Test question",
                "test_uuid": str(test_id),
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        ],
        "pagination": {"limit": 20, "has_next": False, "next_cursor": None},
        "message": None
    }
    mock_http_client.get.return_value = mock_response

    response = tests_api.get(test_id)

    assert isinstance(response, APIGetTestResponse)
    assert str(response.test_uuid) == str(test_id)
    assert response.test_status == "finished"
    assert len(response.questions) == 1
    mock_http_client.get.assert_called_once_with(
        f"v1/tests/{test_id}", params={"limit": 20}
    )


@pytest.mark.asyncio
async def test_async_get_all_questions(tests_api, mock_http_client):
    test_id = uuid.uuid4()
    mock_response = {
        "test_uuid": str(test_id),
        "test_status": "finished",
        "test_name": "Sample Test",
        "client_name": "Test Client",
        "test_type": "safety",
        "test_language": "en",
        "n_test_questions": 1,
        "writer_model_name": "gpt-4o-mini",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "questions": [
            {
                "question_uuid": str(uuid.uuid4()),
                "question_text": "Test question",
                "test_uuid": str(test_id),
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        ],
        "pagination": {"limit": 20, "has_next": False, "next_cursor": None},
        "message": None
    }
    mock_http_client.async_get = AsyncMock(return_value=mock_response)

    response = await tests_api.async_get(test_id)

    assert isinstance(response, APIGetTestResponse)
    assert str(response.test_uuid) == str(test_id)
    assert response.test_status == "finished"
    assert len(response.questions) == 1
    mock_http_client.async_get.assert_called_once_with(
        f"v1/tests/{test_id}", params={"limit": 20}
    )


def test_list(tests_api, mock_http_client):
    mock_response = [
        {
            "test_uuid": str(uuid.uuid4()),
            "test_status": "finished",
            "test_name": "Sample Test 1",
            "client_name": "Test Client 1",
            "test_type": "safety",
            "test_language": "en",
            "n_test_questions": 1,
            "writer_model_name": "gpt-4o-mini",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "questions": [
                {
                    "question_uuid": str(uuid.uuid4()),
                    "question_text": "Test question 1",
                    "test_uuid": str(uuid.uuid4()),
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:00:00Z"
                }
            ],
            "pagination": {"limit": 20, "has_next": False, "next_cursor": None},
            "message": None
        },
        {
            "test_uuid": str(uuid.uuid4()),
            "test_status": "generating_questions",
            "test_name": "Sample Test 2",
            "client_name": "Test Client 2",
            "test_type": "hallucination",
            "test_language": "es",
            "n_test_questions": 2,
            "writer_model_name": "gpt-4o-mini",
            "created_at": "2023-01-02T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "questions": [
                {
                    "question_uuid": str(uuid.uuid4()),
                    "question_text": "Test question 2",
                    "test_uuid": str(uuid.uuid4()),
                    "created_at": "2023-01-02T00:00:00Z",
                    "updated_at": "2023-01-02T00:00:00Z"
                }
            ],
            "pagination": {"limit": 20, "has_next": False, "next_cursor": None},
            "message": None
        }
    ]
    mock_http_client.get.return_value = mock_response

    response = tests_api.list()

    assert len(response) == 2
    assert all(isinstance(r, APIGetTestResponse) for r in response)
    mock_http_client.get.assert_called_once_with("v1/tests", params={})


@pytest.mark.asyncio
async def test_async_list(tests_api, mock_http_client):
    mock_response = [
        {
            "test_uuid": str(uuid.uuid4()),
            "test_status": "finished",
            "test_name": "Sample Test 1",
            "client_name": "Test Client 1",
            "test_type": "safety",
            "test_language": "en",
            "n_test_questions": 1,
            "writer_model_name": "gpt-4o-mini",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "questions": [
                {
                    "question_uuid": str(uuid.uuid4()),
                    "question_text": "Test question 1",
                    "test_uuid": str(uuid.uuid4()),
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:00:00Z"
                }
            ],
            "pagination": {"limit": 20, "has_next": False, "next_cursor": None},
            "message": None
        },
        {
            "test_uuid": str(uuid.uuid4()),
            "test_status": "generating_questions",
            "test_name": "Sample Test 2",
            "client_name": "Test Client 2",
            "test_type": "hallucination",
            "test_language": "es",
            "n_test_questions": 2,
            "writer_model_name": "gpt-4o-mini",
            "created_at": "2023-01-02T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "questions": [
                {
                    "question_uuid": str(uuid.uuid4()),
                    "question_text": "Test question 2",
                    "test_uuid": str(uuid.uuid4()),
                    "created_at": "2023-01-02T00:00:00Z",
                    "updated_at": "2023-01-02T00:00:00Z"
                }
            ],
            "pagination": {"limit": 20, "has_next": False, "next_cursor": None},
            "message": None
        }
    ]
    mock_http_client.async_get = AsyncMock(return_value=mock_response)

    response = await tests_api.async_list()

    assert len(response) == 2
    assert all(isinstance(r, APIGetTestResponse) for r in response)
    mock_http_client.async_get.assert_called_once_with("v1/tests", params={})


def test_create(tests_api, mock_http_client):
    test_data = APIMakeTestRequest(
        test_name="Test",
        test_type="safety",
        test_language="en",
        n_test_questions=20,
        writer_model_name="gpt-4o-mini",
        student_description="Description",
        test_policy="Policy"
    )
    mock_response = {"test_uuid": str(uuid.uuid4())}
    mock_http_client.post.return_value = mock_response

    response = tests_api.create(test_data)

    assert isinstance(response, APIMakeTestResponse)
    assert response.test_uuid == uuid.UUID(mock_response["test_uuid"])
    mock_http_client.post.assert_called_once_with(
        "v1/tests", json=test_data.model_dump(mode="json")
    )


@pytest.mark.asyncio
async def test_async_create(tests_api, mock_http_client):
    test_data = APIMakeTestRequest(
        test_name="Test",
        test_type="safety",
        test_language="en",
        n_test_questions=20,
        writer_model_name="gpt-4o-mini",
        student_description="Description",
        test_policy="Policy"
    )
    mock_response = {"test_uuid": str(uuid.uuid4())}
    mock_http_client.async_post = AsyncMock(return_value=mock_response)

    response = await tests_api.async_create(test_data)

    assert isinstance(response, APIMakeTestResponse)
    assert response.test_uuid == uuid.UUID(mock_response["test_uuid"])
    mock_http_client.async_post.assert_called_once_with(
        "v1/tests", json=test_data.model_dump(mode="json")
    )

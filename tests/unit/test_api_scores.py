
import uuid
from unittest.mock import Mock, AsyncMock
import pytest
from sdk.api.scores import ScoresAPI
from sdk._internal_types import APIGetScoreResponse, APIMakeScoreRequest, APIMakeScoreResponse, APIScoredAnswerResponse


@pytest.fixture
def mock_http_client():
    return Mock()


@pytest.fixture
def scores_api(mock_http_client):
    return ScoresAPI(mock_http_client)


def test_get(scores_api, mock_http_client):
    score_run_uuid = uuid.uuid4()
    mock_response = {
        "score_run_uuid": str(score_run_uuid),
        "score_run_status": "finished",
        "test_uuid": str(uuid.uuid4()),
        "score_run_model": "gpt-4",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "answers": [
            {
                "answer_uuid": str(uuid.uuid4()),
                "answer_text": "Test answer",
                "question_uuid": str(uuid.uuid4()),
                "question_text": "Test question",
                "test_uuid": str(uuid.uuid4()),
                "score_run_uuid": str(score_run_uuid),
                "is_safe": True,
                "confidence": 0.95,
                "explanation": "Explanation"
            }
        ],
        "pagination": {"limit": 20, "has_next": False, "next_cursor": None}
    }
    mock_http_client.get.return_value = mock_response

    response = scores_api.get(score_run_uuid)

    assert isinstance(response, APIGetScoreResponse)
    assert str(response.score_run_uuid) == str(score_run_uuid)
    assert response.score_run_status == "finished"
    assert len(response.answers) == 1
    mock_http_client.get.assert_called_once_with(
        f"v1/scores/{score_run_uuid}", params={"limit": 20}
    )


@pytest.mark.asyncio
async def test_async_get(scores_api, mock_http_client):
    score_run_uuid = uuid.uuid4()
    mock_response = {
        "score_run_uuid": str(score_run_uuid),
        "score_run_status": "finished",
        "test_uuid": str(uuid.uuid4()),
        "score_run_model": "gpt-4",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "answers": [
            {
                "answer_uuid": str(uuid.uuid4()),
                "answer_text": "Test answer",
                "question_uuid": str(uuid.uuid4()),
                "question_text": "Test question",
                "test_uuid": str(uuid.uuid4()),
                "score_run_uuid": str(score_run_uuid),
                "is_safe": True,
                "confidence": 0.95,
                "explanation": "Explanation"
            }
        ],
        "pagination": {"limit": 20, "has_next": False, "next_cursor": None}
    }
    mock_http_client.async_get = AsyncMock(return_value=mock_response)

    response = await scores_api.async_get(score_run_uuid)

    assert isinstance(response, APIGetScoreResponse)
    assert str(response.score_run_uuid) == str(score_run_uuid)
    assert response.score_run_status == "finished"
    assert len(response.answers) == 1
    mock_http_client.async_get.assert_called_once_with(
        f"v1/scores/{score_run_uuid}", params={"limit": 20}
    )


def test_get_all_scores(scores_api, mock_http_client):
    score_run_uuid = uuid.uuid4()
    mock_response = {
        "score_run_uuid": str(score_run_uuid),
        "score_run_status": "finished",
        "test_uuid": str(uuid.uuid4()),
        "score_run_model": "gpt-4",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "answers": [
            {
                "answer_uuid": str(uuid.uuid4()),
                "answer_text": "Test answer",
                "question_uuid": str(uuid.uuid4()),
                "question_text": "Test question",
                "test_uuid": str(uuid.uuid4()),
                "score_run_uuid": str(score_run_uuid),
                "is_safe": True,
                "confidence": 0.95,
                "explanation": "Explanation"
            }
        ],
        "pagination": {"limit": 20, "has_next": False, "next_cursor": None}
    }
    mock_http_client.get.return_value = mock_response

    response = scores_api.get_all_scores(score_run_uuid)

    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], APIScoredAnswerResponse)
    mock_http_client.get.assert_called_with(
        f"v1/scores/{score_run_uuid}", params={"limit": 20}
    )


@pytest.mark.asyncio
async def test_async_get_all_scores(scores_api, mock_http_client):
    score_run_uuid = uuid.uuid4()
    mock_response = {
        "score_run_uuid": str(score_run_uuid),
        "score_run_status": "finished",
        "test_uuid": str(uuid.uuid4()),
        "score_run_model": "gpt-4",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "answers": [
            {
                "answer_uuid": str(uuid.uuid4()),
                "answer_text": "Test answer",
                "question_uuid": str(uuid.uuid4()),
                "question_text": "Test question",
                "test_uuid": str(uuid.uuid4()),
                "score_run_uuid": str(score_run_uuid),
                "is_safe": True,
                "confidence": 0.95,
                "explanation": "Explanation"
            }
        ],
        "pagination": {"limit": 20, "has_next": False, "next_cursor": None}
    }
    mock_http_client.async_get = AsyncMock(return_value=mock_response)

    response = await scores_api.async_get_all_scores(score_run_uuid)

    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], APIScoredAnswerResponse)
    mock_http_client.async_get.assert_called_with(
        f"v1/scores/{score_run_uuid}", params={"limit": 20}
    )


def test_list(scores_api, mock_http_client):
    mock_response = [
        {
            "score_run_uuid": str(uuid.uuid4()),
            "score_run_status": "finished",
            "test_uuid": str(uuid.uuid4()),
            "score_run_model": "gpt-4",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "answers": [
                {
                    "answer_uuid": str(uuid.uuid4()),
                    "answer_text": "Test answer 1",
                    "question_uuid": str(uuid.uuid4()),
                    "question_text": "Test question 1",
                    "test_uuid": str(uuid.uuid4()),
                    "score_run_uuid": str(uuid.uuid4()),
                    "is_safe": True,
                    "confidence": 0.95,
                    "explanation": "Explanation 1"
                }
            ],
            "pagination": {"limit": 20, "has_next": False, "next_cursor": None}
        },
        {
            "score_run_uuid": str(uuid.uuid4()),
            "score_run_status": "scoring",
            "test_uuid": str(uuid.uuid4()),
            "score_run_model": "gpt-4",
            "created_at": "2023-01-02T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "answers": [
                {
                    "answer_uuid": str(uuid.uuid4()),
                    "answer_text": "Test answer 2",
                    "question_uuid": str(uuid.uuid4()),
                    "question_text": "Test question 2",
                    "test_uuid": str(uuid.uuid4()),
                    "score_run_uuid": str(uuid.uuid4()),
                    "is_safe": None,
                    "confidence": None,
                    "explanation": None
                }
            ],
            "pagination": {"limit": 20, "has_next": False, "next_cursor": None}
        }
    ]
    mock_http_client.get.return_value = mock_response

    response = scores_api.list()

    assert len(response) == 2
    assert all(isinstance(r, APIGetScoreResponse) for r in response)
    mock_http_client.get.assert_called_once_with("v1/scores", params={})


@pytest.mark.asyncio
async def test_async_list(scores_api, mock_http_client):
    mock_response = [
        {
            "score_run_uuid": str(uuid.uuid4()),
            "score_run_status": "finished",
            "test_uuid": str(uuid.uuid4()),
            "score_run_model": "gpt-4",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "answers": [
                {
                    "answer_uuid": str(uuid.uuid4()),
                    "answer_text": "Test answer 1",
                    "question_uuid": str(uuid.uuid4()),
                    "question_text": "Test question 1",
                    "test_uuid": str(uuid.uuid4()),
                    "score_run_uuid": str(uuid.uuid4()),
                    "is_safe": True,
                    "confidence": 0.95,
                    "explanation": "Explanation 1"
                }
            ],
            "pagination": {"limit": 20, "has_next": False, "next_cursor": None}
        },
        {
            "score_run_uuid": str(uuid.uuid4()),
            "score_run_status": "scoring",
            "test_uuid": str(uuid.uuid4()),
            "score_run_model": "gpt-4",
            "created_at": "2023-01-02T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "answers": [
                {
                    "answer_uuid": str(uuid.uuid4()),
                    "answer_text": "Test answer 2",
                    "question_uuid": str(uuid.uuid4()),
                    "question_text": "Test question 2",
                    "test_uuid": str(uuid.uuid4()),
                    "score_run_uuid": str(uuid.uuid4()),
                    "is_safe": None,
                    "confidence": None,
                    "explanation": None
                }
            ],
            "pagination": {"limit": 20, "has_next": False, "next_cursor": None}
        }
    ]
    mock_http_client.async_get = AsyncMock(return_value=mock_response)

    response = await scores_api.async_list()

    assert len(response) == 2
    assert all(isinstance(r, APIGetScoreResponse) for r in response)
    mock_http_client.async_get.assert_called_once_with("v1/scores", params={})


def test_create(scores_api, mock_http_client):
    score_data = APIMakeScoreRequest(
        test_uuid=uuid.uuid4(),
        score_run_model="gpt-4",
        answers=[
            {
                "question_uuid": uuid.uuid4(),
                "answer_text": "Test answer"
            }
        ]
    )
    mock_response = {"score_run_uuid": str(uuid.uuid4())}
    mock_http_client.post.return_value = mock_response

    response = scores_api.create(score_data)

    assert isinstance(response, APIMakeScoreResponse)
    assert response.score_run_uuid == uuid.UUID(
        mock_response["score_run_uuid"])
    mock_http_client.post.assert_called_once_with(
        "v1/scores", json=score_data.model_dump(mode="json")
    )


@pytest.mark.asyncio
async def test_async_create(scores_api, mock_http_client):
    score_data = APIMakeScoreRequest(
        test_uuid=uuid.uuid4(),
        score_run_model="gpt-4",
        answers=[
            {
                "question_uuid": uuid.uuid4(),
                "answer_text": "Test answer"
            }
        ]
    )
    mock_response = {"score_run_uuid": str(uuid.uuid4())}
    mock_http_client.async_post = AsyncMock(return_value=mock_response)

    response = await scores_api.async_create(score_data)

    assert isinstance(response, APIMakeScoreResponse)
    assert response.score_run_uuid == uuid.UUID(
        mock_response["score_run_uuid"])
    mock_http_client.async_post.assert_called_once_with(
        "v1/scores", json=score_data.model_dump(mode="json")
    )

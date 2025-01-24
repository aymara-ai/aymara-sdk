from unittest.mock import mock_open, patch

import pytest

from aymara_ai.generated.aymara_api_client.models import GetImagePresignedUrlsResponse
from aymara_ai.types import ImageStudentAnswerInput


def test_upload_images(aymara_client):
    test_uuid = "test123"
    student_answers = [
        ImageStudentAnswerInput(
            question_uuid="q1", answer_image_path="path/to/image1.jpg"
        ),
        ImageStudentAnswerInput(
            question_uuid="q2", answer_image_path="path/to/image2.jpg"
        ),
    ]

    with patch(
        "aymara_ai.core.uploads.get_image_presigned_urls.sync_detailed"
    ) as mock_get_urls, patch("httpx.put") as mock_put, patch(
        "builtins.open", mock_open(read_data=b"image_data")
    ), patch("os.path.exists", return_value=True):
        # Mock the presigned URL response
        response = GetImagePresignedUrlsResponse()
        response["q1"] = "https://storage.com/q1?token=123"
        response["q2"] = "https://storage.com/q2?token=456"
        mock_get_urls.return_value.parsed = response
        mock_get_urls.return_value.status_code = 200

        # Mock successful upload responses
        mock_put.return_value.status_code = 200

        result = aymara_client.upload_images(
            test_uuid=test_uuid, student_answers=student_answers, batch_size=2
        )

        assert isinstance(result, dict)
        assert len(result) == 2
        assert result["q1"] == "q1"
        assert result["q2"] == "q2"

        # Verify the presigned URL request
        mock_get_urls.assert_called_once()

        # Verify the upload requests
        assert mock_put.call_count == 2


def test_upload_images_validation(aymara_client):
    test_uuid = "test123"
    student_answers = [
        ImageStudentAnswerInput(
            question_uuid="q1", answer_image_path="nonexistent/path.jpg"
        )
    ]

    with patch(
        "aymara_ai.core.uploads.get_image_presigned_urls.sync_detailed"
    ) as mock_get_urls, patch("os.path.exists", return_value=False):
        mock_get_urls.return_value.status_code = (
            200  # Mock the get call before error check
        )
        with pytest.raises(ValueError, match="Image path does not exist"):
            aymara_client.upload_images(
                test_uuid=test_uuid, student_answers=student_answers
            )


@pytest.mark.asyncio
async def test_upload_images_async(aymara_client):
    test_uuid = "test123"
    student_answers = [
        ImageStudentAnswerInput(
            question_uuid="q1", answer_image_path="path/to/image1.jpg"
        ),
        ImageStudentAnswerInput(
            question_uuid="q2", answer_image_path="path/to/image2.jpg"
        ),
    ]

    with patch(
        "aymara_ai.core.uploads.get_image_presigned_urls.asyncio_detailed"
    ) as mock_get_urls, patch("httpx.AsyncClient") as mock_client, patch(
        "builtins.open", mock_open(read_data=b"image_data")
    ), patch("os.path.exists", return_value=True):
        # Mock the presigned URL response
        response = GetImagePresignedUrlsResponse()
        response["q1"] = "https://storage.com/q1?token=123"
        response["q2"] = "https://storage.com/q2?token=456"
        mock_get_urls.return_value.parsed = response
        mock_get_urls.return_value.status_code = 200

        # Mock async client context manager
        mock_client_instance = mock_client.return_value
        mock_client_instance.__aenter__.return_value = mock_client_instance

        # Create a proper async response mock
        class AsyncMock:
            status_code = 200

            async def __call__(self, *args, **kwargs):
                return self

            def __await__(self):
                yield
                return self

        mock_client_instance.put = AsyncMock()

        result = await aymara_client.upload_images_async(
            test_uuid=test_uuid, student_answers=student_answers, batch_size=2
        )

        assert isinstance(result, dict)
        assert len(result) == 2
        assert result["q1"] == "q1"
        assert result["q2"] == "q2"


def test_upload_images_with_progress(aymara_client):
    test_uuid = "test123"
    student_answers = [
        ImageStudentAnswerInput(
            question_uuid="q1", answer_image_path="path/to/image1.jpg"
        ),
        ImageStudentAnswerInput(
            question_uuid="q2", answer_image_path="path/to/image2.jpg"
        ),
    ]
    progress_calls = []

    def progress_callback(count):
        progress_calls.append(count)

    with patch(
        "aymara_ai.core.uploads.get_image_presigned_urls.sync_detailed"
    ) as mock_get_urls, patch("httpx.put") as mock_put, patch(
        "builtins.open", mock_open(read_data=b"image_data")
    ), patch("os.path.exists", return_value=True):
        response = GetImagePresignedUrlsResponse()
        response["q1"] = "https://storage.com/q1?token=123"
        response["q2"] = "https://storage.com/q2?token=456"
        mock_get_urls.return_value.parsed = response
        mock_get_urls.return_value.status_code = 200
        mock_put.return_value.status_code = 200

        result = aymara_client.upload_images(
            test_uuid=test_uuid,
            student_answers=student_answers,
            batch_size=2,
            progress_callback=progress_callback,
        )

        assert progress_calls == [1, 2]
        assert len(result) == 2


def test_upload_images_error_handling(aymara_client):
    test_uuid = "test123"
    student_answers = [
        ImageStudentAnswerInput(
            question_uuid="q1", answer_image_path="path/to/image1.jpg"
        )
    ]

    with patch(
        "aymara_ai.core.uploads.get_image_presigned_urls.sync_detailed"
    ) as mock_get_urls, patch("os.path.exists", return_value=True):
        # Mock validation error response
        mock_get_urls.return_value.status_code = 422
        mock_get_urls.return_value.parsed.detail = "Validation error"

        with pytest.raises(ValueError, match="Validation error"):
            aymara_client.upload_images(
                test_uuid=test_uuid, student_answers=student_answers
            )

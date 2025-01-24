from typing import List

import pytest

from aymara_ai.core.sdk import AymaraAI
from aymara_ai.types import (
    ImageStudentAnswerInput,
    SafetyTestResponse,
)


class TestUploadMixin:
    @pytest.fixture(scope="class")
    def test_image_path(self, tmp_path_factory) -> str:
        # Create a temporary mock image file
        temp_dir = tmp_path_factory.mktemp("test_data")
        mock_image = temp_dir / "mock_image.jpg"

        # Create an empty file with some random bytes to simulate an image
        mock_image.write_bytes(b"mock image content")

        return str(mock_image)

    @pytest.fixture(scope="class")
    async def image_safety_test_data(self, aymara_client: AymaraAI):
        # Create an image safety test and return its UUID and questions
        test_name = "Upload Integration Test"
        student_description = "An AI image generation model"
        test_policy = "No explicit content or violence"
        num_test_questions = 2

        test_response = await aymara_client.create_image_safety_test_async(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            num_test_questions=num_test_questions,
        )
        return test_response

    @pytest.fixture(scope="class")
    def image_student_answers(
        self, image_safety_test_data, test_image_path
    ) -> List[ImageStudentAnswerInput]:
        questions = image_safety_test_data.questions

        answers = [
            ImageStudentAnswerInput(
                question_uuid=question.question_uuid,
                answer_image_path=test_image_path,
            )
            for question in questions
        ]

        return answers

    async def test_upload_images_async(
        self,
        aymara_client: AymaraAI,
        image_safety_test_data: SafetyTestResponse,
        image_student_answers: List[ImageStudentAnswerInput],
    ):
        # Test async upload
        uploaded_keys = await aymara_client.upload_images_async(
            image_safety_test_data.test_uuid,
            [answer.to_answer_in_schema() for answer in image_student_answers],
        )

        assert isinstance(uploaded_keys, dict)
        assert len(uploaded_keys) == len(image_student_answers)
        assert all(isinstance(key, str) for key in uploaded_keys.values())

    def test_upload_images_sync(
        self,
        aymara_client: AymaraAI,
        image_safety_test_data: SafetyTestResponse,
        image_student_answers: List[ImageStudentAnswerInput],
    ):
        # Test sync upload
        uploaded_keys = aymara_client.upload_images(
            image_safety_test_data.test_uuid,
            [answer.to_answer_in_schema() for answer in image_student_answers],
        )

        assert isinstance(uploaded_keys, dict)
        assert len(uploaded_keys) == len(image_student_answers)
        assert all(isinstance(key, str) for key in uploaded_keys.values())

    def test_upload_with_progress_callback(
        self,
        aymara_client: AymaraAI,
        image_safety_test_data: SafetyTestResponse,
        image_student_answers: List[ImageStudentAnswerInput],
    ):
        progress_calls = []

        def progress_callback(count: int):
            progress_calls.append(count)

        aymara_client.upload_images(
            image_safety_test_data.test_uuid,
            [answer.to_answer_in_schema() for answer in image_student_answers],
            progress_callback=progress_callback,
        )

        assert len(progress_calls) == len(image_student_answers)
        assert progress_calls[-1] == len(image_student_answers)

    def test_upload_with_invalid_image_path(
        self,
        aymara_client: AymaraAI,
        image_safety_test_data: SafetyTestResponse,
    ):
        invalid_answers = [
            ImageStudentAnswerInput(
                question_uuid=image_safety_test_data.questions[0].question_uuid,
                answer_image_path="non_existent_file.jpg",
            ),
        ]

        with pytest.raises(ValueError) as exc_info:
            aymara_client.upload_images(
                image_safety_test_data.test_uuid,
                [answer.to_answer_in_schema() for answer in invalid_answers],
            )
        assert "Image path does not exist" in str(exc_info.value)

    def test_upload_with_batch_size(
        self,
        aymara_client: AymaraAI,
        image_safety_test_data: SafetyTestResponse,
        image_student_answers: List[ImageStudentAnswerInput],
    ):
        # Test with different batch sizes
        for batch_size in [1, 2, 5]:
            uploaded_keys = aymara_client.upload_images(
                image_safety_test_data.test_uuid,
                [answer.to_answer_in_schema() for answer in image_student_answers],
                batch_size=batch_size,
            )

            assert isinstance(uploaded_keys, dict)
            assert len(uploaded_keys) == len(image_student_answers)

    def test_upload_with_non_image_file(
        self,
        aymara_client: AymaraAI,
        image_safety_test_data: SafetyTestResponse,
        tmp_path,
    ):
        # Create a text file
        text_file = tmp_path / "test.txt"
        text_file.write_text("This is not an image")

        invalid_answers = [
            ImageStudentAnswerInput(
                question_uuid=image_safety_test_data.questions[0].question_uuid,
                answer_image_path=str(text_file),
            ),
        ]

        with pytest.raises(ValueError):
            aymara_client.upload_images(
                image_safety_test_data.test_uuid,
                [answer.to_answer_in_schema() for answer in invalid_answers],
            )

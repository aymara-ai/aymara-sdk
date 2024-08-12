"""
Tests API
"""
import uuid
import logging
from typing import List


from sdk.http_client import HTTPClient
from sdk._internal_types import ApiTestResponse, ApiTestRequest, ApiCreateTestResponse, ApiTestQuestionResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class TestsAPI:
    """
    Tests API
    """

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_path = "v1/tests"

    def get(self, test_id: uuid.UUID, page: int = 1, page_size: int = 20) -> ApiTestResponse:
        """
        Get a test with pagination support for questions
        """
        params = {"page": page, "page_size": page_size}
        response = self.http_client.get(
            f"{self.base_path}/{test_id}", params=params)
        return ApiTestResponse(**response)

    def get_all_questions(self, test_id: uuid.UUID) -> List[ApiTestQuestionResponse]:
        """
        Get all questions for a test, with optional limit
        """
        all_questions = []
        current_page = 1
        n_test_questions = None
        while n_test_questions is None or len(all_questions) < n_test_questions:
            response = self.get(test_id, page=current_page)
            n_test_questions = response.n_test_questions
            if not response.questions:
                break
            all_questions.extend(response.questions)
            current_page += 1

        if n_test_questions is not None and len(all_questions) != n_test_questions:
            logger.warning(
                "Expected %s questions, but got %s", n_test_questions, len(all_questions))

        return all_questions[:n_test_questions] if n_test_questions else all_questions

    def list(self, **params) -> List[ApiTestResponse]:
        """
        List tests
        """
        response = self.http_client.get(self.base_path, params=params)
        return [ApiTestResponse.model_validate(item) for item in response]

    def create(self, test_data: ApiTestRequest) -> ApiCreateTestResponse:
        """
        Create a test
        """
        test_data = test_data.model_dump()
        response = self.http_client.post(self.base_path, json=test_data)
        return ApiCreateTestResponse(**response)

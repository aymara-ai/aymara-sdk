"""
Tests API
"""
import uuid
import logging
from typing import List, Optional

from sdk.http_client import HTTPClient
from sdk._internal_types import APIGetTestResponse, APIMakeTestRequest, APIMakeTestResponse, APITestQuestionResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_LIMIT = 20


class TestsAPI:
    """
    Tests API
    """

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_path = "v1/tests"

    def get(self, test_id: uuid.UUID, limit: int = DEFAULT_LIMIT, cursor: Optional[str] = None) -> APIGetTestResponse:
        """
        Get a test with pagination support for questions
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        response = self.http_client.get(
            f"{self.base_path}/{test_id}", params=params)
        return APIGetTestResponse(**response)

    def get_all_questions(self, test_id: uuid.UUID) -> List[APITestQuestionResponse]:
        """
        Get all questions for a test
        """
        all_questions = []
        cursor = None
        while True:
            response = self.get(test_id, limit=DEFAULT_LIMIT, cursor=cursor)
            if not response.questions:
                break
            all_questions.extend(response.questions)
            if not response.pagination.has_next:
                break
            cursor = response.pagination.next_cursor

        if response.n_test_questions is not None and len(all_questions) != response.n_test_questions:
            logger.warning(
                "Expected %s questions, but got %s", response.n_test_questions, len(all_questions))

        return all_questions[:response.n_test_questions] if response.n_test_questions else all_questions

    def list(self, **params) -> List[APIGetTestResponse]:
        """
        List tests
        """
        response = self.http_client.get(self.base_path, params=params)
        return [APIGetTestResponse.model_validate(item) for item in response]

    def create(self, test_data: APIMakeTestRequest) -> APIMakeTestResponse:
        """
        Create a test
        """
        test_data = test_data.model_dump()
        response = self.http_client.post(self.base_path, json=test_data)
        return APIMakeTestResponse(**response)
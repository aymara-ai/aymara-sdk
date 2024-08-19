"""
Scores API
"""

import uuid
import logging
from typing import List, Optional

from aymara_ai.http_client import HTTPClient
from aymara_ai._internal_types import APIGetScoreResponse, APIMakeScoreRequest, APIMakeScoreResponse, APIScoredAnswerResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_LIMIT = 20


class ScoresAPI:
    """
    Scores API
    """

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_path = "v1/scores"

    def get(self, score_run_uuid: uuid.UUID, limit: int = DEFAULT_LIMIT, cursor: Optional[str] = None) -> APIGetScoreResponse:
        """
        Get a score with pagination support for answers (synchronous)
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        response = self.http_client.get(
            f"{self.base_path}/{score_run_uuid}", params=params)
        return APIGetScoreResponse(**response)

    async def async_get(self, score_run_uuid: uuid.UUID, limit: int = DEFAULT_LIMIT, cursor: Optional[str] = None) -> APIGetScoreResponse:
        """
        Get a score with pagination support for answers (asynchronous)
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        response = await self.http_client.async_get(
            f"{self.base_path}/{score_run_uuid}", params=params)
        return APIGetScoreResponse(**response)

    def get_all_scores(self, score_run_uuid: uuid.UUID) -> List[APIScoredAnswerResponse]:
        """
        Get all scored answers for a score run (synchronous)
        """
        all_answers = []
        cursor = None
        while True:
            response = self.get(
                score_run_uuid, limit=DEFAULT_LIMIT, cursor=cursor)
            if not response.answers:
                break
            all_answers.extend(response.answers)
            if not response.pagination.has_next:
                break
            cursor = response.pagination.next_cursor

        return all_answers

    async def async_get_all_scores(self, score_run_uuid: uuid.UUID) -> List[APIScoredAnswerResponse]:
        """
        Get all scored answers for a score run (asynchronous)
        """
        all_answers = []
        cursor = None
        while True:
            response = await self.async_get(
                score_run_uuid, limit=DEFAULT_LIMIT, cursor=cursor)
            if not response.answers:
                break
            all_answers.extend(response.answers)
            if not response.pagination.has_next:
                break
            cursor = response.pagination.next_cursor

        return all_answers

    def list(self, **params) -> List[APIGetScoreResponse]:
        """
        List scores (synchronous)
        """
        response = self.http_client.get(self.base_path, params=params)
        return [APIGetScoreResponse.model_validate(item) for item in response]

    async def async_list(self, **params) -> List[APIGetScoreResponse]:
        """
        List scores (asynchronous)
        """
        response = await self.http_client.async_get(self.base_path, params=params)
        return [APIGetScoreResponse.model_validate(item) for item in response]

    def create(self, score_data: APIMakeScoreRequest) -> APIMakeScoreResponse:
        """
        Create a score (synchronous)
        """
        score_data = score_data.model_dump(mode="json")
        response = self.http_client.post(self.base_path, json=score_data)
        return APIMakeScoreResponse(**response)

    async def async_create(self, score_data: APIMakeScoreRequest) -> APIMakeScoreResponse:
        """
        Create a score (asynchronous)
        """
        score_data = score_data.model_dump(mode="json")
        response = await self.http_client.async_post(self.base_path, json=score_data)
        return APIMakeScoreResponse(**response)

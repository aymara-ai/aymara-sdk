"""
Internal types for the SDK
"""
import uuid
from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel

from aymara_ai.types import TestType


class APIPaginationInfo(BaseModel):
    """
    Pagination information
    """
    limit: int
    has_next: bool
    next_cursor: Optional[uuid.UUID] = None


class APIMakeTestRequest(BaseModel):
    """
    Make test request
    """
    test_name: str
    test_type: TestType
    test_language: str
    n_test_questions: int
    writer_model_name: str
    student_description: str
    test_policy: Optional[str] = None
    test_system_prompt: Optional[str] = None


class APIMakeTestResponse(BaseModel):
    """
    Make test response
    """
    test_uuid: uuid.UUID


class APITestQuestionResponse(BaseModel):
    """
    Question response
    """
    question_uuid: uuid.UUID
    question_text: str
    test_uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class APITestStatus(str, Enum):
    RECORD_CREATED = 'record_created'
    GENERATING_QUESTIONS = 'generating_questions'
    FINISHED = 'finished'
    FAILED = 'failed'


class APIGetTestResponse(BaseModel):
    """
    Get test response
    """
    test_uuid: uuid.UUID
    test_status: APITestStatus
    test_name: str
    client_name: str
    test_type: str
    test_language: str
    n_test_questions: int
    writer_model_name: str
    created_at: datetime
    updated_at: datetime
    questions: Optional[List[APITestQuestionResponse]] = None
    pagination: APIPaginationInfo
    message: Optional[str] = None


class APIMakeScoreResponse(BaseModel):
    """
    Make score response
    """
    score_run_uuid: uuid.UUID


class APIAnswerRequest(BaseModel):
    """
    Answer request
    """
    question_uuid: uuid.UUID
    question_text: Optional[str] = None
    answer_text: str


class APIMakeScoreRequest(BaseModel):
    """
    Make score request
    """
    test_uuid: uuid.UUID
    score_run_model: str
    answers: List[APIAnswerRequest]
    overwrite_questions: Optional[bool] = False


class APIScoredAnswerResponse(BaseModel):
    """
    Answer response within the score response
    """
    answer_uuid: uuid.UUID
    answer_text: str
    question_uuid: uuid.UUID
    question_text: str
    test_uuid: uuid.UUID
    score_run_uuid: uuid.UUID
    is_safe: Optional[bool] = None
    confidence: Optional[float] = None
    is_follow: Optional[bool] = None
    instruction_unfollowed: Optional[str] = None
    explanation: Optional[str] = None


class APIScoreRunStatus(str, Enum):
    RECORD_CREATED = 'record_created'
    SCORING = 'scoring'
    FINISHED = 'finished'
    FAILED = 'failed'


class APIGetScoreResponse(BaseModel):
    """
    Get score response
    """
    score_run_uuid: uuid.UUID
    score_run_status: APIScoreRunStatus
    test_uuid: uuid.UUID
    test_type: TestType
    score_run_model: str
    created_at: datetime
    updated_at: datetime
    answers: List[APIScoredAnswerResponse]
    pagination: APIPaginationInfo

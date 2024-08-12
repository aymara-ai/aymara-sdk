import uuid
from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel


class ApiTestQuestionResponse(BaseModel):
    """
    Question response
    """
    question_uuid: uuid.UUID
    question_text: str
    test_uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ApiPaginationInfo(BaseModel):
    """
    Pagination information
    """
    page: int
    page_size: int
    total_questions: int
    total_pages: int


class ApiTestResponse(BaseModel):
    """
    Test response
    """
    test_uuid: uuid.UUID
    test_status: Literal['record_created',
                         'generating_questions', 'finished', 'failed']
    test_name: str
    client_name: str
    test_type: str
    test_language: str
    n_test_questions: int
    writer_model_name: str
    created_at: datetime
    updated_at: datetime
    questions: Optional[List[ApiTestQuestionResponse]] = None
    pagination: Optional[ApiPaginationInfo] = None
    message: Optional[str] = None


class ApiTestRequest(BaseModel):
    """
    Test request
    """
    test_name: str
    test_type: Literal['safety', 'hallucination', 'jailbreak']
    test_language: str
    n_test_questions: int
    writer_model_name: str
    student_description: str
    test_policy: str


class ApiCreateTestResponse(BaseModel):
    """
    Create test response
    """
    test_uuid: uuid.UUID

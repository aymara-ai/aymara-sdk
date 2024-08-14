"""
Types for the SDK
"""
from uuid import UUID
from typing import Annotated, Literal, List, Optional
from pydantic import BaseModel, Field


class MakeTestParams(BaseModel):
    """
    Parameters for making a test
    """
    test_name: Annotated[str, Field(..., description="Name of the test", json_schema_extra={
                                    "example": "Safety Test 1"})]
    test_type: Annotated[Literal['safety', 'hallucination',
                                 'jailbreak'], Field(..., description="Type of the test")]
    test_language: Annotated[str, Field(..., description="Language of the test", json_schema_extra={
                                        "example": "en"})]
    student_description: Annotated[str, Field(..., description="Description of the student", json_schema_extra={
                                              "example": "A high school student"})]
    test_policy: Annotated[str, Field(..., description="Policy for the test", json_schema_extra={
                                      "example": "No explicit content"})]
    n_test_questions: Annotated[int, Field(
        ..., ge=1, description="Number of test questions", json_schema_extra={"example": 10})]


class Question(BaseModel):
    """
    Question in the test
    """
    question_text: Annotated[str,
                             Field(..., description="Question in the test")]
    question_uuid: Annotated[UUID,
                             Field(..., description="UUID of the question")]


class GetTestResponse(BaseModel):
    """
    Response for getting a test
    """
    test_uuid: Annotated[UUID, Field(..., description="UUID of the test")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    test_type: Annotated[Literal['safety', 'hallucination',
                                 'jailbreak'], Field(..., description="Type of the test")]
    test_status: Annotated[Literal['failed', 'pending',
                                   'completed'], Field(..., description="Status of the test")]
    questions: Annotated[List[Question] | None, Field(
        None, description="Questions in the test")]


class CreateTestResponse(BaseModel):
    """
    Create test response
    """
    test_uuid: Annotated[UUID, Field(..., description="UUID of the test")]
    test_status: Annotated[Literal['failed', 'completed'],
                           Field(..., description="Status of the test")]
    test_type: Annotated[Literal['safety', 'hallucination',
                                 'jailbreak'], Field(..., description="Type of the test")]
    questions: Annotated[List[Question],
                         Field(..., description="Questions in the test")]


class CreateTestAsyncResponse(BaseModel):
    """
    Create test async response
    """
    test_uuid: Annotated[UUID, Field(..., description="UUID of the test")]


class StudentAnswer(BaseModel):
    """
    Student answer
    """
    question_uuid: Annotated[UUID,
                             Field(..., description="UUID of the question")]
    answer_text: Annotated[str,
                           Field(..., description="Answer to the question")]


class ScoreTestParams(BaseModel):
    """
    Parameters for scoring a test
    """
    test_uuid: Annotated[UUID, Field(..., description="UUID of the test")]
    student_responses: Annotated[List[StudentAnswer],
                                 Field(..., description="Student responses")]


class ScoredAnswer(BaseModel):
    """
    Response for an individual answer
    """
    answer_uuid: Annotated[UUID, Field(..., description="UUID of the answer")]
    question_uuid: Annotated[UUID,
                             Field(..., description="UUID of the question")]
    answer_text: Annotated[str,
                           Field(..., description="Answer to the question")]
    question_text: Annotated[str,
                             Field(..., description="Question in the test")]
    is_safe: Annotated[Optional[bool], Field(
        None, description="Safety status of the answer")]
    confidence: Annotated[Optional[float], Field(
        None, description="Confidence score of the answer")]
    explanation: Annotated[Optional[str], Field(
        None, description="Explanation for the answer's evaluation")]


class ScoreTestResponse(BaseModel):
    """
    Response for scoring a test
    """
    score_run_uuid: Annotated[UUID,
                              Field(..., description="UUID of the score run")]
    score_run_status: Annotated[Literal['completed', 'failed', 'pending'],
                                Field(..., description="Status of the score run")]
    test_uuid: Annotated[UUID, Field(..., description="UUID of the test")]
    answers: Annotated[List[ScoredAnswer] | None,
                       Field(None, description="List of scored answers")]


class CreateScoreAsyncResponse(BaseModel):
    """
    Create score async response
    """
    score_run_uuid: Annotated[UUID,
                              Field(..., description="UUID of the score run")]

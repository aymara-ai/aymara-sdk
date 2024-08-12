"""
Types for the SDK
"""
from typing import Annotated, Literal, List
from pydantic import BaseModel, Field
from uuid import UUID


class MakeTestParams(BaseModel):
    """
    Parameters for making a test
    """
    test_name: Annotated[str,
                         Field(..., description="Name of the test", example="Safety Test 1")]
    test_type: Annotated[Literal['safety', 'hallucination',
                                 'jailbreak'], Field(..., description="Type of the test")]
    test_language: Annotated[str,
                             Field(..., description="Language of the test", example="en")]
    student_description: Annotated[str, Field(
        ..., description="Description of the student", example="A high school student")]
    test_policy: Annotated[str, Field(
        ..., description="Policy for the test", example="No explicit content")]
    n_test_questions: Annotated[int, Field(..., ge=1,
                                           description="Number of test questions", example=10)]


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

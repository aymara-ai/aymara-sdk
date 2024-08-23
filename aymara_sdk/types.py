"""
Types for the SDK
"""

from typing import Annotated, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

from aymara_sdk.generated.aymara_api_client.models.answer_in_schema import (
    AnswerInSchema as _AnswerInSchema,
)
from aymara_sdk.generated.aymara_api_client.models.question_schema import QuestionSchema
from aymara_sdk.generated.aymara_api_client.models.test_type import TestType


class Status(Enum):
    FAILED = "failed"
    PENDING = "pending"
    COMPLETED = "completed"


class Question(BaseModel):
    """
    Question in the test
    """

    question_text: Annotated[str, Field(..., description="Question in the test")]
    question_uuid: Annotated[str, Field(..., description="UUID of the question")]

    @classmethod
    def from_question_schema(cls, question: QuestionSchema) -> "Question":
        return cls(
            question_uuid=question.question_uuid, question_text=question.question_text
        )

    def to_question_schema(self) -> QuestionSchema:
        return QuestionSchema(
            question_uuid=self.question_uuid, question_text=self.question_text
        )


class GetTestResponse(BaseModel):
    """
    Response for getting a test
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    test_type: Annotated[TestType, Field(..., description="Type of the test")]
    test_status: Annotated[Status, Field(..., description="Status of the test")]
    questions: Annotated[
        List[Question] | None, Field(None, description="Questions in the test")
    ]


class CreateTestResponse(BaseModel):
    """
    Create test response
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    test_status: Annotated[Status, Field(..., description="Status of the test")]
    test_type: Annotated[TestType, Field(..., description="Type of the test")]
    questions: Annotated[
        List[Question], Field(..., description="Questions in the test")
    ]


class CreateTestNoWaitResponse(BaseModel):
    """
    Create test and don't wait for completion response
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]


class StudentAnswer(BaseModel):
    """
    Student answer for a question
    """

    question_uuid: Annotated[str, Field(..., description="UUID of the question")]
    answer_text: Annotated[
        str, Field(..., description="Answer text provided by the student")
    ]

    @classmethod
    def from_answer_in_schema(cls, answer: _AnswerInSchema) -> "StudentAnswer":
        return cls(question_uuid=answer.question_uuid, answer_text=answer.answer_text)

    def to_answer_in_schema(self) -> _AnswerInSchema:
        return _AnswerInSchema(
            question_uuid=self.question_uuid, answer_text=self.answer_text
        )


class ScoreTestParams(BaseModel):
    """
    Parameters for scoring a test
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    student_responses: Annotated[
        List[StudentAnswer], Field(..., description="Student responses")
    ]


class BaseScoredAnswer(BaseModel):
    """
    Base class for scored answers
    """

    __abstract__ = True

    answer_uuid: Annotated[str, Field(..., description="UUID of the answer")]
    question_uuid: Annotated[str, Field(..., description="UUID of the question")]
    answer_text: Annotated[str, Field(..., description="Answer to the question")]
    question_text: Annotated[str, Field(..., description="Question in the test")]


class ScoredSafetyAnswer(BaseScoredAnswer):
    """
    Response for an individual answer in a safety test
    """

    is_safe: Annotated[bool, Field(..., description="Safety status of the answer")]
    confidence: Annotated[
        float, Field(..., description="Confidence score of the answer")
    ]
    explanation: Annotated[
        Optional[str],
        Field(None, description="Explanation for the answer's evaluation"),
    ]


class ScoredJailbreakAnswer(BaseScoredAnswer):
    """
    Response for an individual answer in a jailbreak test
    """

    is_follow: Annotated[
        bool,
        Field(
            ...,
            description="Boolean representing if the answer follows the system prompt",
        ),
    ]
    instruction_unfollowed: Annotated[
        Optional[str], Field(None, description="Instruction that was not followed")
    ]
    explanation: Annotated[
        Optional[str],
        Field(None, description="Explanation for the answer's evaluation"),
    ]


class ScoreTestResponse(BaseModel):
    """
    Response for scoring a test
    """

    score_run_uuid: Annotated[str, Field(..., description="UUID of the score run")]
    score_run_status: Annotated[
        Status, Field(..., description="Status of the score run")
    ]
    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    answers: Annotated[
        List[ScoredSafetyAnswer | ScoredJailbreakAnswer] | None,
        Field(None, description="List of scored answers"),
    ]


class CreateScoreNoWaitResponse(BaseModel):
    """
    Create score and don't wait for completion response
    """

    score_run_uuid: Annotated[str, Field(..., description="UUID of the score run")]

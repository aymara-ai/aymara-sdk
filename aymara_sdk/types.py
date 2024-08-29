"""
Types for the SDK
"""

from typing import Annotated, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
import pandas as pd
from aymara_sdk.generated.aymara_api_client.models.answer_in_schema import (
    AnswerInSchema as _AnswerInSchema,
)
from aymara_sdk.generated.aymara_api_client.models.test_schema import (
    TestSchema as TestParams,
)


from aymara_sdk.generated.aymara_api_client.models.question_schema import QuestionSchema

__all__ = ["TestParams"]


class Status(Enum):
    """Test status"""

    FAILED = "failed"
    PENDING = "pending"
    COMPLETED = "completed"


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


class QuestionResponse(BaseModel):
    """
    Question in the test
    """

    question_text: Annotated[str, Field(..., description="Question in the test")]
    question_uuid: Annotated[str, Field(..., description="UUID of the question")]

    @classmethod
    def from_question_schema(cls, question: QuestionSchema) -> "QuestionResponse":
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
    test_status: Annotated[Status, Field(..., description="Status of the test")]
    questions: Annotated[
        List[QuestionResponse] | None, Field(None, description="Questions in the test")
    ]


class CreateTestResponse(BaseModel):
    """
    Create test response
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    test_status: Annotated[Status, Field(..., description="Status of the test")]
    questions: Annotated[
        List[QuestionResponse], Field(..., description="Questions in the test")
    ]


class ScoredAnswerResponse(BaseModel):
    """
    Scored answer
    """

    answer_uuid: Annotated[str, Field(..., description="UUID of the answer")]
    question_uuid: Annotated[str, Field(..., description="UUID of the question")]
    answer_text: Annotated[str, Field(..., description="Answer to the question")]
    question_text: Annotated[str, Field(..., description="Question in the test")]
    explanation: Annotated[
        Optional[str], Field(None, description="Explanation for the score")
    ]
    confidence: Annotated[float, Field(..., description="Confidence score")]


class ScoreTestResponse(BaseModel):
    """
    Response for scoring a test
    """

    score_run_uuid: Annotated[str, Field(..., description="UUID of the score run")]
    score_run_status: Annotated[
        Status, Field(..., description="Status of the score run")
    ]
    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    num_test_questions: Annotated[
        int, Field(..., description="Number of test questions")
    ]
    answers: Annotated[
        List[ScoredAnswerResponse],
        Field(None, description="List of scored answers"),
    ]

    def pass_rate(self) -> float:
        num_unsafe_answers = len(self.answers)
        return (self.num_test_questions - num_unsafe_answers) / self.num_test_questions

    def to_df(self) -> pd.DataFrame:
        # Create a list to store all rows
        rows = []

        # Create test-level data
        test_data = {
            "score_run_uuid": self.score_run_uuid,
            "score_run_status": self.score_run_status,
            "test_uuid": self.test_uuid,
            "test_name": self.test_name,
            "num_test_questions": self.num_test_questions,
            "pass_rate": self.pass_rate(),
        }

        if self.answers:
            # Create a row for each answer, including test-level data
            for answer in self.answers:
                row = test_data.copy()
                row.update(
                    {
                        "answer_uuid": answer.answer_uuid,
                        "question_uuid": answer.question_uuid,
                        "answer_text": answer.answer_text,
                        "question_text": answer.question_text,
                        "explanation": answer.explanation,
                        "confidence": answer.confidence,
                    }
                )
                rows.append(row)
        else:
            # If there are no answers, just add the test-level data
            rows.append(test_data)

        # Create DataFrame from the list of rows
        return pd.DataFrame(rows)

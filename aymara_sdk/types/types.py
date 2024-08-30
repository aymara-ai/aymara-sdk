"""
Types for the SDK
"""

from typing import Annotated, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
import pandas as pd
from aymara_sdk.generated.aymara_api_client.models.answer_in_schema import (
    AnswerInSchema,
)
from aymara_sdk.generated.aymara_api_client.models.answer_schema import AnswerSchema
from aymara_sdk.generated.aymara_api_client.models.question_schema import QuestionSchema
from aymara_sdk.generated.aymara_api_client.models.score_run_out_schema import (
    ScoreRunOutSchema,
)
from aymara_sdk.generated.aymara_api_client.models.test_out_schema import TestOutSchema
from aymara_sdk.generated.aymara_api_client.models.test_status import TestStatus
from aymara_sdk.generated.aymara_api_client.models.score_run_status import (
    ScoreRunStatus,
)


class Status(Enum):
    """Status for Test or Score Run"""

    FAILED = "failed"
    PENDING = "pending"
    COMPLETED = "completed"

    @classmethod
    def from_api_status(cls, api_status: Union[TestStatus, ScoreRunStatus]) -> "Status":
        """
        Transform an API status to the user-friendly status.

        :param api_status: API status (either TestStatus or ScoreRunStatus).
        :type api_status: Union[TestStatus, ScoreRunStatus]
        :return: Transformed status.
        :rtype: Status
        """
        if isinstance(api_status, TestStatus):
            status_mapping = {
                TestStatus.RECORD_CREATED: Status.PENDING,
                TestStatus.GENERATING_QUESTIONS: Status.PENDING,
                TestStatus.FINISHED: Status.COMPLETED,
                TestStatus.FAILED: Status.FAILED,
            }
        elif isinstance(api_status, ScoreRunStatus):
            status_mapping = {
                ScoreRunStatus.RECORD_CREATED: Status.PENDING,
                ScoreRunStatus.SCORING: Status.PENDING,
                ScoreRunStatus.FINISHED: Status.COMPLETED,
                ScoreRunStatus.FAILED: Status.FAILED,
            }
        else:
            raise ValueError(f"Unexpected status type: {type(api_status)}")

        return status_mapping.get(api_status)


class StudentAnswerInput(BaseModel):
    """
    Student answer for a question
    """

    question_uuid: Annotated[str, Field(..., description="UUID of the question")]
    answer_text: Annotated[
        str, Field(..., description="Answer text provided by the student")
    ]

    @classmethod
    def from_answer_in_schema(cls, answer: AnswerInSchema) -> "StudentAnswerInput":
        return cls(question_uuid=answer.question_uuid, answer_text=answer.answer_text)

    def to_answer_in_schema(self) -> AnswerInSchema:
        return AnswerInSchema(
            question_uuid=self.question_uuid, answer_text=self.answer_text
        )


class CreateScoreRunInput(BaseModel):
    """
    Parameters for scoring a test
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    student_responses: Annotated[
        List[StudentAnswerInput], Field(..., description="Student responses")
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


class BaseTestResponse(BaseModel):
    """
    Base test response
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    test_status: Annotated[Status, Field(..., description="Status of the test")]


class GetTestResponse(BaseTestResponse):
    """
    Response for getting a test. May not have questions if the test is not completed.
    """

    questions: Annotated[
        List[QuestionResponse] | None, Field(None, description="Questions in the test")
    ]

    @classmethod
    def from_test_out_schema_and_questions(
        cls, test: TestOutSchema, questions: List[QuestionSchema]
    ) -> "GetTestResponse":
        return cls(
            test_uuid=test.test_uuid,
            test_name=test.test_name,
            test_status=Status.from_api_status(test.test_status),
            questions=[
                QuestionResponse.from_question_schema(question)
                for question in questions
            ]
            if questions
            else None,
        )


class CreateTestResponse(BaseTestResponse):
    """
    Create test response. Will have test questions as we wait for the test to be completed.
    """

    questions: Annotated[
        List[QuestionResponse], Field(..., description="Questions in the test")
    ]

    @classmethod
    def from_test_out_schema_and_questions(
        cls, test: TestOutSchema, questions: List[QuestionSchema]
    ) -> "CreateTestResponse":
        return cls(
            test_uuid=test.test_uuid,
            test_name=test.test_name,
            test_status=Status.from_api_status(test.test_status),
            questions=[
                QuestionResponse.from_question_schema(question)
                for question in questions
            ],
        )


class ScoredAnswerResponse(BaseModel):
    """
    A single answer to a question in the test that has been scored.
    """

    answer_uuid: Annotated[str, Field(..., description="UUID of the answer")]
    question_uuid: Annotated[str, Field(..., description="UUID of the question")]
    answer_text: Annotated[str, Field(..., description="Answer to the question")]
    question_text: Annotated[str, Field(..., description="Question in the test")]
    explanation: Annotated[
        Optional[str], Field(None, description="Explanation for the score")
    ]
    confidence: Annotated[float, Field(..., description="Confidence score")]

    @classmethod
    def from_answer_out_schema(cls, answer: AnswerSchema) -> "ScoredAnswerResponse":
        return cls(
            answer_uuid=answer.answer_uuid,
            question_uuid=answer.question.question_uuid,
            answer_text=answer.answer_text,
            question_text=answer.question.question_text,
            explanation=answer.explanation,
            confidence=answer.confidence,
        )


class BaseScoreRunResponse(BaseModel):
    """
    Base score run response
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

    def pass_rate(self) -> float:
        if self.answers is None:
            raise ValueError("Answers are not available")
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


class GetScoreRunResponse(BaseScoreRunResponse):
    """
    Response for getting a score run. May not have answers if the score run is not completed.
    """

    answers: Annotated[
        List[ScoredAnswerResponse] | None,
        Field(None, description="List of scored answers"),
    ]

    @classmethod
    def from_score_run_out_schema_and_answers(
        cls, score_run: ScoreRunOutSchema, answers: List[AnswerSchema]
    ) -> "GetScoreRunResponse":
        return cls(
            score_run_uuid=score_run.score_run_uuid,
            score_run_status=Status.from_api_status(score_run.score_run_status),
            test_uuid=score_run.test.test_uuid,
            test_name=score_run.test.test_name,
            num_test_questions=score_run.test.n_test_questions,
            answers=[
                ScoredAnswerResponse.from_answer_out_schema(answer)
                for answer in answers
            ]
            if answers
            else None,
        )


class CreateScoreRunResponse(BaseScoreRunResponse):
    """
    Response for creating a score run. Will have answers as we wait for the score run to be completed.
    """

    answers: Annotated[
        List[ScoredAnswerResponse], Field(..., description="List of scored answers")
    ]

    @classmethod
    def from_score_run_out_schema_and_answers(
        cls, score_run: ScoreRunOutSchema, answers: List[AnswerSchema]
    ) -> "CreateScoreRunResponse":
        return cls(
            score_run_uuid=score_run.score_run_uuid,
            score_run_status=Status.from_api_status(score_run.score_run_status),
            test_uuid=score_run.test.test_uuid,
            test_name=score_run.test.test_name,
            num_test_questions=score_run.test.n_test_questions,
            answers=[
                ScoredAnswerResponse.from_answer_out_schema(answer)
                for answer in answers
            ],
        )

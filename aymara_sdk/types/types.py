"""
Types for the SDK
"""

from enum import Enum
from typing import Annotated, List, Optional, Union

import pandas as pd
from pydantic import BaseModel, Field

from aymara_sdk.generated.aymara_api_client.models.answer_in_schema import (
    AnswerInSchema,
)
from aymara_sdk.generated.aymara_api_client.models.answer_schema import AnswerSchema
from aymara_sdk.generated.aymara_api_client.models.explanation_status import (
    ExplanationStatus,
)
from aymara_sdk.generated.aymara_api_client.models.question_schema import QuestionSchema
from aymara_sdk.generated.aymara_api_client.models.score_run_explanation_out_schema import (
    ScoreRunExplanationOutSchema,
)
from aymara_sdk.generated.aymara_api_client.models.score_run_out_schema import (
    ScoreRunOutSchema,
)
from aymara_sdk.generated.aymara_api_client.models.score_run_status import (
    ScoreRunStatus,
)
from aymara_sdk.generated.aymara_api_client.models.score_runs_explanation_out_schema import (
    ScoreRunsExplanationOutSchema,
)
from aymara_sdk.generated.aymara_api_client.models.test_out_schema import TestOutSchema
from aymara_sdk.generated.aymara_api_client.models.test_status import TestStatus


class Status(Enum):
    """Status for Test or Score Run"""

    FAILED = "failed"
    PENDING = "pending"
    COMPLETED = "completed"

    @classmethod
    def from_api_status(
        cls, api_status: Union[TestStatus, ScoreRunStatus, ExplanationStatus]
    ) -> "Status":
        """
        Transform an API status to the user-friendly status.

        :param api_status: API status (either TestStatus or ScoreRunStatus).
        :type api_status: Union[TestStatus, ScoreRunStatus]
        :return: Transformed status.
        :rtype: Status
        """
        if isinstance(api_status, TestStatus):
            status_mapping = {
                TestStatus.RECORD_CREATED: cls.PENDING,
                TestStatus.GENERATING_QUESTIONS: cls.PENDING,
                TestStatus.FINISHED: cls.COMPLETED,
                TestStatus.FAILED: cls.FAILED,
            }
        elif isinstance(api_status, ScoreRunStatus):
            status_mapping = {
                ScoreRunStatus.RECORD_CREATED: cls.PENDING,
                ScoreRunStatus.SCORING: cls.PENDING,
                ScoreRunStatus.FINISHED: cls.COMPLETED,
                ScoreRunStatus.FAILED: cls.FAILED,
            }
        elif isinstance(api_status, ExplanationStatus):
            status_mapping = {
                ExplanationStatus.RECORD_CREATED: cls.PENDING,
                ExplanationStatus.GENERATING: cls.PENDING,
                ExplanationStatus.FINISHED: cls.COMPLETED,
                ExplanationStatus.FAILED: cls.FAILED,
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


class TestResponse(BaseModel):
    """
    Test response. May or may not have questions, depending on the test status.
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    test_status: Annotated[Status, Field(..., description="Status of the test")]

    questions: Annotated[
        List[QuestionResponse] | None, Field(None, description="Questions in the test")
    ]
    failure_reason: Annotated[
        Optional[str], Field(None, description="Reason for the test failure")
    ]

    def to_questions_df(self) -> pd.DataFrame:
        """Create a questions DataFrame."""

        rows = []
        if self.questions:
            rows = [
                {
                    **{
                        "test_uuid": self.test_uuid,
                        "test_name": self.test_name,
                    },
                    **{
                        "question_uuid": question.question_uuid,
                        "question_text": question.question_text,
                    },
                }
                for question in self.questions
            ]

        return pd.DataFrame(rows)

    @classmethod
    def from_test_out_schema_and_questions(
        cls,
        test: TestOutSchema,
        questions: List[QuestionSchema],
        failure_reason: Optional[str] = None,
    ) -> "TestResponse":
        return cls(
            test_uuid=test.test_uuid,
            test_name=test.test_name,
            test_status=Status.from_api_status(test.test_status),
            questions=[
                QuestionResponse.from_question_schema(question)
                for question in questions
            ]
            if questions is not None
            else None,
            failure_reason=failure_reason,
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


class ScoreRunResponse(BaseModel):
    """
    Score run response. May or may not have answers, depending on the score run status.
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
        List[ScoredAnswerResponse] | None,
        Field(None, description="List of scored answers"),
    ]

    failure_reason: Annotated[
        Optional[str], Field(None, description="Reason for the score run failure")
    ]

    def pass_rate(self) -> float:
        if self.answers is None:
            raise ValueError("Answers are not available")
        num_unsafe_answers = len(self.answers)
        return (self.num_test_questions - num_unsafe_answers) / self.num_test_questions

    def to_scores_df(self) -> pd.DataFrame:
        """Create a scores DataFrame."""

        rows = []
        if self.answers:
            rows = [
                {
                    **{
                        "score_run_uuid": self.score_run_uuid,
                        "test_uuid": self.test_uuid,
                        "test_name": self.test_name,
                    },
                    **{
                        "question_uuid": answer.question_uuid,
                        "answer_uuid": answer.answer_uuid,
                        "question_text": answer.question_text,
                        "answer_text": answer.answer_text,
                        "explanation": answer.explanation,
                        "confidence": answer.confidence,
                    },
                }
                for answer in self.answers
            ]

        return pd.DataFrame(rows)

    @classmethod
    def from_score_run_out_schema_and_answers(
        cls,
        score_run: ScoreRunOutSchema,
        answers: List[AnswerSchema] | None = None,
        failure_reason: Optional[str] = None,
    ) -> "ScoreRunResponse":
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
            if answers is not None
            else None,
            failure_reason=failure_reason,
        )


class ScoreRunExplanationResponse(BaseModel):
    """
    Score run explanation item response.
    """

    score_run_explanation_uuid: Annotated[
        str, Field(..., description="UUID of the score run explanation")
    ]
    explanation_summary: Annotated[
        str, Field(..., description="Summary of the explanation")
    ]
    improvement_advice: Annotated[str, Field(..., description="Advice for improvement")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    score_run_uuid: Annotated[str, Field(..., description="UUID of the score run")]

    @classmethod
    def from_score_run_explanation_out_schema(
        cls, explanation: ScoreRunExplanationOutSchema
    ) -> "ScoreRunExplanationResponse":
        return cls(
            score_run_explanation_uuid=explanation.score_run_explanation_uuid,
            explanation_summary=explanation.explanation_summary,
            improvement_advice=explanation.improvement_advice,
            test_name=explanation.score_run.test.test_name,
            score_run_uuid=explanation.score_run.score_run_uuid,
        )


class ScoreRunsExplanationResponse(BaseModel):
    """
    Score run explanation response.
    """

    score_runs_explanation_uuid: Annotated[
        str, Field(..., description="UUID of the score run explanation")
    ]
    overall_explanation_summary: Annotated[
        str, Field(..., description="Summary of the overall explanation")
    ]
    overall_improvement_advice: Annotated[
        str, Field(..., description="Advice for improvement")
    ]

    score_run_explanations: Annotated[
        List[ScoreRunExplanationResponse],
        Field(..., description="List of score run explanations"),
    ]

    failure_reason: Annotated[
        Optional[str], Field(None, description="Reason for the score run failure")
    ]

    @classmethod
    def from_explanation_out_schema_and_failure_reason(
        cls,
        explanation: ScoreRunsExplanationOutSchema,
        failure_reason: Optional[str] = None,
    ) -> "ScoreRunsExplanationResponse":
        return cls(
            score_runs_explanation_uuid=explanation.score_runs_explanation_uuid,
            overall_explanation_summary=explanation.overall_explanation_summary,
            overall_improvement_advice=explanation.overall_improvement_advice,
            score_run_explanations=[
                ScoreRunExplanationResponse.from_score_run_explanation_out_schema(
                    explanation
                )
                for explanation in explanation.score_run_explanations
            ],
            failure_reason=failure_reason,
        )

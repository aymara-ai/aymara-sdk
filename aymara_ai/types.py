"""
Types for the SDK
"""

from datetime import datetime
from enum import Enum
from typing import Annotated, Iterator, List, Optional, Union

import pandas as pd
from pydantic import BaseModel, Field, RootModel

from aymara_ai.generated.aymara_api_client.models import ScoreRunSuiteSummaryOutSchema
from aymara_ai.generated.aymara_api_client.models.answer_in_schema import (
    AnswerInSchema,
)
from aymara_ai.generated.aymara_api_client.models.answer_out_schema import (
    AnswerOutSchema,
)
from aymara_ai.generated.aymara_api_client.models.question_schema import QuestionSchema
from aymara_ai.generated.aymara_api_client.models.score_run_out_schema import (
    ScoreRunOutSchema,
)
from aymara_ai.generated.aymara_api_client.models.score_run_status import (
    ScoreRunStatus,
)
from aymara_ai.generated.aymara_api_client.models.score_run_suite_summary_status import (
    ScoreRunSuiteSummaryStatus,
)
from aymara_ai.generated.aymara_api_client.models.score_run_summary_out_schema import (
    ScoreRunSummaryOutSchema,
)
from aymara_ai.generated.aymara_api_client.models.test_out_schema import TestOutSchema
from aymara_ai.generated.aymara_api_client.models.test_status import TestStatus
from aymara_ai.generated.aymara_api_client.models.test_type import TestType


class Status(Enum):
    """Status for Test or Score Run"""

    FAILED = "failed"
    PENDING = "pending"
    COMPLETED = "completed"

    @classmethod
    def from_api_status(
        cls, api_status: Union[TestStatus, ScoreRunStatus, ScoreRunSuiteSummaryStatus]
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
        elif isinstance(api_status, ScoreRunSuiteSummaryStatus):
            status_mapping = {
                ScoreRunSuiteSummaryStatus.RECORD_CREATED: cls.PENDING,
                ScoreRunSuiteSummaryStatus.GENERATING: cls.PENDING,
                ScoreRunSuiteSummaryStatus.FINISHED: cls.COMPLETED,
                ScoreRunSuiteSummaryStatus.FAILED: cls.FAILED,
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
        Optional[str], Field(None, description="Answer text provided by the student")
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
    Test response. May or may not have questions, depending on the test status.
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    test_status: Annotated[Status, Field(..., description="Status of the test")]
    created_at: Annotated[
        datetime, Field(..., description="Timestamp of the test creation")
    ]

    num_test_questions: Annotated[
        Optional[int], Field(None, description="Number of test questions")
    ]

    questions: Annotated[
        Optional[List[QuestionResponse]],
        Field(None, description="Questions in the test"),
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
        questions: Optional[List[QuestionSchema]] = None,
        failure_reason: Optional[str] = None,
    ) -> "BaseTestResponse":
        base_attributes = {
            "test_uuid": test.test_uuid,
            "test_name": test.test_name,
            "test_status": Status.from_api_status(test.test_status),
            "created_at": test.created_at,
            "num_test_questions": test.num_test_questions,
            "questions": [QuestionResponse.from_question_schema(q) for q in questions]
            if questions
            else None,
            "failure_reason": failure_reason,
        }

        if test.test_type == TestType.SAFETY:
            return SafetyTestResponse(**base_attributes, test_policy=test.test_policy)
        elif test.test_type == TestType.JAILBREAK:
            return JailbreakTestResponse(
                **base_attributes, test_system_prompt=test.test_system_prompt
            )
        else:
            raise ValueError(f"Unsupported test type: {test.test_type}")


class SafetyTestResponse(BaseTestResponse):
    """
    Safety test response.
    """

    test_policy: Annotated[str, Field(..., description="Safety Policy to test against")]


class JailbreakTestResponse(BaseTestResponse):
    """
    Jailbreak test response.
    """

    test_system_prompt: Annotated[
        str, Field(..., description="System prompt to jailbreak")
    ]


class ListTestResponse(RootModel):
    """
    List of tests.
    """

    root: List[BaseTestResponse]

    def __iter__(self) -> Iterator[BaseTestResponse]:
        return iter(self.root)

    def __getitem__(self, index) -> BaseTestResponse:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

    def to_df(self) -> pd.DataFrame:
        """Create a DataFrame from the list of TestResponses."""
        rows = []
        for test in self.root:
            row = {
                "test_uuid": test.test_uuid,
                "test_name": test.test_name,
                "test_status": test.test_status.value,
                "created_at": test.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "failure_reason": test.failure_reason,
                "num_test_questions": test.num_test_questions,
            }

            if isinstance(test, SafetyTestResponse):
                row["test_policy"] = test.test_policy
            elif isinstance(test, JailbreakTestResponse):
                row["test_system_prompt"] = test.test_system_prompt

            rows.append(row)
        return pd.DataFrame(rows)


class ScoredAnswerResponse(BaseModel):
    """
    A single answer to a question in the test that has been scored.
    """

    answer_uuid: Annotated[str, Field(..., description="UUID of the answer")]
    question_uuid: Annotated[str, Field(..., description="UUID of the question")]
    answer_text: Annotated[
        Optional[str], Field(None, description="Answer to the question")
    ]
    question_text: Annotated[str, Field(..., description="Question in the test")]
    explanation: Annotated[
        Optional[str], Field(None, description="Explanation for the score")
    ]
    confidence: Annotated[Optional[float], Field(None, description="Confidence score")]
    is_passed: Annotated[
        Optional[bool], Field(None, description="Whether the answer is passed")
    ]

    @classmethod
    def from_answer_out_schema(cls, answer: AnswerOutSchema) -> "ScoredAnswerResponse":
        return cls(
            answer_uuid=answer.answer_uuid,
            question_uuid=answer.question.question_uuid,
            answer_text=answer.answer_text,
            question_text=answer.question.question_text,
            explanation=answer.explanation,
            confidence=answer.confidence,
            is_passed=answer.is_passed,
        )


class ScoreRunResponse(BaseModel):
    """
    Score run response. May or may not have answers, depending on the score run status.
    """

    score_run_uuid: Annotated[str, Field(..., description="UUID of the score run")]
    score_run_status: Annotated[
        Status, Field(..., description="Status of the score run")
    ]

    test: Annotated[BaseTestResponse, Field(..., description="Test response")]
    answers: Annotated[
        Optional[List[ScoredAnswerResponse]],
        Field(None, description="List of scored answers"),
    ]

    created_at: Annotated[
        datetime, Field(..., description="Timestamp of the score run creation")
    ]

    failure_reason: Annotated[
        Optional[str], Field(None, description="Reason for the score run failure")
    ]

    def pass_rate(self) -> float:
        if self.answers is None:
            raise ValueError("Answers are not available")
        failed_answers = len(
            [answer for answer in self.answers if answer.is_passed is False]
        )

        answered_questions = len(
            [answer for answer in self.answers if answer.is_passed is not None]
        )
        return (answered_questions - failed_answers) / answered_questions

    def to_scores_df(self) -> pd.DataFrame:
        """Create a scores DataFrame."""
        rows = (
            [
                {
                    "score_run_uuid": self.score_run_uuid,
                    "test_uuid": self.test.test_uuid,
                    "test_name": self.test.test_name,
                    "question_uuid": answer.question_uuid,
                    "answer_uuid": answer.answer_uuid,
                    "is_passed": answer.is_passed,
                    "question_text": answer.question_text,
                    "answer_text": answer.answer_text,
                    "explanation": answer.explanation,
                    "confidence": answer.confidence,
                }
                for answer in self.answers
            ]
            if self.answers
            else []
        )

        return pd.DataFrame(rows)

    @classmethod
    def from_score_run_out_schema_and_answers(
        cls,
        score_run: ScoreRunOutSchema,
        answers: Optional[List[AnswerOutSchema]] = None,
        failure_reason: Optional[str] = None,
    ) -> "ScoreRunResponse":
        return cls(
            score_run_uuid=score_run.score_run_uuid,
            score_run_status=Status.from_api_status(score_run.score_run_status),
            test=BaseTestResponse.from_test_out_schema_and_questions(
                score_run.test,
                questions=[answer.question for answer in answers]
                if answers is not None
                else None,
            ),
            answers=[
                ScoredAnswerResponse.from_answer_out_schema(answer)
                for answer in answers
            ]
            if answers is not None
            else None,
            created_at=score_run.created_at,
            failure_reason=failure_reason,
        )


class ListScoreRunResponse(RootModel):
    """
    List of score runs.
    """

    root: List["ScoreRunResponse"]

    def __iter__(self) -> Iterator[ScoreRunResponse]:
        return iter(self.root)

    def __getitem__(self, index) -> ScoreRunResponse:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

    def to_df(self) -> pd.DataFrame:
        """Create a DataFrame from the list of ScoreRunResponses."""
        rows = []
        for score_run in self.root:
            row = {
                "score_run_uuid": score_run.score_run_uuid,
                "test_uuid": score_run.test.test_uuid,
                "test_name": score_run.test.test_name,
                "score_run_status": score_run.score_run_status.value,
                "created_at": score_run.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "failure_reason": score_run.failure_reason,
                "num_test_questions": score_run.test.num_test_questions,
                "pass_rate": score_run.pass_rate() if score_run.answers else None,
            }
            rows.append(row)
        return pd.DataFrame(rows)


class ScoreRunSummaryResponse(BaseModel):
    """
    Score run summary response.
    """

    score_run_summary_uuid: Annotated[
        str, Field(..., description="UUID of the score run summary")
    ]
    explanation_summary: Annotated[
        str, Field(..., description="Summary of the explanations")
    ]
    improvement_advice: Annotated[str, Field(..., description="Advice for improvement")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    score_run_uuid: Annotated[str, Field(..., description="UUID of the score run")]

    @classmethod
    def from_score_run_summary_out_schema(
        cls, summary: ScoreRunSummaryOutSchema
    ) -> "ScoreRunSummaryResponse":
        return cls(
            score_run_summary_uuid=summary.score_run_summary_uuid,
            explanation_summary=summary.explanation_summary,
            improvement_advice=summary.improvement_advice,
            test_name=summary.score_run.test.test_name,
            score_run_uuid=summary.score_run.score_run_uuid,
        )


class ScoreRunSuiteSummaryResponse(BaseModel):
    """
    Score run suite summary response.
    """

    score_run_suite_summary_uuid: Annotated[
        str, Field(..., description="UUID of the score run suite summary")
    ]

    score_run_suite_summary_status: Annotated[
        Status, Field(..., description="Status of the score run suite summary")
    ]

    overall_summary: Annotated[
        Optional[str], Field(None, description="Summary of the overall explanation")
    ]
    overall_improvement_advice: Annotated[
        Optional[str], Field(None, description="Advice for improvement")
    ]

    score_run_summaries: Annotated[
        List[ScoreRunSummaryResponse],
        Field(..., description="List of score run summaries"),
    ]

    created_at: Annotated[
        datetime,
        Field(..., description="Timestamp of the score run suite summary creation"),
    ]

    failure_reason: Annotated[
        Optional[str], Field(None, description="Reason for the score run failure")
    ]

    def to_df(self) -> pd.DataFrame:
        """Create a scores DataFrame."""
        rows = [
            {
                "score_run_suite_summary_uuid": self.score_run_suite_summary_uuid,
                "test_name": "Overall",
                "explanation_summary": self.overall_summary,
                "improvement_advice": self.overall_improvement_advice,
            }
        ] + [
            {
                "score_run_suite_summary_uuid": self.score_run_suite_summary_uuid,
                "score_run_summary_uuid": summary.score_run_summary_uuid,
                "test_name": summary.test_name,
                "explanation_summary": summary.explanation_summary,
                "improvement_advice": summary.improvement_advice,
            }
            for summary in self.score_run_summaries
        ]

        return pd.DataFrame(rows)

    @classmethod
    def from_summary_out_schema_and_failure_reason(
        cls,
        summary: ScoreRunSuiteSummaryOutSchema,
        failure_reason: Optional[str] = None,
    ) -> "ScoreRunSuiteSummaryResponse":
        return cls(
            score_run_suite_summary_uuid=summary.score_run_suite_summary_uuid,
            score_run_suite_summary_status=Status.from_api_status(summary.status),
            overall_summary=summary.overall_summary,
            overall_improvement_advice=summary.overall_improvement_advice,
            score_run_summaries=[
                ScoreRunSummaryResponse.from_score_run_summary_out_schema(summary)
                for summary in summary.score_run_summaries
            ],
            created_at=summary.created_at,
            failure_reason=failure_reason,
        )


class ListScoreRunSuiteSummaryResponse(RootModel):
    """
    List of score run suite summaries.
    """

    root: List["ScoreRunSuiteSummaryResponse"]

    def __iter__(self) -> Iterator[ScoreRunSuiteSummaryResponse]:
        return iter(self.root)

    def __getitem__(self, index) -> ScoreRunSuiteSummaryResponse:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

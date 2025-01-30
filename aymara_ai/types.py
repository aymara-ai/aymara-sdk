"""
Types for the SDK
"""

import re
from datetime import datetime
from enum import Enum
from typing import Annotated, Iterator, List, Optional, Union

import pandas as pd
from pydantic import BaseModel, Field, RootModel, model_validator

from aymara_ai.generated.aymara_api_client.models import ScoreRunSuiteSummaryOutSchema
from aymara_ai.generated.aymara_api_client.models.answer_in_schema import (
    AnswerInSchema,
)
from aymara_ai.generated.aymara_api_client.models.answer_out_schema import (
    AnswerOutSchema,
)
from aymara_ai.generated.aymara_api_client.models.example_in_schema import (
    ExampleInSchema,
)
from aymara_ai.generated.aymara_api_client.models.example_type import ExampleType
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
from aymara_ai.generated.aymara_api_client.models.scoring_example_in_schema import (
    ScoringExampleInSchema,
)
from aymara_ai.generated.aymara_api_client.models.scoring_example_in_schema_example_type import (
    ScoringExampleInSchemaExampleType,
)
from aymara_ai.generated.aymara_api_client.models.test_out_schema import TestOutSchema
from aymara_ai.generated.aymara_api_client.models.test_status import TestStatus
from aymara_ai.generated.aymara_api_client.models.test_type import TestType


class Status(str, Enum):
    """Status for Test or Score Run"""

    UPLOADING = "UPLOADING"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

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
                ScoreRunStatus.IMAGE_UPLOADING: cls.UPLOADING,
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


class BaseStudentAnswerInput(BaseModel):
    """
    Base class for student answers
    """

    question_uuid: Annotated[str, Field(..., description="UUID of the question")]
    is_refusal: Annotated[
        bool, Field(default=False, description="Whether the student refused to answer")
    ]
    exclude_from_scoring: Annotated[
        bool,
        Field(
            default=False,
            description="Whether the answer should be excluded from scoring",
        ),
    ]

    def to_answer_in_schema(self) -> AnswerInSchema:
        return AnswerInSchema(
            question_uuid=self.question_uuid,
            answer_text=getattr(self, "answer_text", None),
            answer_image_path=getattr(self, "answer_image_path", None),
            student_refused=self.is_refusal,
            exclude_from_scoring=self.exclude_from_scoring,
        )

    @model_validator(mode="after")
    def validate_answer_provided(self) -> "BaseStudentAnswerInput":
        """Validate that an answer is provided unless exclude_from_scoring is True."""
        if not self.exclude_from_scoring:
            answer_text = getattr(self, "answer_text", None)
            answer_image_path = getattr(self, "answer_image_path", None)
            if (
                answer_text is None
                and answer_image_path is None
                and not self.is_refusal
            ):
                raise ValueError(
                    "Either answer_text or answer_image_path must be provided "
                    "unless exclude_from_scoring or is_refusal is True"
                )
        return self


class TextStudentAnswerInput(BaseStudentAnswerInput):
    """
    Student text answer for a question
    """

    answer_text: Annotated[
        Optional[str], Field(..., description="Answer text provided by the student")
    ]

    @classmethod
    def from_answer_in_schema(cls, answer: AnswerInSchema) -> "TextStudentAnswerInput":
        if answer.answer_text is None:
            raise ValueError(
                "Cannot create TextStudentAnswerInput from answer without text"
            )
        return cls(
            question_uuid=answer.question_uuid,
            answer_text=answer.answer_text,
            is_refusal=answer.student_refused,
            exclude_from_scoring=answer.exclude_from_scoring,
        )


class ImageStudentAnswerInput(BaseStudentAnswerInput):
    """
    Student image answer for a question
    """

    answer_image_path: Annotated[
        Optional[str], Field(default=None, description="Path to the image")
    ]

    @classmethod
    def from_answer_in_schema(cls, answer: AnswerInSchema) -> "ImageStudentAnswerInput":
        if answer.answer_image_path is None:
            raise ValueError(
                "Cannot create ImageStudentAnswerInput from answer without image path"
            )
        return cls(
            question_uuid=answer.question_uuid,
            answer_image_path=answer.answer_image_path,
            is_refusal=answer.student_refused,
            exclude_from_scoring=answer.exclude_from_scoring,
        )


class ScoringExample(BaseModel):
    """
    An example answer to guide the scoring process
    """

    question_text: Annotated[str, Field(..., description="Example question text")]
    answer_text: Annotated[str, Field(..., description="Example answer text")]
    explanation: Annotated[
        Optional[str],
        Field(None, description="Explanation of why this answer should pass/fail"),
    ]
    is_passing: Annotated[
        bool, Field(..., description="Whether this is a passing example")
    ]

    def to_scoring_example_in_schema(self) -> ScoringExampleInSchema:
        return ScoringExampleInSchema(
            question_text=self.question_text,
            answer_text=self.answer_text,
            explanation=self.explanation,
            example_type=ScoringExampleInSchemaExampleType.PASS
            if self.is_passing
            else ScoringExampleInSchemaExampleType.FAIL,
        )


class ImageScoringExample(BaseModel):
    """
    An example answer to guide the scoring process
    """

    question_text: Annotated[str, Field(..., description="Example question text")]
    image_description: Annotated[
        str, Field(..., description="Description of the image")
    ]
    explanation: Annotated[
        Optional[str],
        Field(None, description="Explanation of why this answer should pass/fail"),
    ]
    is_passing: Annotated[
        bool, Field(..., description="Whether this is a passing example")
    ]

    def to_scoring_example_in_schema(self) -> ScoringExampleInSchema:
        return ScoringExampleInSchema(
            question_text=self.question_text,
            answer_text=self.image_description,
            explanation=self.explanation,
            example_type=ScoringExampleInSchemaExampleType.PASS
            if self.is_passing
            else ScoringExampleInSchemaExampleType.FAIL,
        )


class CreateScoreRunInput(BaseModel):
    """
    Parameters for scoring a test
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    student_responses: Annotated[
        List[TextStudentAnswerInput], Field(..., description="Student responses")
    ]
    scoring_examples: Annotated[
        Optional[List[ScoringExample]],
        Field(None, description="Examples to guide scoring"),
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
            question_uuid=question.question_uuid,
            question_text=question.question_text,
        )

    def to_question_schema(self) -> QuestionSchema:
        return QuestionSchema(
            question_uuid=self.question_uuid,
            question_text=self.question_text,
        )


class AccuracyQuestionResponse(QuestionResponse):
    """
    Question in the test
    """

    accuracy_question_type: Annotated[
        Optional[str],
        Field(None, description="Type of the question for accuracy tests"),
    ]

    @classmethod
    def from_question_schema(
        cls, question: QuestionSchema
    ) -> "AccuracyQuestionResponse":
        return cls(
            question_uuid=question.question_uuid,
            question_text=question.question_text,
            accuracy_question_type=question.accuracy_question_type,
        )

    def to_question_schema(self) -> QuestionSchema:
        return QuestionSchema(
            question_uuid=self.question_uuid,
            question_text=self.question_text,
            accuracy_question_type=self.accuracy_question_type,
        )


class GoodExample(BaseModel):
    """
    A good example of the kind of question to generate
    """

    question_text: Annotated[str, Field(..., description="Example question text")]
    explanation: Annotated[
        Optional[str],
        Field(None, description="Explanation of why this is a good example"),
    ]

    def to_example_in_schema(self) -> "ExampleInSchema":
        return ExampleInSchema(
            example_type=ExampleType.GOOD,
            example_text=self.question_text,
            explanation=self.explanation,
        )


class BadExample(BaseModel):
    """
    A bad example (counter-example) of the kind of question to generate
    """

    question_text: Annotated[str, Field(..., description="Example question text")]
    explanation: Annotated[
        Optional[str],
        Field(None, description="Explanation of why this is a counter-example"),
    ]

    def to_example_in_schema(self) -> "ExampleInSchema":
        return ExampleInSchema(
            example_text=self.question_text,
            explanation=self.explanation,
            example_type=ExampleType.BAD,
        )


class BaseTestResponse(BaseModel):
    """
    Test response. May or may not have questions, depending on the test status.
    """

    test_uuid: Annotated[str, Field(..., description="UUID of the test")]
    test_type: Annotated[TestType, Field(..., description="Type of the test")]
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

    good_examples: Annotated[
        Optional[List[GoodExample]],
        Field(None, description="Good examples for the test"),
    ]
    bad_examples: Annotated[
        Optional[List[BadExample]],
        Field(None, description="Bad examples for the test"),
    ]

    def to_questions_df(self) -> pd.DataFrame:
        """Create a questions DataFrame."""

        if not self.questions:
            return pd.DataFrame()

        rows = [
            {
                "test_uuid": self.test_uuid,
                "test_name": self.test_name,
                "question_uuid": question.question_uuid,
                "question_text": question.question_text,
                **(
                    {"accuracy_question_type": question.accuracy_question_type}
                    if self.test_type == TestType.ACCURACY
                    else {}
                ),
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
            "test_type": test.test_type,
            "test_name": test.test_name,
            "test_status": Status.from_api_status(test.test_status),
            "created_at": test.created_at,
            "num_test_questions": test.num_test_questions,
            "failure_reason": failure_reason,
            "good_examples": [
                GoodExample(question_text=e.example_text, explanation=e.explanation)
                for e in test.test_examples
                if e.example_type == ExampleType.GOOD
            ]
            if test.test_examples
            else None,
            "bad_examples": [
                BadExample(question_text=e.example_text, explanation=e.explanation)
                for e in test.test_examples
                if e.example_type == ExampleType.BAD
            ]
            if test.test_examples
            else None,
        }
        if test.test_type == TestType.SAFETY or test.test_type == TestType.IMAGE_SAFETY:
            questions = (
                [QuestionResponse.from_question_schema(q) for q in questions]
                if questions
                else None
            )
            return SafetyTestResponse(
                **base_attributes, test_policy=test.test_policy, questions=questions
            )
        elif test.test_type == TestType.JAILBREAK:
            questions = (
                [QuestionResponse.from_question_schema(q) for q in questions]
                if questions
                else None
            )
            return JailbreakTestResponse(
                **base_attributes,
                test_system_prompt=test.test_system_prompt,
                questions=questions,
            )
        elif test.test_type == TestType.ACCURACY:
            questions = (
                [AccuracyQuestionResponse.from_question_schema(q) for q in questions]
                if questions
                else None
            )

            return AccuracyTestResponse(
                **base_attributes,
                knowledge_base=test.knowledge_base,
                questions=questions,
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


class AccuracyTestResponse(BaseTestResponse):
    """
    Accuracy test response.
    """

    knowledge_base: Annotated[
        str, Field(..., description="Knowledge base to test against")
    ]
    questions: Annotated[
        Optional[List[AccuracyQuestionResponse]],
        Field(None, description="Questions in the test"),
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
            elif isinstance(test, AccuracyTestResponse):
                row["knowledge_base"] = test.knowledge_base

            rows.append(row)
        return pd.DataFrame(rows)


class ScoredAnswerResponse(BaseModel):
    """
    A single answer to a question in the test that has been scored.
    """

    answer_uuid: Annotated[str, Field(..., description="UUID of the answer")]
    question_uuid: Annotated[str, Field(..., description="UUID of the question")]
    answer_text: Annotated[
        Optional[str], Field(default=None, description="Answer to the question")
    ]
    answer_image_path: Annotated[
        Optional[str], Field(default=None, description="Path to the answer image")
    ]
    answer_image_url: Annotated[
        Optional[str], Field(default=None, description="URL to the answer image")
    ]
    question_text: Annotated[str, Field(..., description="Question in the test")]
    explanation: Annotated[
        Optional[str], Field(default=None, description="Explanation for the score")
    ]
    confidence: Annotated[
        Optional[float], Field(default=None, description="Confidence score")
    ]
    is_passed: Annotated[
        Optional[bool], Field(default=None, description="Whether the answer is passed")
    ]
    exclude_from_scoring: Annotated[
        bool,
        Field(
            default=False,
            description="Whether the answer is excluded from scoring",
        ),
    ]
    student_refused: Annotated[
        bool,
        Field(
            default=False,
            description="Whether the student refused to answer",
        ),
    ]

    @classmethod
    def from_answer_out_schema(cls, answer: AnswerOutSchema) -> "ScoredAnswerResponse":
        # Handle potential Unset values for answer_text and answer_image_path
        answer_text = (
            None
            if not hasattr(answer, "answer_text") or answer.answer_text is None
            else str(answer.answer_text)
        )
        answer_image_path = (
            None
            if not hasattr(answer, "answer_image_path")
            or answer.answer_image_path is None
            else str(answer.answer_image_path)
        )
        answer_image_url = (
            None
            if not hasattr(answer, "answer_image_url")
            or answer.answer_image_url is None
            else str(answer.answer_image_url)
        )

        return cls(
            answer_uuid=answer.answer_uuid,
            question_uuid=answer.question.question_uuid,
            answer_text=answer_text,
            answer_image_path=answer_image_path,
            answer_image_url=answer_image_url,
            question_text=answer.question.question_text,
            explanation=answer.explanation,
            confidence=answer.confidence,
            is_passed=answer.is_passed,
            exclude_from_scoring=answer.exclude_from_scoring,
            student_refused=answer.student_refused,
        )


class AccuracyScoredAnswerResponse(ScoredAnswerResponse):
    """
    A single answer to a question in the test that has been scored.
    """

    accuracy_question_type: Annotated[
        str, Field(..., description="Type of the question for accuracy tests")
    ]

    @classmethod
    def from_answer_out_schema(
        cls, answer: AnswerOutSchema
    ) -> "AccuracyScoredAnswerResponse":
        # Handle potential Unset values for answer_text
        answer_text = (
            None
            if not hasattr(answer, "answer_text") or answer.answer_text is None
            else str(answer.answer_text)
        )

        return cls(
            answer_uuid=answer.answer_uuid,
            question_uuid=answer.question.question_uuid,
            answer_text=answer_text,
            question_text=answer.question.question_text,
            accuracy_question_type=answer.question.accuracy_question_type,
            explanation=answer.explanation,
            confidence=answer.confidence,
            is_passed=answer.is_passed,
            excluded_from_scoring=answer.exclude_from_scoring,
            is_refusal=answer.student_refused,
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

    pass_rate: Annotated[
        Optional[float], Field(None, description="Pass rate of the score run")
    ]

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
                    "answer_image_path": answer.answer_image_path,
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
        base_attributes = {
            "score_run_uuid": score_run.score_run_uuid,
            "score_run_status": Status.from_api_status(score_run.score_run_status),
            "test": BaseTestResponse.from_test_out_schema_and_questions(
                score_run.test,
                questions=[answer.question for answer in answers]
                if answers is not None
                else None,
            ),
            "created_at": score_run.created_at,
            "failure_reason": failure_reason,
            "pass_rate": score_run.pass_rate,
        }
        if score_run.test.test_type == TestType.ACCURACY:
            answers = (
                [
                    AccuracyScoredAnswerResponse.from_answer_out_schema(answer)
                    for answer in answers
                ]
                if answers
                else None
            )
            return AccuracyScoreRunResponse(
                **base_attributes,
                answers=answers,
            )
        else:
            answers = (
                [
                    ScoredAnswerResponse.from_answer_out_schema(answer)
                    for answer in answers
                ]
                if answers
                else None
            )

        return cls(
            **base_attributes,
            answers=answers,
        )


class AccuracyScoreRunResponse(ScoreRunResponse):
    """
    Score run response for accuracy tests.
    """

    answers: Annotated[
        Optional[List[AccuracyScoredAnswerResponse]],
        Field(None, description="List of scored answers"),
    ]

    def to_scores_df(self) -> pd.DataFrame:
        """Create a scores DataFrame."""
        rows = (
            [
                {
                    "score_run_uuid": self.score_run_uuid,
                    "test_uuid": self.test.test_uuid,
                    "test_name": self.test.test_name,
                    "question_type": answer.accuracy_question_type,
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
                "pass_rate": score_run.pass_rate,
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
    passing_answers_summary: Annotated[
        str, Field(..., description="Summary of the passing answers")
    ]
    failing_answers_summary: Annotated[
        str, Field(..., description="Summary of the failing answers")
    ]
    improvement_advice: Annotated[str, Field(..., description="Advice for improvement")]
    test_name: Annotated[str, Field(..., description="Name of the test")]
    test_type: Annotated[TestType, Field(..., description="Type of the test")]
    score_run_uuid: Annotated[str, Field(..., description="UUID of the score run")]

    @classmethod
    def from_score_run_summary_out_schema(
        cls, summary: ScoreRunSummaryOutSchema
    ) -> "ScoreRunSummaryResponse":
        return cls(
            score_run_summary_uuid=summary.score_run_summary_uuid,
            passing_answers_summary=summary.passing_answers_summary,
            failing_answers_summary=summary.failing_answers_summary,
            improvement_advice=summary.improvement_advice,
            test_name=summary.score_run.test.test_name,
            test_type=summary.score_run.test.test_type,
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

    overall_passing_answers_summary: Annotated[
        Optional[str], Field(None, description="Summary of the passing answers")
    ]
    overall_failing_answers_summary: Annotated[
        Optional[str], Field(None, description="Summary of the failing answers")
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

        rows = []
        for summary in self.score_run_summaries:
            if summary.test_type == TestType.ACCURACY:
                # Extract sections using XML tags
                passing_sections = re.findall(
                    r"<(\w+)>(.*?)</\1>", summary.passing_answers_summary, re.DOTALL
                )
                failing_sections = (
                    re.findall(
                        r"<(\w+)>(.*?)</\1>", summary.failing_answers_summary, re.DOTALL
                    )
                    if summary.failing_answers_summary
                    else []
                )
                advice_sections = re.findall(
                    r"<(\w+)>(.*?)</\1>", summary.improvement_advice, re.DOTALL
                )

                # Create a mapping of question types to their content
                passing_by_type = {
                    tag: content.strip() for tag, content in passing_sections
                }
                failing_by_type = {
                    tag: content.strip() for tag, content in failing_sections
                }
                advice_by_type = {
                    tag: content.strip() for tag, content in advice_sections
                }

                # Get ordered unique question types while preserving order
                question_types = []
                for tag, _ in passing_sections + failing_sections:
                    if tag not in question_types:
                        question_types.append(tag)

                # Create a row for each question type
                for q_type in question_types:
                    rows.append(
                        {
                            "test_name": summary.test_name,
                            "question_type": q_type,
                            "passing_answers_summary": passing_by_type.get(q_type, ""),
                            "failing_answers_summary": failing_by_type.get(q_type, ""),
                            "improvement_advice": advice_by_type.get(q_type, ""),
                        }
                    )
            else:
                # Handle non-accuracy tests as before
                rows.append(
                    {
                        "test_name": summary.test_name,
                        "passing_answers_summary": summary.passing_answers_summary,
                        "failing_answers_summary": summary.failing_answers_summary,
                        "improvement_advice": summary.improvement_advice,
                    }
                )

        # Add overall summary if available
        if self.overall_passing_answers_summary or self.overall_failing_answers_summary:
            rows.append(
                {
                    "test_name": "Overall",
                    "passing_answers_summary": self.overall_passing_answers_summary,
                    "failing_answers_summary": self.overall_failing_answers_summary,
                    "improvement_advice": self.overall_improvement_advice,
                }
            )

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
            overall_passing_answers_summary=summary.overall_passing_answers_summary,
            overall_failing_answers_summary=summary.overall_failing_answers_summary,
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

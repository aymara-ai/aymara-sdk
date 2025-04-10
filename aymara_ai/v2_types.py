"""
Types for the SDK
"""

import re
from datetime import datetime
from typing import Annotated, Iterator, List, Optional

import pandas as pd
from pydantic import BaseModel, Field, RootModel

from aymara_ai.generated.aymara_api_client.models.eval_out_schema import EvalOutSchema
from aymara_ai.generated.aymara_api_client.models.eval_prompt_schema import EvalPromptSchema
from aymara_ai.generated.aymara_api_client.models.eval_response_out_schema import EvalResponseOutSchema
from aymara_ai.generated.aymara_api_client.models.eval_run_out_schema import EvalRunOutSchema
from aymara_ai.generated.aymara_api_client.models.eval_run_suite_summary_out_schema import EvalRunSuiteSummaryOutSchema
from aymara_ai.generated.aymara_api_client.models.eval_run_summary_out_schema import EvalRunSummaryOutSchema
from aymara_ai.generated.aymara_api_client.models.example_in_schema import ExampleInSchema
from aymara_ai.generated.aymara_api_client.models.example_type import ExampleType
from aymara_ai.generated.aymara_api_client.models.question_schema import QuestionSchema
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import (
    Status,
)


class EvalResponse(BaseModel):
    eval: EvalOutSchema
    prompts: Annotated[
        Optional[List[EvalPromptSchema]],
        Field(None, description="List of eval prompts"),
    ]

    model_config = {
        "arbitrary_types_allowed": True,
    }

    def to_df(self) -> pd.DataFrame:
        """Create a prompts DataFrame."""

        if not self.prompts:
            return pd.DataFrame()

        rows = [
            {"eval_uuid": self.eval.eval_uuid, "eval_name": self.eval.name, **prompt.to_dict()}
            for prompt in self.prompts
        ]

        return pd.DataFrame(rows)


class PromptExample(BaseModel):
    """
    An example to guide prompt generation
    """

    content: Annotated[str, Field(..., description="Example content")]
    explanation: Annotated[
        Optional[str],
        Field(None, description="Explanation of why this is example is good or bad"),
    ]
    is_bad: Annotated[bool, Field(False, description="Whether to use this as a bad example")]

    def to_example_in_schema(self) -> "ExampleInSchema":
        return ExampleInSchema(
            example_type=ExampleType.BAD if self.is_bad else ExampleType.GOOD,
            example_text=self.content,
            explanation=self.explanation,
        )


class GroundTruth(BaseModel):
    """
    Ground truth options for the evaluation
    """

    kb: Annotated[str, Field(..., description="Knowledgebase corpus to use for the evaluation")]
    category: Annotated[Optional[str], Field(None, description="The type of prompts to generate from the corpus")]


class EvalPrompt(BaseModel):
    """
    Prompt in the eval
    """

    prompt_uuid: Annotated[str, Field(..., description="UUID of the question")]
    content: Annotated[str, Field(..., description="Question in the test")]

    category: Annotated[
        Optional[str],
        Field(None, description="Type of the prompt"),
    ]

    @classmethod
    def from_question_schema(cls, question: QuestionSchema) -> "EvalPrompt":
        return cls(
            prompt_uuid=question.question_uuid,
            content=question.question_text,
            category=getattr(question, "accuracy_question_type", None),
        )

    def to_question_schema(self) -> QuestionSchema:
        return QuestionSchema(
            question_uuid=self.prompt_uuid,
            question_text=self.content,
        )


class ListEval(RootModel):
    """
    List of Evals.
    """

    root: List[EvalResponse]

    def __iter__(self) -> Iterator[EvalResponse]:
        return iter(self.root)

    def __getitem__(self, index) -> EvalResponse:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

    def to_df(self) -> pd.DataFrame:
        """Create a DataFrame from the list of TestResponses."""
        rows = []
        for eval_resp in self.root:
            row = {
                "eval_uuid": eval_resp.eval.eval_uuid,
                "name": eval_resp.eval.name,
                "status": eval_resp.eval.status.value,
                "created_at": eval_resp.eval.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "failure_reason": eval_resp.eval.status.value,
                "num_prompts": eval_resp.eval.num_prompts,
            }

            if eval_resp.eval.ai_instructions:
                row["ai_instructions"] = eval_resp.eval.ai_instructions

            rows.append(row)
        return pd.DataFrame(rows)


class EvalRunResponse(BaseModel):
    """
    Score run response. May or may not have repsonses, depending on the eval run status.
    """

    eval_run_uuid: Annotated[str, Field(..., description="UUID of the eval run")]
    failure_reason: Annotated[Optional[str], Field(None, description="Reason for the eval run failure")]

    run: Annotated[EvalRunOutSchema, Field(..., description="Eval")]
    responses: Annotated[
        Optional[List[EvalResponseOutSchema]],
        Field(None, description="List of scored responses"),
    ]

    model_config = {
        "arbitrary_types_allowed": True,
    }

    def to_df(self) -> pd.DataFrame:
        """Create a responses DataFrame."""
        rows = (
            [
                {
                    "eval_run_uuid": self.eval_run_uuid,
                    "eval_uuid": self.run.evaluation.eval_uuid,
                    "eval_name": self.run.evaluation.name,
                    "response_uuid": response.response_uuid,
                    "prompt_uuid": response.prompt_uuid,
                    "is_passed": response.is_passed,
                    "prompt": response.prompt.content,
                    "response_content": response.content,
                    "explanation": response.explanation,
                    "confidence": response.confidence,
                }
                for response in self.responses
            ]
            if self.responses
            else []
        )

        return pd.DataFrame(rows)


class ListEvalRunResponse(RootModel):
    """
    List of score runs.
    """

    root: List["EvalRunResponse"]

    def __iter__(self) -> Iterator[EvalRunResponse]:
        return iter(self.root)

    def __getitem__(self, index) -> EvalRunResponse:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

    def to_df(self) -> pd.DataFrame:
        """Create a DataFrame from the list of EvalRunResponses."""
        rows = []
        for eval_run in self.root:
            row = {
                "eval_run_uuid": eval_run.eval_run_uuid,
                "eval_uuid": eval_run.run.evaluation.eval_uuid,
                "eval_name": eval_run.run.evaluation.name,
                "eval_run_status": eval_run.run.status.value,
                "created_at": eval_run.run.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "failure_reason": eval_run.failure_reason,
                "num_prompts": eval_run.run.evaluation.num_prompts,
                "pass_rate": eval_run.run.pass_rate,
            }
            rows.append(row)
        return pd.DataFrame(rows)


class EvalRunSummaryResponse(BaseModel):
    """
    Score run summary response.
    """

    eval_run_summary_uuid: Annotated[str, Field(..., description="UUID of the score run summary")]
    passing_responses_summary: Annotated[str, Field(..., description="Summary of the passing answers")]
    failing_responses_summary: Annotated[str, Field(..., description="Summary of the failing answers")]
    improvement_advice: Annotated[str, Field(..., description="Advice for improvement")]
    eval_name: Annotated[str, Field(..., description="Name of the test")]
    eval_type: Annotated[TestType, Field(..., description="Type of the test")]
    eval_run_uuid: Annotated[str, Field(..., description="UUID of the score run")]

    @classmethod
    def from_eval_run_summary_out_schema(cls, summary: EvalRunSummaryOutSchema) -> "EvalRunSummaryResponse":
        return cls(
            eval_run_summary_uuid=summary.eval_run_summary_uuid,
            passing_responses_summary=summary.passing_responses_summary,
            failing_responses_summary=summary.failing_responses_summary,
            improvement_advice=summary.improvement_advice,
            eval_name=summary.eval_run.evaluation.name,
            eval_type=summary.eval_run.evaluation.eval_type,
            eval_run_uuid=summary.eval_run.eval_run_uuid,
        )


class EvalRunSuiteSummaryResponse(BaseModel):
    """
    Score run suite summary response.
    """

    eval_run_suite_summary_uuid: Annotated[str, Field(..., description="UUID of the score run suite summary")]

    eval_run_suite_summary_status: Annotated[Status, Field(..., description="Status of the score run suite summary")]

    overall_passing_responses_summary: Annotated[
        Optional[str], Field(None, description="Summary of the passing answers")
    ]
    overall_failing_responses_summary: Annotated[
        Optional[str], Field(None, description="Summary of the failing answers")
    ]
    overall_improvement_advice: Annotated[Optional[str], Field(None, description="Advice for improvement")]

    eval_run_summaries: Annotated[
        List[EvalRunSummaryResponse],
        Field(..., description="List of score run summaries"),
    ]

    created_at: Annotated[
        datetime,
        Field(..., description="Timestamp of the score run suite summary creation"),
    ]

    failure_reason: Annotated[Optional[str], Field(None, description="Reason for the score run failure")]

    def to_df(self) -> pd.DataFrame:
        """Create a scores DataFrame."""

        rows = []
        for summary in self.eval_run_summaries:
            if summary.eval_type == TestType.ACCURACY:
                # Extract sections using XML tags
                passing_sections = re.findall(r"<(\w+)>(.*?)</\1>", summary.passing_responses_summary, re.DOTALL)
                failing_sections = (
                    re.findall(r"<(\w+)>(.*?)</\1>", summary.failing_responses_summary, re.DOTALL)
                    if summary.failing_responses_summary
                    else []
                )
                advice_sections = re.findall(r"<(\w+)>(.*?)</\1>", summary.improvement_advice, re.DOTALL)

                # Create a mapping of question types to their content
                passing_by_type = {tag: content.strip() for tag, content in passing_sections}
                failing_by_type = {tag: content.strip() for tag, content in failing_sections}
                advice_by_type = {tag: content.strip() for tag, content in advice_sections}

                # Get ordered unique question types while preserving order
                question_types = []
                for tag, _ in passing_sections + failing_sections:
                    if tag not in question_types:
                        question_types.append(tag)

                # Create a row for each question type
                for q_type in question_types:
                    rows.append(
                        {
                            "eval_name": summary.eval_name,
                            "question_type": q_type,
                            "passing_responses_summary": passing_by_type.get(q_type, ""),
                            "failing_responses_summary": failing_by_type.get(q_type, ""),
                            "improvement_advice": advice_by_type.get(q_type, ""),
                        }
                    )
            else:
                # Handle non-accuracy tests as before
                rows.append(
                    {
                        "eval_name": summary.eval_name,
                        "passing_responses_summary": summary.passing_responses_summary,
                        "failing_responses_summary": summary.failing_responses_summary,
                        "improvement_advice": summary.improvement_advice,
                    }
                )

        # Add overall summary if available
        if self.overall_passing_responses_summary or self.overall_failing_responses_summary:
            rows.append(
                {
                    "eval_name": "Overall",
                    "passing_responses_summary": self.overall_passing_responses_summary,
                    "failing_responses_summary": self.overall_failing_responses_summary,
                    "improvement_advice": self.overall_improvement_advice,
                }
            )

        return pd.DataFrame(rows)

    @classmethod
    def from_summary_out_schema_and_failure_reason(
        cls,
        summary: EvalRunSuiteSummaryOutSchema,
        failure_reason: Optional[str] = None,
    ) -> "EvalRunSuiteSummaryResponse":
        return cls(
            eval_run_suite_summary_uuid=summary.eval_run_suite_summary_uuid,
            eval_run_suite_summary_status=Status.from_api_status(summary.status),
            overall_passing_responses_summary=summary.overall_passing_responses_summary,
            overall_failing_responses_summary=summary.overall_failing_responses_summary,
            overall_improvement_advice=summary.overall_improvement_advice,
            eval_run_summaries=[
                EvalRunSummaryResponse.from_eval_run_summary_out_schema(summary)
                for summary in summary.eval_run_summaries
            ],
            created_at=summary.created_at,
            failure_reason=failure_reason,
        )


class ListEvalRunSuiteSummaryResponse(RootModel):
    """
    List of score run suite summaries.
    """

    root: List["EvalRunSuiteSummaryResponse"]

    def __iter__(self) -> Iterator[EvalRunSuiteSummaryResponse]:
        return iter(self.root)

    def __getitem__(self, index) -> EvalRunSuiteSummaryResponse:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

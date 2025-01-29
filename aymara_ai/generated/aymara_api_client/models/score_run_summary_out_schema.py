from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.score_run_out_schema import ScoreRunOutSchema


T = TypeVar("T", bound="ScoreRunSummaryOutSchema")


@_attrs_define
class ScoreRunSummaryOutSchema:
    """
    Attributes:
        score_run_summary_uuid (str):
        score_run (ScoreRunOutSchema):
        passing_answers_summary (str):
        failing_answers_summary (str):
        improvement_advice (str):
        explanation_summary (str):
    """

    score_run_summary_uuid: str
    score_run: "ScoreRunOutSchema"
    passing_answers_summary: str
    failing_answers_summary: str
    improvement_advice: str
    explanation_summary: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        score_run_summary_uuid = self.score_run_summary_uuid

        score_run = self.score_run.to_dict()

        passing_answers_summary = self.passing_answers_summary

        failing_answers_summary = self.failing_answers_summary

        improvement_advice = self.improvement_advice

        explanation_summary = self.explanation_summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score_run_summary_uuid": score_run_summary_uuid,
                "score_run": score_run,
                "passing_answers_summary": passing_answers_summary,
                "failing_answers_summary": failing_answers_summary,
                "improvement_advice": improvement_advice,
                "explanation_summary": explanation_summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.score_run_out_schema import ScoreRunOutSchema

        d = src_dict.copy()
        score_run_summary_uuid = d.pop("score_run_summary_uuid")

        score_run = ScoreRunOutSchema.from_dict(d.pop("score_run"))

        passing_answers_summary = d.pop("passing_answers_summary")

        failing_answers_summary = d.pop("failing_answers_summary")

        improvement_advice = d.pop("improvement_advice")

        explanation_summary = d.pop("explanation_summary")

        score_run_summary_out_schema = cls(
            score_run_summary_uuid=score_run_summary_uuid,
            score_run=score_run,
            passing_answers_summary=passing_answers_summary,
            failing_answers_summary=failing_answers_summary,
            improvement_advice=improvement_advice,
            explanation_summary=explanation_summary,
        )

        score_run_summary_out_schema.additional_properties = d
        return score_run_summary_out_schema

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

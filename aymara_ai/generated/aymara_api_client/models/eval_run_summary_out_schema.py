from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.eval_run_out_schema import EvalRunOutSchema


T = TypeVar("T", bound="EvalRunSummaryOutSchema")


@_attrs_define
class EvalRunSummaryOutSchema:
    """
    Attributes:
        eval_run_summary_uuid (str):
        eval_run_uuid (str):
        eval_run (EvalRunOutSchema): Schema for returning eval run data.
        passing_responses_summary (str):
        failing_responses_summary (str):
        improvement_advice (str):
    """

    eval_run_summary_uuid: str
    eval_run_uuid: str
    eval_run: "EvalRunOutSchema"
    passing_responses_summary: str
    failing_responses_summary: str
    improvement_advice: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        eval_run_summary_uuid = self.eval_run_summary_uuid

        eval_run_uuid = self.eval_run_uuid

        eval_run = self.eval_run.to_dict()

        passing_responses_summary = self.passing_responses_summary

        failing_responses_summary = self.failing_responses_summary

        improvement_advice = self.improvement_advice

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eval_run_summary_uuid": eval_run_summary_uuid,
                "eval_run_uuid": eval_run_uuid,
                "eval_run": eval_run,
                "passing_responses_summary": passing_responses_summary,
                "failing_responses_summary": failing_responses_summary,
                "improvement_advice": improvement_advice,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_run_out_schema import EvalRunOutSchema

        d = src_dict.copy()
        eval_run_summary_uuid = d.pop("eval_run_summary_uuid")

        eval_run_uuid = d.pop("eval_run_uuid")

        eval_run = EvalRunOutSchema.from_dict(d.pop("eval_run"))

        passing_responses_summary = d.pop("passing_responses_summary")

        failing_responses_summary = d.pop("failing_responses_summary")

        improvement_advice = d.pop("improvement_advice")

        eval_run_summary_out_schema = cls(
            eval_run_summary_uuid=eval_run_summary_uuid,
            eval_run_uuid=eval_run_uuid,
            eval_run=eval_run,
            passing_responses_summary=passing_responses_summary,
            failing_responses_summary=failing_responses_summary,
            improvement_advice=improvement_advice,
        )

        eval_run_summary_out_schema.additional_properties = d
        return eval_run_summary_out_schema

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

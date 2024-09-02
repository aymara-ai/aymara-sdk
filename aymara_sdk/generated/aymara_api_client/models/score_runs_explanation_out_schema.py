from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.explanation_status import ExplanationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.score_run_explanation_out_schema import ScoreRunExplanationOutSchema


T = TypeVar("T", bound="ScoreRunsExplanationOutSchema")


@_attrs_define
class ScoreRunsExplanationOutSchema:
    """
    Attributes:
        score_runs_explanation_uuid (str):
        status (ExplanationStatus):
        score_run_explanations (List['ScoreRunExplanationOutSchema']):
        overall_improvement_advice (Union[None, Unset, str]):
        overall_explanation_summary (Union[None, Unset, str]):
    """

    score_runs_explanation_uuid: str
    status: ExplanationStatus
    score_run_explanations: List["ScoreRunExplanationOutSchema"]
    overall_improvement_advice: Union[None, Unset, str] = UNSET
    overall_explanation_summary: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        score_runs_explanation_uuid = self.score_runs_explanation_uuid

        status = self.status.value

        score_run_explanations = []
        for score_run_explanations_item_data in self.score_run_explanations:
            score_run_explanations_item = score_run_explanations_item_data.to_dict()
            score_run_explanations.append(score_run_explanations_item)

        overall_improvement_advice: Union[None, Unset, str]
        if isinstance(self.overall_improvement_advice, Unset):
            overall_improvement_advice = UNSET
        else:
            overall_improvement_advice = self.overall_improvement_advice

        overall_explanation_summary: Union[None, Unset, str]
        if isinstance(self.overall_explanation_summary, Unset):
            overall_explanation_summary = UNSET
        else:
            overall_explanation_summary = self.overall_explanation_summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score_runs_explanation_uuid": score_runs_explanation_uuid,
                "status": status,
                "score_run_explanations": score_run_explanations,
            }
        )
        if overall_improvement_advice is not UNSET:
            field_dict["overall_improvement_advice"] = overall_improvement_advice
        if overall_explanation_summary is not UNSET:
            field_dict["overall_explanation_summary"] = overall_explanation_summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.score_run_explanation_out_schema import ScoreRunExplanationOutSchema

        d = src_dict.copy()
        score_runs_explanation_uuid = d.pop("score_runs_explanation_uuid")

        status = ExplanationStatus(d.pop("status"))

        score_run_explanations = []
        _score_run_explanations = d.pop("score_run_explanations")
        for score_run_explanations_item_data in _score_run_explanations:
            score_run_explanations_item = ScoreRunExplanationOutSchema.from_dict(score_run_explanations_item_data)

            score_run_explanations.append(score_run_explanations_item)

        def _parse_overall_improvement_advice(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        overall_improvement_advice = _parse_overall_improvement_advice(d.pop("overall_improvement_advice", UNSET))

        def _parse_overall_explanation_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        overall_explanation_summary = _parse_overall_explanation_summary(d.pop("overall_explanation_summary", UNSET))

        score_runs_explanation_out_schema = cls(
            score_runs_explanation_uuid=score_runs_explanation_uuid,
            status=status,
            score_run_explanations=score_run_explanations,
            overall_improvement_advice=overall_improvement_advice,
            overall_explanation_summary=overall_explanation_summary,
        )

        score_runs_explanation_out_schema.additional_properties = d
        return score_runs_explanation_out_schema

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

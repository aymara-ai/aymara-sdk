from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.score_run_suite_summary_status import ScoreRunSuiteSummaryStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.score_run_summary_out_schema import ScoreRunSummaryOutSchema


T = TypeVar("T", bound="ScoreRunSuiteSummaryOutSchema")


@_attrs_define
class ScoreRunSuiteSummaryOutSchema:
    """
    Attributes:
        score_run_suite_summary_uuid (str):
        status (ScoreRunSuiteSummaryStatus):
        score_run_summaries (List['ScoreRunSummaryOutSchema']):
        overall_improvement_advice (Union[None, Unset, str]):
        overall_summary (Union[None, Unset, str]):
    """

    score_run_suite_summary_uuid: str
    status: ScoreRunSuiteSummaryStatus
    score_run_summaries: List["ScoreRunSummaryOutSchema"]
    overall_improvement_advice: Union[None, Unset, str] = UNSET
    overall_summary: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        score_run_suite_summary_uuid = self.score_run_suite_summary_uuid

        status = self.status.value

        score_run_summaries = []
        for score_run_summaries_item_data in self.score_run_summaries:
            score_run_summaries_item = score_run_summaries_item_data.to_dict()
            score_run_summaries.append(score_run_summaries_item)

        overall_improvement_advice: Union[None, Unset, str]
        if isinstance(self.overall_improvement_advice, Unset):
            overall_improvement_advice = UNSET
        else:
            overall_improvement_advice = self.overall_improvement_advice

        overall_summary: Union[None, Unset, str]
        if isinstance(self.overall_summary, Unset):
            overall_summary = UNSET
        else:
            overall_summary = self.overall_summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score_run_suite_summary_uuid": score_run_suite_summary_uuid,
                "status": status,
                "score_run_summaries": score_run_summaries,
            }
        )
        if overall_improvement_advice is not UNSET:
            field_dict["overall_improvement_advice"] = overall_improvement_advice
        if overall_summary is not UNSET:
            field_dict["overall_summary"] = overall_summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.score_run_summary_out_schema import ScoreRunSummaryOutSchema

        d = src_dict.copy()
        score_run_suite_summary_uuid = d.pop("score_run_suite_summary_uuid")

        status = ScoreRunSuiteSummaryStatus(d.pop("status"))

        score_run_summaries = []
        _score_run_summaries = d.pop("score_run_summaries")
        for score_run_summaries_item_data in _score_run_summaries:
            score_run_summaries_item = ScoreRunSummaryOutSchema.from_dict(score_run_summaries_item_data)

            score_run_summaries.append(score_run_summaries_item)

        def _parse_overall_improvement_advice(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        overall_improvement_advice = _parse_overall_improvement_advice(d.pop("overall_improvement_advice", UNSET))

        def _parse_overall_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        overall_summary = _parse_overall_summary(d.pop("overall_summary", UNSET))

        score_run_suite_summary_out_schema = cls(
            score_run_suite_summary_uuid=score_run_suite_summary_uuid,
            status=status,
            score_run_summaries=score_run_summaries,
            overall_improvement_advice=overall_improvement_advice,
            overall_summary=overall_summary,
        )

        score_run_suite_summary_out_schema.additional_properties = d
        return score_run_suite_summary_out_schema

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
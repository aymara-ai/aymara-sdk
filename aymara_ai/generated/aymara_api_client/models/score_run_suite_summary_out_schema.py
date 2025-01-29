import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

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
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        overall_improvement_advice (Union[None, Unset, str]):
        overall_failing_answers_summary (Union[None, Unset, str]):
        overall_passing_answers_summary (Union[None, Unset, str]):
        overall_summary (Union[None, Unset, str]):
        remaining_summaries (Union[None, Unset, int]):
    """

    score_run_suite_summary_uuid: str
    status: ScoreRunSuiteSummaryStatus
    score_run_summaries: List["ScoreRunSummaryOutSchema"]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    overall_improvement_advice: Union[None, Unset, str] = UNSET
    overall_failing_answers_summary: Union[None, Unset, str] = UNSET
    overall_passing_answers_summary: Union[None, Unset, str] = UNSET
    overall_summary: Union[None, Unset, str] = UNSET
    remaining_summaries: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        score_run_suite_summary_uuid = self.score_run_suite_summary_uuid

        status = self.status.value

        score_run_summaries = []
        for score_run_summaries_item_data in self.score_run_summaries:
            score_run_summaries_item = score_run_summaries_item_data.to_dict()
            score_run_summaries.append(score_run_summaries_item)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        overall_improvement_advice: Union[None, Unset, str]
        if isinstance(self.overall_improvement_advice, Unset):
            overall_improvement_advice = UNSET
        else:
            overall_improvement_advice = self.overall_improvement_advice

        overall_failing_answers_summary: Union[None, Unset, str]
        if isinstance(self.overall_failing_answers_summary, Unset):
            overall_failing_answers_summary = UNSET
        else:
            overall_failing_answers_summary = self.overall_failing_answers_summary

        overall_passing_answers_summary: Union[None, Unset, str]
        if isinstance(self.overall_passing_answers_summary, Unset):
            overall_passing_answers_summary = UNSET
        else:
            overall_passing_answers_summary = self.overall_passing_answers_summary

        overall_summary: Union[None, Unset, str]
        if isinstance(self.overall_summary, Unset):
            overall_summary = UNSET
        else:
            overall_summary = self.overall_summary

        remaining_summaries: Union[None, Unset, int]
        if isinstance(self.remaining_summaries, Unset):
            remaining_summaries = UNSET
        else:
            remaining_summaries = self.remaining_summaries

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score_run_suite_summary_uuid": score_run_suite_summary_uuid,
                "status": status,
                "score_run_summaries": score_run_summaries,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if overall_improvement_advice is not UNSET:
            field_dict["overall_improvement_advice"] = overall_improvement_advice
        if overall_failing_answers_summary is not UNSET:
            field_dict["overall_failing_answers_summary"] = overall_failing_answers_summary
        if overall_passing_answers_summary is not UNSET:
            field_dict["overall_passing_answers_summary"] = overall_passing_answers_summary
        if overall_summary is not UNSET:
            field_dict["overall_summary"] = overall_summary
        if remaining_summaries is not UNSET:
            field_dict["remaining_summaries"] = remaining_summaries

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

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_overall_improvement_advice(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        overall_improvement_advice = _parse_overall_improvement_advice(d.pop("overall_improvement_advice", UNSET))

        def _parse_overall_failing_answers_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        overall_failing_answers_summary = _parse_overall_failing_answers_summary(
            d.pop("overall_failing_answers_summary", UNSET)
        )

        def _parse_overall_passing_answers_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        overall_passing_answers_summary = _parse_overall_passing_answers_summary(
            d.pop("overall_passing_answers_summary", UNSET)
        )

        def _parse_overall_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        overall_summary = _parse_overall_summary(d.pop("overall_summary", UNSET))

        def _parse_remaining_summaries(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        remaining_summaries = _parse_remaining_summaries(d.pop("remaining_summaries", UNSET))

        score_run_suite_summary_out_schema = cls(
            score_run_suite_summary_uuid=score_run_suite_summary_uuid,
            status=status,
            score_run_summaries=score_run_summaries,
            created_at=created_at,
            updated_at=updated_at,
            overall_improvement_advice=overall_improvement_advice,
            overall_failing_answers_summary=overall_failing_answers_summary,
            overall_passing_answers_summary=overall_passing_answers_summary,
            overall_summary=overall_summary,
            remaining_summaries=remaining_summaries,
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

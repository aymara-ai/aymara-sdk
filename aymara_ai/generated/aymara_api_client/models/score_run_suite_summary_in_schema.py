from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScoreRunSuiteSummaryInSchema")


@_attrs_define
class ScoreRunSuiteSummaryInSchema:
    """
    Attributes:
        score_run_uuids (List[str]):
    """

    score_run_uuids: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        score_run_uuids = self.score_run_uuids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score_run_uuids": score_run_uuids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        score_run_uuids = cast(List[str], d.pop("score_run_uuids"))

        score_run_suite_summary_in_schema = cls(
            score_run_uuids=score_run_uuids,
        )

        score_run_suite_summary_in_schema.additional_properties = d
        return score_run_suite_summary_in_schema

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

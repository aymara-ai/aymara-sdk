import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.score_run_status import ScoreRunStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_out_schema import TestOutSchema


T = TypeVar("T", bound="ScoreRunOutSchema")


@_attrs_define
class ScoreRunOutSchema:
    """
    Attributes:
        score_run_uuid (str):
        score_run_status (ScoreRunStatus):
        test (TestOutSchema):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        remaining_score_runs (Union[None, Unset, int]):
    """

    score_run_uuid: str
    score_run_status: ScoreRunStatus
    test: "TestOutSchema"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    remaining_score_runs: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        score_run_uuid = self.score_run_uuid

        score_run_status = self.score_run_status.value

        test = self.test.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        remaining_score_runs: Union[None, Unset, int]
        if isinstance(self.remaining_score_runs, Unset):
            remaining_score_runs = UNSET
        else:
            remaining_score_runs = self.remaining_score_runs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score_run_uuid": score_run_uuid,
                "score_run_status": score_run_status,
                "test": test,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if remaining_score_runs is not UNSET:
            field_dict["remaining_score_runs"] = remaining_score_runs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_out_schema import TestOutSchema

        d = src_dict.copy()
        score_run_uuid = d.pop("score_run_uuid")

        score_run_status = ScoreRunStatus(d.pop("score_run_status"))

        test = TestOutSchema.from_dict(d.pop("test"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_remaining_score_runs(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        remaining_score_runs = _parse_remaining_score_runs(d.pop("remaining_score_runs", UNSET))

        score_run_out_schema = cls(
            score_run_uuid=score_run_uuid,
            score_run_status=score_run_status,
            test=test,
            created_at=created_at,
            updated_at=updated_at,
            remaining_score_runs=remaining_score_runs,
        )

        score_run_out_schema.additional_properties = d
        return score_run_out_schema

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

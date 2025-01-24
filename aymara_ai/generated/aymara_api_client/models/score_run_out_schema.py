import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.score_run_status import ScoreRunStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scoring_example_out_schema import ScoringExampleOutSchema
    from ..models.test_out_schema import TestOutSchema
    from ..models.user_out_schema import UserOutSchema


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
        price (float):
        remaining_score_runs (Union[None, Unset, int]):
        price_adjustment_note (Union[None, Unset, str]):
        created_by (Union['UserOutSchema', None, Unset]):
        score_run_examples (Union[List['ScoringExampleOutSchema'], None, Unset]):
        pass_rate (Union[None, Unset, float]):
    """

    score_run_uuid: str
    score_run_status: ScoreRunStatus
    test: "TestOutSchema"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    price: float
    remaining_score_runs: Union[None, Unset, int] = UNSET
    price_adjustment_note: Union[None, Unset, str] = UNSET
    created_by: Union["UserOutSchema", None, Unset] = UNSET
    score_run_examples: Union[List["ScoringExampleOutSchema"], None, Unset] = UNSET
    pass_rate: Union[None, Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.user_out_schema import UserOutSchema

        score_run_uuid = self.score_run_uuid

        score_run_status = self.score_run_status.value

        test = self.test.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        price = self.price

        remaining_score_runs: Union[None, Unset, int]
        if isinstance(self.remaining_score_runs, Unset):
            remaining_score_runs = UNSET
        else:
            remaining_score_runs = self.remaining_score_runs

        price_adjustment_note: Union[None, Unset, str]
        if isinstance(self.price_adjustment_note, Unset):
            price_adjustment_note = UNSET
        else:
            price_adjustment_note = self.price_adjustment_note

        created_by: Union[Dict[str, Any], None, Unset]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        elif isinstance(self.created_by, UserOutSchema):
            created_by = self.created_by.to_dict()
        else:
            created_by = self.created_by

        score_run_examples: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.score_run_examples, Unset):
            score_run_examples = UNSET
        elif isinstance(self.score_run_examples, list):
            score_run_examples = []
            for score_run_examples_type_0_item_data in self.score_run_examples:
                score_run_examples_type_0_item = score_run_examples_type_0_item_data.to_dict()
                score_run_examples.append(score_run_examples_type_0_item)

        else:
            score_run_examples = self.score_run_examples

        pass_rate: Union[None, Unset, float]
        if isinstance(self.pass_rate, Unset):
            pass_rate = UNSET
        else:
            pass_rate = self.pass_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score_run_uuid": score_run_uuid,
                "score_run_status": score_run_status,
                "test": test,
                "created_at": created_at,
                "updated_at": updated_at,
                "price": price,
            }
        )
        if remaining_score_runs is not UNSET:
            field_dict["remaining_score_runs"] = remaining_score_runs
        if price_adjustment_note is not UNSET:
            field_dict["price_adjustment_note"] = price_adjustment_note
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if score_run_examples is not UNSET:
            field_dict["score_run_examples"] = score_run_examples
        if pass_rate is not UNSET:
            field_dict["pass_rate"] = pass_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.scoring_example_out_schema import ScoringExampleOutSchema
        from ..models.test_out_schema import TestOutSchema
        from ..models.user_out_schema import UserOutSchema

        d = src_dict.copy()
        score_run_uuid = d.pop("score_run_uuid")

        score_run_status = ScoreRunStatus(d.pop("score_run_status"))

        test = TestOutSchema.from_dict(d.pop("test"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        price = d.pop("price")

        def _parse_remaining_score_runs(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        remaining_score_runs = _parse_remaining_score_runs(d.pop("remaining_score_runs", UNSET))

        def _parse_price_adjustment_note(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        price_adjustment_note = _parse_price_adjustment_note(d.pop("price_adjustment_note", UNSET))

        def _parse_created_by(data: object) -> Union["UserOutSchema", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_type_0 = UserOutSchema.from_dict(data)

                return created_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union["UserOutSchema", None, Unset], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_score_run_examples(data: object) -> Union[List["ScoringExampleOutSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                score_run_examples_type_0 = []
                _score_run_examples_type_0 = data
                for score_run_examples_type_0_item_data in _score_run_examples_type_0:
                    score_run_examples_type_0_item = ScoringExampleOutSchema.from_dict(
                        score_run_examples_type_0_item_data
                    )

                    score_run_examples_type_0.append(score_run_examples_type_0_item)

                return score_run_examples_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ScoringExampleOutSchema"], None, Unset], data)

        score_run_examples = _parse_score_run_examples(d.pop("score_run_examples", UNSET))

        def _parse_pass_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        pass_rate = _parse_pass_rate(d.pop("pass_rate", UNSET))

        score_run_out_schema = cls(
            score_run_uuid=score_run_uuid,
            score_run_status=score_run_status,
            test=test,
            created_at=created_at,
            updated_at=updated_at,
            price=price,
            remaining_score_runs=remaining_score_runs,
            price_adjustment_note=price_adjustment_note,
            created_by=created_by,
            score_run_examples=score_run_examples,
            pass_rate=pass_rate,
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

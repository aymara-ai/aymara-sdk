import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.score_run_out_schema import ScoreRunOutSchema


T = TypeVar("T", bound="BillingCycleUsageSchema")


@_attrs_define
class BillingCycleUsageSchema:
    """
    Attributes:
        billing_cycle_uuid (str):
        billing_cycle_start_date (datetime.date):
        billing_cycle_end_date (datetime.date):
        paid_amount_usd (Union[float, str]):
        score_runs (List['ScoreRunOutSchema']):
    """

    billing_cycle_uuid: str
    billing_cycle_start_date: datetime.date
    billing_cycle_end_date: datetime.date
    paid_amount_usd: Union[float, str]
    score_runs: List["ScoreRunOutSchema"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        billing_cycle_uuid = self.billing_cycle_uuid

        billing_cycle_start_date = self.billing_cycle_start_date.isoformat()

        billing_cycle_end_date = self.billing_cycle_end_date.isoformat()

        paid_amount_usd: Union[float, str]
        paid_amount_usd = self.paid_amount_usd

        score_runs = []
        for score_runs_item_data in self.score_runs:
            score_runs_item = score_runs_item_data.to_dict()
            score_runs.append(score_runs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "billing_cycle_uuid": billing_cycle_uuid,
                "billing_cycle_start_date": billing_cycle_start_date,
                "billing_cycle_end_date": billing_cycle_end_date,
                "paid_amount_usd": paid_amount_usd,
                "score_runs": score_runs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.score_run_out_schema import ScoreRunOutSchema

        d = src_dict.copy()
        billing_cycle_uuid = d.pop("billing_cycle_uuid")

        billing_cycle_start_date = isoparse(d.pop("billing_cycle_start_date")).date()

        billing_cycle_end_date = isoparse(d.pop("billing_cycle_end_date")).date()

        def _parse_paid_amount_usd(data: object) -> Union[float, str]:
            return cast(Union[float, str], data)

        paid_amount_usd = _parse_paid_amount_usd(d.pop("paid_amount_usd"))

        score_runs = []
        _score_runs = d.pop("score_runs")
        for score_runs_item_data in _score_runs:
            score_runs_item = ScoreRunOutSchema.from_dict(score_runs_item_data)

            score_runs.append(score_runs_item)

        billing_cycle_usage_schema = cls(
            billing_cycle_uuid=billing_cycle_uuid,
            billing_cycle_start_date=billing_cycle_start_date,
            billing_cycle_end_date=billing_cycle_end_date,
            paid_amount_usd=paid_amount_usd,
            score_runs=score_runs,
        )

        billing_cycle_usage_schema.additional_properties = d
        return billing_cycle_usage_schema

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

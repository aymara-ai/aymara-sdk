from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_cycle_usage_schema import BillingCycleUsageSchema
    from ..models.score_run_out_schema import ScoreRunOutSchema
    from ..models.usage_response_schema_test_type_displays import UsageResponseSchemaTestTypeDisplays


T = TypeVar("T", bound="UsageResponseSchema")


@_attrs_define
class UsageResponseSchema:
    """
    Attributes:
        test_type_displays (UsageResponseSchemaTestTypeDisplays):
        billing_cycles (Union[List['BillingCycleUsageSchema'], None, Unset]):
        free_score_runs (Union[List['ScoreRunOutSchema'], None, Unset]):
    """

    test_type_displays: "UsageResponseSchemaTestTypeDisplays"
    billing_cycles: Union[List["BillingCycleUsageSchema"], None, Unset] = UNSET
    free_score_runs: Union[List["ScoreRunOutSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_type_displays = self.test_type_displays.to_dict()

        billing_cycles: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.billing_cycles, Unset):
            billing_cycles = UNSET
        elif isinstance(self.billing_cycles, list):
            billing_cycles = []
            for billing_cycles_type_0_item_data in self.billing_cycles:
                billing_cycles_type_0_item = billing_cycles_type_0_item_data.to_dict()
                billing_cycles.append(billing_cycles_type_0_item)

        else:
            billing_cycles = self.billing_cycles

        free_score_runs: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.free_score_runs, Unset):
            free_score_runs = UNSET
        elif isinstance(self.free_score_runs, list):
            free_score_runs = []
            for free_score_runs_type_0_item_data in self.free_score_runs:
                free_score_runs_type_0_item = free_score_runs_type_0_item_data.to_dict()
                free_score_runs.append(free_score_runs_type_0_item)

        else:
            free_score_runs = self.free_score_runs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_type_displays": test_type_displays,
            }
        )
        if billing_cycles is not UNSET:
            field_dict["billing_cycles"] = billing_cycles
        if free_score_runs is not UNSET:
            field_dict["free_score_runs"] = free_score_runs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.billing_cycle_usage_schema import BillingCycleUsageSchema
        from ..models.score_run_out_schema import ScoreRunOutSchema
        from ..models.usage_response_schema_test_type_displays import UsageResponseSchemaTestTypeDisplays

        d = src_dict.copy()
        test_type_displays = UsageResponseSchemaTestTypeDisplays.from_dict(d.pop("test_type_displays"))

        def _parse_billing_cycles(data: object) -> Union[List["BillingCycleUsageSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                billing_cycles_type_0 = []
                _billing_cycles_type_0 = data
                for billing_cycles_type_0_item_data in _billing_cycles_type_0:
                    billing_cycles_type_0_item = BillingCycleUsageSchema.from_dict(billing_cycles_type_0_item_data)

                    billing_cycles_type_0.append(billing_cycles_type_0_item)

                return billing_cycles_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["BillingCycleUsageSchema"], None, Unset], data)

        billing_cycles = _parse_billing_cycles(d.pop("billing_cycles", UNSET))

        def _parse_free_score_runs(data: object) -> Union[List["ScoreRunOutSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                free_score_runs_type_0 = []
                _free_score_runs_type_0 = data
                for free_score_runs_type_0_item_data in _free_score_runs_type_0:
                    free_score_runs_type_0_item = ScoreRunOutSchema.from_dict(free_score_runs_type_0_item_data)

                    free_score_runs_type_0.append(free_score_runs_type_0_item)

                return free_score_runs_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ScoreRunOutSchema"], None, Unset], data)

        free_score_runs = _parse_free_score_runs(d.pop("free_score_runs", UNSET))

        usage_response_schema = cls(
            test_type_displays=test_type_displays,
            billing_cycles=billing_cycles,
            free_score_runs=free_score_runs,
        )

        usage_response_schema.additional_properties = d
        return usage_response_schema

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

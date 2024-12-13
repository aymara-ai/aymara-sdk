from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.example_type import ExampleType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExampleOutSchema")


@_attrs_define
class ExampleOutSchema:
    """
    Attributes:
        example_uuid (str):
        example_text (str):
        example_type (ExampleType):
        explanation (Union[None, Unset, str]):
    """

    example_uuid: str
    example_text: str
    example_type: ExampleType
    explanation: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        example_uuid = self.example_uuid

        example_text = self.example_text

        example_type = self.example_type.value

        explanation: Union[None, Unset, str]
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "example_uuid": example_uuid,
                "example_text": example_text,
                "example_type": example_type,
            }
        )
        if explanation is not UNSET:
            field_dict["explanation"] = explanation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        example_uuid = d.pop("example_uuid")

        example_text = d.pop("example_text")

        example_type = ExampleType(d.pop("example_type"))

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        example_out_schema = cls(
            example_uuid=example_uuid,
            example_text=example_text,
            example_type=example_type,
            explanation=explanation,
        )

        example_out_schema.additional_properties = d
        return example_out_schema

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

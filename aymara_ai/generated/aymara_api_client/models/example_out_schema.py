from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.example_out_schema_example_type import ExampleOutSchemaExampleType

T = TypeVar("T", bound="ExampleOutSchema")


@_attrs_define
class ExampleOutSchema:
    """
    Attributes:
        example_uuid (str):
        question_text (str):
        example_type (ExampleOutSchemaExampleType):
    """

    example_uuid: str
    question_text: str
    example_type: ExampleOutSchemaExampleType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        example_uuid = self.example_uuid

        question_text = self.question_text

        example_type = self.example_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "example_uuid": example_uuid,
                "question_text": question_text,
                "example_type": example_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        example_uuid = d.pop("example_uuid")

        question_text = d.pop("question_text")

        example_type = ExampleOutSchemaExampleType(d.pop("example_type"))

        example_out_schema = cls(
            example_uuid=example_uuid,
            question_text=question_text,
            example_type=example_type,
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

from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.example_in_schema_example_type import ExampleInSchemaExampleType

T = TypeVar("T", bound="ExampleInSchema")


@_attrs_define
class ExampleInSchema:
    """
    Attributes:
        question_text (str):
        example_type (ExampleInSchemaExampleType):
    """

    question_text: str
    example_type: ExampleInSchemaExampleType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        question_text = self.question_text

        example_type = self.example_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_text": question_text,
                "example_type": example_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        question_text = d.pop("question_text")

        example_type = ExampleInSchemaExampleType(d.pop("example_type"))

        example_in_schema = cls(
            question_text=question_text,
            example_type=example_type,
        )

        example_in_schema.additional_properties = d
        return example_in_schema

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

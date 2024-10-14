from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="QuestionSchema")


@_attrs_define
class QuestionSchema:
    """
    Attributes:
        question_uuid (str):
        question_text (str):
    """

    question_uuid: str
    question_text: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        question_uuid = self.question_uuid

        question_text = self.question_text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_uuid": question_uuid,
                "question_text": question_text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        question_uuid = d.pop("question_uuid")

        question_text = d.pop("question_text")

        question_schema = cls(
            question_uuid=question_uuid,
            question_text=question_text,
        )

        question_schema.additional_properties = d
        return question_schema

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

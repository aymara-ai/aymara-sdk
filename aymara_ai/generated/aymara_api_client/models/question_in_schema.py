from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QuestionInSchema")


@_attrs_define
class QuestionInSchema:
    """
    Attributes:
        question_text (str):
        accuracy_question_type (Union[None, Unset, str]):
    """

    question_text: str
    accuracy_question_type: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        question_text = self.question_text

        accuracy_question_type: Union[None, Unset, str]
        if isinstance(self.accuracy_question_type, Unset):
            accuracy_question_type = UNSET
        else:
            accuracy_question_type = self.accuracy_question_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_text": question_text,
            }
        )
        if accuracy_question_type is not UNSET:
            field_dict["accuracy_question_type"] = accuracy_question_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        question_text = d.pop("question_text")

        def _parse_accuracy_question_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        accuracy_question_type = _parse_accuracy_question_type(d.pop("accuracy_question_type", UNSET))

        question_in_schema = cls(
            question_text=question_text,
            accuracy_question_type=accuracy_question_type,
        )

        question_in_schema.additional_properties = d
        return question_in_schema

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

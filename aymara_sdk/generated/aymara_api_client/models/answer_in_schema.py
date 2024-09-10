from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AnswerInSchema")


@_attrs_define
class AnswerInSchema:
    """
    Attributes:
        question_uuid (str):
        answer_text (Union[None, Unset, str]):
    """

    question_uuid: str
    answer_text: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        question_uuid = self.question_uuid

        answer_text: Union[None, Unset, str]
        if isinstance(self.answer_text, Unset):
            answer_text = UNSET
        else:
            answer_text = self.answer_text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_uuid": question_uuid,
            }
        )
        if answer_text is not UNSET:
            field_dict["answer_text"] = answer_text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        question_uuid = d.pop("question_uuid")

        def _parse_answer_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        answer_text = _parse_answer_text(d.pop("answer_text", UNSET))

        answer_in_schema = cls(
            question_uuid=question_uuid,
            answer_text=answer_text,
        )

        answer_in_schema.additional_properties = d
        return answer_in_schema

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

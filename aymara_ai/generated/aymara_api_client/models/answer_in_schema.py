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
        answer_image_path (Union[None, Unset, str]):
        student_refused (Union[Unset, bool]):  Default: False.
        exclude_from_scoring (Union[Unset, bool]):  Default: False.
    """

    question_uuid: str
    answer_text: Union[None, Unset, str] = UNSET
    answer_image_path: Union[None, Unset, str] = UNSET
    student_refused: Union[Unset, bool] = False
    exclude_from_scoring: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        question_uuid = self.question_uuid

        answer_text: Union[None, Unset, str]
        if isinstance(self.answer_text, Unset):
            answer_text = UNSET
        else:
            answer_text = self.answer_text

        answer_image_path: Union[None, Unset, str]
        if isinstance(self.answer_image_path, Unset):
            answer_image_path = UNSET
        else:
            answer_image_path = self.answer_image_path

        student_refused = self.student_refused

        exclude_from_scoring = self.exclude_from_scoring

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_uuid": question_uuid,
            }
        )
        if answer_text is not UNSET:
            field_dict["answer_text"] = answer_text
        if answer_image_path is not UNSET:
            field_dict["answer_image_path"] = answer_image_path
        if student_refused is not UNSET:
            field_dict["student_refused"] = student_refused
        if exclude_from_scoring is not UNSET:
            field_dict["exclude_from_scoring"] = exclude_from_scoring

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

        def _parse_answer_image_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        answer_image_path = _parse_answer_image_path(d.pop("answer_image_path", UNSET))

        student_refused = d.pop("student_refused", UNSET)

        exclude_from_scoring = d.pop("exclude_from_scoring", UNSET)

        answer_in_schema = cls(
            question_uuid=question_uuid,
            answer_text=answer_text,
            answer_image_path=answer_image_path,
            student_refused=student_refused,
            exclude_from_scoring=exclude_from_scoring,
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

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.answer_in_schema import AnswerInSchema


T = TypeVar("T", bound="ImageUploadRequestInSchema")


@_attrs_define
class ImageUploadRequestInSchema:
    """
    Attributes:
        test_uuid (str):
        answers (List['AnswerInSchema']):
    """

    test_uuid: str
    answers: List["AnswerInSchema"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_uuid = self.test_uuid

        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()
            answers.append(answers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_uuid": test_uuid,
                "answers": answers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.answer_in_schema import AnswerInSchema

        d = src_dict.copy()
        test_uuid = d.pop("test_uuid")

        answers = []
        _answers = d.pop("answers")
        for answers_item_data in _answers:
            answers_item = AnswerInSchema.from_dict(answers_item_data)

            answers.append(answers_item)

        image_upload_request_in_schema = cls(
            test_uuid=test_uuid,
            answers=answers,
        )

        image_upload_request_in_schema.additional_properties = d
        return image_upload_request_in_schema

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

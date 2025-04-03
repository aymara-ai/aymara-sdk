from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.answer_in_schema import AnswerInSchema


T = TypeVar("T", bound="MultiturnContinueInSchema")


@_attrs_define
class MultiturnContinueInSchema:
    """Schema for continuing a specific conversation in a multiturn test.

    Attributes:
        test_uuid (str):
        answers (Union[List['AnswerInSchema'], None, Unset]):
    """

    test_uuid: str
    answers: Union[List["AnswerInSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_uuid = self.test_uuid

        answers: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.answers, Unset):
            answers = UNSET
        elif isinstance(self.answers, list):
            answers = []
            for answers_type_0_item_data in self.answers:
                answers_type_0_item = answers_type_0_item_data.to_dict()
                answers.append(answers_type_0_item)

        else:
            answers = self.answers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_uuid": test_uuid,
            }
        )
        if answers is not UNSET:
            field_dict["answers"] = answers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.answer_in_schema import AnswerInSchema

        d = src_dict.copy()
        test_uuid = d.pop("test_uuid")

        def _parse_answers(data: object) -> Union[List["AnswerInSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                answers_type_0 = []
                _answers_type_0 = data
                for answers_type_0_item_data in _answers_type_0:
                    answers_type_0_item = AnswerInSchema.from_dict(answers_type_0_item_data)

                    answers_type_0.append(answers_type_0_item)

                return answers_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["AnswerInSchema"], None, Unset], data)

        answers = _parse_answers(d.pop("answers", UNSET))

        multiturn_continue_in_schema = cls(
            test_uuid=test_uuid,
            answers=answers,
        )

        multiturn_continue_in_schema.additional_properties = d
        return multiturn_continue_in_schema

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

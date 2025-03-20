from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.eval_question_schema import EvalQuestionSchema


T = TypeVar("T", bound="EvalQuestionListSchema")


@_attrs_define
class EvalQuestionListSchema:
    """Schema for a list of  eval questions with metadata.

    Attributes:
        questions (List['EvalQuestionSchema']):
        count (int):
        categories (List[str]):
    """

    questions: List["EvalQuestionSchema"]
    count: int
    categories: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        questions = []
        for questions_item_data in self.questions:
            questions_item = questions_item_data.to_dict()
            questions.append(questions_item)

        count = self.count

        categories = self.categories

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "questions": questions,
                "count": count,
                "categories": categories,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_question_schema import EvalQuestionSchema

        d = src_dict.copy()
        questions = []
        _questions = d.pop("questions")
        for questions_item_data in _questions:
            questions_item = EvalQuestionSchema.from_dict(questions_item_data)

            questions.append(questions_item)

        count = d.pop("count")

        categories = cast(List[str], d.pop("categories"))

        eval_question_list_schema = cls(
            questions=questions,
            count=count,
            categories=categories,
        )

        eval_question_list_schema.additional_properties = d
        return eval_question_list_schema

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

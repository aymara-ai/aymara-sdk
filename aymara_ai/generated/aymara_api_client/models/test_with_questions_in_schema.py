from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.question_in_schema import QuestionInSchema
    from ..models.test_in_schema import TestInSchema


T = TypeVar("T", bound="TestWithQuestionsInSchema")


@_attrs_define
class TestWithQuestionsInSchema:
    """
    Attributes:
        test (TestInSchema):
        questions (Union[List['QuestionInSchema'], None, Unset]):
    """

    test: "TestInSchema"
    questions: Union[List["QuestionInSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test = self.test.to_dict()

        questions: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.questions, Unset):
            questions = UNSET
        elif isinstance(self.questions, list):
            questions = []
            for questions_type_0_item_data in self.questions:
                questions_type_0_item = questions_type_0_item_data.to_dict()
                questions.append(questions_type_0_item)

        else:
            questions = self.questions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test": test,
            }
        )
        if questions is not UNSET:
            field_dict["questions"] = questions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.question_in_schema import QuestionInSchema
        from ..models.test_in_schema import TestInSchema

        d = src_dict.copy()
        test = TestInSchema.from_dict(d.pop("test"))

        def _parse_questions(data: object) -> Union[List["QuestionInSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                questions_type_0 = []
                _questions_type_0 = data
                for questions_type_0_item_data in _questions_type_0:
                    questions_type_0_item = QuestionInSchema.from_dict(questions_type_0_item_data)

                    questions_type_0.append(questions_type_0_item)

                return questions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["QuestionInSchema"], None, Unset], data)

        questions = _parse_questions(d.pop("questions", UNSET))

        test_with_questions_in_schema = cls(
            test=test,
            questions=questions,
        )

        test_with_questions_in_schema.additional_properties = d
        return test_with_questions_in_schema

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

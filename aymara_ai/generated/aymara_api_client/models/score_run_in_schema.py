from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.answer_in_schema import AnswerInSchema
    from ..models.scoring_example_in_schema import ScoringExampleInSchema


T = TypeVar("T", bound="ScoreRunInSchema")


@_attrs_define
class ScoreRunInSchema:
    """
    Attributes:
        test_uuid (str):
        answers (List['AnswerInSchema']):
        examples (Union[List['ScoringExampleInSchema'], None, Unset]):
    """

    test_uuid: str
    answers: List["AnswerInSchema"]
    examples: Union[List["ScoringExampleInSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_uuid = self.test_uuid

        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()
            answers.append(answers_item)

        examples: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.examples, Unset):
            examples = UNSET
        elif isinstance(self.examples, list):
            examples = []
            for examples_type_0_item_data in self.examples:
                examples_type_0_item = examples_type_0_item_data.to_dict()
                examples.append(examples_type_0_item)

        else:
            examples = self.examples

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_uuid": test_uuid,
                "answers": answers,
            }
        )
        if examples is not UNSET:
            field_dict["examples"] = examples

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.answer_in_schema import AnswerInSchema
        from ..models.scoring_example_in_schema import ScoringExampleInSchema

        d = src_dict.copy()
        test_uuid = d.pop("test_uuid")

        answers = []
        _answers = d.pop("answers")
        for answers_item_data in _answers:
            answers_item = AnswerInSchema.from_dict(answers_item_data)

            answers.append(answers_item)

        def _parse_examples(data: object) -> Union[List["ScoringExampleInSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                examples_type_0 = []
                _examples_type_0 = data
                for examples_type_0_item_data in _examples_type_0:
                    examples_type_0_item = ScoringExampleInSchema.from_dict(examples_type_0_item_data)

                    examples_type_0.append(examples_type_0_item)

                return examples_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ScoringExampleInSchema"], None, Unset], data)

        examples = _parse_examples(d.pop("examples", UNSET))

        score_run_in_schema = cls(
            test_uuid=test_uuid,
            answers=answers,
            examples=examples,
        )

        score_run_in_schema.additional_properties = d
        return score_run_in_schema

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

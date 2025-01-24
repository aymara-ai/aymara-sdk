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
        score_run_examples (Union[List['ScoringExampleInSchema'], None, Unset]):
    """

    test_uuid: str
    answers: List["AnswerInSchema"]
    score_run_examples: Union[List["ScoringExampleInSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_uuid = self.test_uuid

        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()
            answers.append(answers_item)

        score_run_examples: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.score_run_examples, Unset):
            score_run_examples = UNSET
        elif isinstance(self.score_run_examples, list):
            score_run_examples = []
            for score_run_examples_type_0_item_data in self.score_run_examples:
                score_run_examples_type_0_item = score_run_examples_type_0_item_data.to_dict()
                score_run_examples.append(score_run_examples_type_0_item)

        else:
            score_run_examples = self.score_run_examples

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_uuid": test_uuid,
                "answers": answers,
            }
        )
        if score_run_examples is not UNSET:
            field_dict["score_run_examples"] = score_run_examples

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

        def _parse_score_run_examples(data: object) -> Union[List["ScoringExampleInSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                score_run_examples_type_0 = []
                _score_run_examples_type_0 = data
                for score_run_examples_type_0_item_data in _score_run_examples_type_0:
                    score_run_examples_type_0_item = ScoringExampleInSchema.from_dict(
                        score_run_examples_type_0_item_data
                    )

                    score_run_examples_type_0.append(score_run_examples_type_0_item)

                return score_run_examples_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ScoringExampleInSchema"], None, Unset], data)

        score_run_examples = _parse_score_run_examples(d.pop("score_run_examples", UNSET))

        score_run_in_schema = cls(
            test_uuid=test_uuid,
            answers=answers,
            score_run_examples=score_run_examples,
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

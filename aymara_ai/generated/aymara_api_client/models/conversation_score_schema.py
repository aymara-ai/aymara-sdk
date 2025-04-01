from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.answer_out_schema import AnswerOutSchema
    from ..models.question_schema import QuestionSchema


T = TypeVar("T", bound="ConversationScoreSchema")


@_attrs_define
class ConversationScoreSchema:
    """
    Attributes:
        conversation_uuid (str):
        scores (List['AnswerOutSchema']):
        current_turn (int):
        prompt (Union['QuestionSchema', None, Unset]):
    """

    conversation_uuid: str
    scores: List["AnswerOutSchema"]
    current_turn: int
    prompt: Union["QuestionSchema", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.question_schema import QuestionSchema

        conversation_uuid = self.conversation_uuid

        scores = []
        for scores_item_data in self.scores:
            scores_item = scores_item_data.to_dict()
            scores.append(scores_item)

        current_turn = self.current_turn

        prompt: Union[Dict[str, Any], None, Unset]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        elif isinstance(self.prompt, QuestionSchema):
            prompt = self.prompt.to_dict()
        else:
            prompt = self.prompt

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversation_uuid": conversation_uuid,
                "scores": scores,
                "current_turn": current_turn,
            }
        )
        if prompt is not UNSET:
            field_dict["prompt"] = prompt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.answer_out_schema import AnswerOutSchema
        from ..models.question_schema import QuestionSchema

        d = src_dict.copy()
        conversation_uuid = d.pop("conversation_uuid")

        scores = []
        _scores = d.pop("scores")
        for scores_item_data in _scores:
            scores_item = AnswerOutSchema.from_dict(scores_item_data)

            scores.append(scores_item)

        current_turn = d.pop("current_turn")

        def _parse_prompt(data: object) -> Union["QuestionSchema", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_type_0 = QuestionSchema.from_dict(data)

                return prompt_type_0
            except:  # noqa: E722
                pass
            return cast(Union["QuestionSchema", None, Unset], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        conversation_score_schema = cls(
            conversation_uuid=conversation_uuid,
            scores=scores,
            current_turn=current_turn,
            prompt=prompt,
        )

        conversation_score_schema.additional_properties = d
        return conversation_score_schema

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

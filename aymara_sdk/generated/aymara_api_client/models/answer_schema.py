from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.question_schema import QuestionSchema


T = TypeVar("T", bound="AnswerSchema")


@_attrs_define
class AnswerSchema:
    """
    Attributes:
        answer_uuid (str):
        answer_text (str):
        question (QuestionSchema):
        is_safe (Union[None, Unset, bool]):
        is_follow (Union[None, Unset, bool]):
        instruction_unfollowed (Union[None, Unset, str]):
        explanation (Union[None, Unset, str]):
        confidence (Union[None, Unset, float]):
    """

    answer_uuid: str
    answer_text: str
    question: "QuestionSchema"
    is_safe: Union[None, Unset, bool] = UNSET
    is_follow: Union[None, Unset, bool] = UNSET
    instruction_unfollowed: Union[None, Unset, str] = UNSET
    explanation: Union[None, Unset, str] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        answer_uuid = self.answer_uuid

        answer_text = self.answer_text

        question = self.question.to_dict()

        is_safe: Union[None, Unset, bool]
        if isinstance(self.is_safe, Unset):
            is_safe = UNSET
        else:
            is_safe = self.is_safe

        is_follow: Union[None, Unset, bool]
        if isinstance(self.is_follow, Unset):
            is_follow = UNSET
        else:
            is_follow = self.is_follow

        instruction_unfollowed: Union[None, Unset, str]
        if isinstance(self.instruction_unfollowed, Unset):
            instruction_unfollowed = UNSET
        else:
            instruction_unfollowed = self.instruction_unfollowed

        explanation: Union[None, Unset, str]
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answer_uuid": answer_uuid,
                "answer_text": answer_text,
                "question": question,
            }
        )
        if is_safe is not UNSET:
            field_dict["is_safe"] = is_safe
        if is_follow is not UNSET:
            field_dict["is_follow"] = is_follow
        if instruction_unfollowed is not UNSET:
            field_dict["instruction_unfollowed"] = instruction_unfollowed
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if confidence is not UNSET:
            field_dict["confidence"] = confidence

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.question_schema import QuestionSchema

        d = src_dict.copy()
        answer_uuid = d.pop("answer_uuid")

        answer_text = d.pop("answer_text")

        question = QuestionSchema.from_dict(d.pop("question"))

        def _parse_is_safe(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_safe = _parse_is_safe(d.pop("is_safe", UNSET))

        def _parse_is_follow(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_follow = _parse_is_follow(d.pop("is_follow", UNSET))

        def _parse_instruction_unfollowed(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instruction_unfollowed = _parse_instruction_unfollowed(d.pop("instruction_unfollowed", UNSET))

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        answer_schema = cls(
            answer_uuid=answer_uuid,
            answer_text=answer_text,
            question=question,
            is_safe=is_safe,
            is_follow=is_follow,
            instruction_unfollowed=instruction_unfollowed,
            explanation=explanation,
            confidence=confidence,
        )

        answer_schema.additional_properties = d
        return answer_schema

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

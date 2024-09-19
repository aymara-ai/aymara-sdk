from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.question_schema import QuestionSchema


T = TypeVar("T", bound="AnswerOutSchema")


@_attrs_define
class AnswerOutSchema:
    """
    Attributes:
        answer_uuid (str):
        question (QuestionSchema):
        answer_text (Union[None, Unset, str]):
        explanation (Union[None, Unset, str]):
        confidence (Union[None, Unset, float]):
        is_passed (Union[None, Unset, bool]):
    """

    answer_uuid: str
    question: "QuestionSchema"
    answer_text: Union[None, Unset, str] = UNSET
    explanation: Union[None, Unset, str] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    is_passed: Union[None, Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        answer_uuid = self.answer_uuid

        question = self.question.to_dict()

        answer_text: Union[None, Unset, str]
        if isinstance(self.answer_text, Unset):
            answer_text = UNSET
        else:
            answer_text = self.answer_text

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

        is_passed: Union[None, Unset, bool]
        if isinstance(self.is_passed, Unset):
            is_passed = UNSET
        else:
            is_passed = self.is_passed

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answer_uuid": answer_uuid,
                "question": question,
            }
        )
        if answer_text is not UNSET:
            field_dict["answer_text"] = answer_text
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if is_passed is not UNSET:
            field_dict["is_passed"] = is_passed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.question_schema import QuestionSchema

        d = src_dict.copy()
        answer_uuid = d.pop("answer_uuid")

        question = QuestionSchema.from_dict(d.pop("question"))

        def _parse_answer_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        answer_text = _parse_answer_text(d.pop("answer_text", UNSET))

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

        def _parse_is_passed(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_passed = _parse_is_passed(d.pop("is_passed", UNSET))

        answer_out_schema = cls(
            answer_uuid=answer_uuid,
            question=question,
            answer_text=answer_text,
            explanation=explanation,
            confidence=confidence,
            is_passed=is_passed,
        )

        answer_out_schema.additional_properties = d
        return answer_out_schema

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

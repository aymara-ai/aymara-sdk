from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_type import ContentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_prompt_schema import EvalPromptSchema


T = TypeVar("T", bound="EvalResponseOutSchema")


@_attrs_define
class EvalResponseOutSchema:
    """Schema for returning AI response data.

    Attributes:
        prompt_uuid (str):
        content (str):
        response_uuid (str):
        prompt (EvalPromptSchema):
        content_type (Union[Unset, ContentType]): Content type for AI interactions. Default: ContentType.TEXT.
        thread_uuid (Union[None, Unset, str]):
        turn_number (Union[Unset, int]):  Default: 1.
        exclude_from_scoring (Union[Unset, bool]):  Default: False.
        ai_refused (Union[Unset, bool]):  Default: False.
        generate_prompt (Union[Unset, bool]):  Default: False.
        explanation (Union[None, Unset, str]):
        confidence (Union[None, Unset, float]):
        is_passed (Union[None, Unset, bool]):
        next_prompt (Union['EvalPromptSchema', None, Unset]):
    """

    prompt_uuid: str
    content: str
    response_uuid: str
    prompt: "EvalPromptSchema"
    content_type: Union[Unset, ContentType] = ContentType.TEXT
    thread_uuid: Union[None, Unset, str] = UNSET
    turn_number: Union[Unset, int] = 1
    exclude_from_scoring: Union[Unset, bool] = False
    ai_refused: Union[Unset, bool] = False
    generate_prompt: Union[Unset, bool] = False
    explanation: Union[None, Unset, str] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    is_passed: Union[None, Unset, bool] = UNSET
    next_prompt: Union["EvalPromptSchema", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.eval_prompt_schema import EvalPromptSchema

        prompt_uuid = self.prompt_uuid

        content = self.content

        response_uuid = self.response_uuid

        prompt = self.prompt.to_dict()

        content_type: Union[Unset, str] = UNSET
        if not isinstance(self.content_type, Unset):
            content_type = self.content_type.value

        thread_uuid: Union[None, Unset, str]
        if isinstance(self.thread_uuid, Unset):
            thread_uuid = UNSET
        else:
            thread_uuid = self.thread_uuid

        turn_number = self.turn_number

        exclude_from_scoring = self.exclude_from_scoring

        ai_refused = self.ai_refused

        generate_prompt = self.generate_prompt

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

        next_prompt: Union[Dict[str, Any], None, Unset]
        if isinstance(self.next_prompt, Unset):
            next_prompt = UNSET
        elif isinstance(self.next_prompt, EvalPromptSchema):
            next_prompt = self.next_prompt.to_dict()
        else:
            next_prompt = self.next_prompt

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt_uuid": prompt_uuid,
                "content": content,
                "response_uuid": response_uuid,
                "prompt": prompt,
            }
        )
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if thread_uuid is not UNSET:
            field_dict["thread_uuid"] = thread_uuid
        if turn_number is not UNSET:
            field_dict["turn_number"] = turn_number
        if exclude_from_scoring is not UNSET:
            field_dict["exclude_from_scoring"] = exclude_from_scoring
        if ai_refused is not UNSET:
            field_dict["ai_refused"] = ai_refused
        if generate_prompt is not UNSET:
            field_dict["generate_prompt"] = generate_prompt
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if is_passed is not UNSET:
            field_dict["is_passed"] = is_passed
        if next_prompt is not UNSET:
            field_dict["next_prompt"] = next_prompt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_prompt_schema import EvalPromptSchema

        d = src_dict.copy()
        prompt_uuid = d.pop("prompt_uuid")

        content = d.pop("content")

        response_uuid = d.pop("response_uuid")

        prompt = EvalPromptSchema.from_dict(d.pop("prompt"))

        _content_type = d.pop("content_type", UNSET)
        content_type: Union[Unset, ContentType]
        if isinstance(_content_type, Unset):
            content_type = UNSET
        else:
            content_type = ContentType(_content_type)

        def _parse_thread_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thread_uuid = _parse_thread_uuid(d.pop("thread_uuid", UNSET))

        turn_number = d.pop("turn_number", UNSET)

        exclude_from_scoring = d.pop("exclude_from_scoring", UNSET)

        ai_refused = d.pop("ai_refused", UNSET)

        generate_prompt = d.pop("generate_prompt", UNSET)

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

        def _parse_next_prompt(data: object) -> Union["EvalPromptSchema", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                next_prompt_type_0 = EvalPromptSchema.from_dict(data)

                return next_prompt_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EvalPromptSchema", None, Unset], data)

        next_prompt = _parse_next_prompt(d.pop("next_prompt", UNSET))

        eval_response_out_schema = cls(
            prompt_uuid=prompt_uuid,
            content=content,
            response_uuid=response_uuid,
            prompt=prompt,
            content_type=content_type,
            thread_uuid=thread_uuid,
            turn_number=turn_number,
            exclude_from_scoring=exclude_from_scoring,
            ai_refused=ai_refused,
            generate_prompt=generate_prompt,
            explanation=explanation,
            confidence=confidence,
            is_passed=is_passed,
            next_prompt=next_prompt,
        )

        eval_response_out_schema.additional_properties = d
        return eval_response_out_schema

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

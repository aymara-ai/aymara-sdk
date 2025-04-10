from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_type import ContentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EvalResponseInSchema")


@_attrs_define
class EvalResponseInSchema:
    """Schema for submitting AI responses to eval prompts.

    Attributes:
        prompt_uuid (str):
        content (str):
        content_type (Union[Unset, ContentType]): Content type for AI interactions. Default: ContentType.TEXT.
        thread_uuid (Union[None, Unset, str]):
        turn_number (Union[Unset, int]):  Default: 1.
        exclude_from_scoring (Union[Unset, bool]):  Default: False.
        ai_refused (Union[Unset, bool]):  Default: False.
        generate_prompt (Union[Unset, bool]):  Default: False.
    """

    prompt_uuid: str
    content: str
    content_type: Union[Unset, ContentType] = ContentType.TEXT
    thread_uuid: Union[None, Unset, str] = UNSET
    turn_number: Union[Unset, int] = 1
    exclude_from_scoring: Union[Unset, bool] = False
    ai_refused: Union[Unset, bool] = False
    generate_prompt: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt_uuid = self.prompt_uuid

        content = self.content

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt_uuid": prompt_uuid,
                "content": content,
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt_uuid = d.pop("prompt_uuid")

        content = d.pop("content")

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

        eval_response_in_schema = cls(
            prompt_uuid=prompt_uuid,
            content=content,
            content_type=content_type,
            thread_uuid=thread_uuid,
            turn_number=turn_number,
            exclude_from_scoring=exclude_from_scoring,
            ai_refused=ai_refused,
            generate_prompt=generate_prompt,
        )

        eval_response_in_schema.additional_properties = d
        return eval_response_in_schema

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

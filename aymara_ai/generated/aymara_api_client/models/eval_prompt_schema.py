from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvalPromptSchema")


@_attrs_define
class EvalPromptSchema:
    """
    Attributes:
        prompt_uuid (str):
        content (str):
        thread_uuid (Union[None, Unset, str]):
        turn_number (Union[Unset, int]):  Default: 1.
        category (Union[None, Unset, str]):
    """

    prompt_uuid: str
    content: str
    thread_uuid: Union[None, Unset, str] = UNSET
    turn_number: Union[Unset, int] = 1
    category: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt_uuid = self.prompt_uuid

        content = self.content

        thread_uuid: Union[None, Unset, str]
        if isinstance(self.thread_uuid, Unset):
            thread_uuid = UNSET
        else:
            thread_uuid = self.thread_uuid

        turn_number = self.turn_number

        category: Union[None, Unset, str]
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt_uuid": prompt_uuid,
                "content": content,
            }
        )
        if thread_uuid is not UNSET:
            field_dict["thread_uuid"] = thread_uuid
        if turn_number is not UNSET:
            field_dict["turn_number"] = turn_number
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt_uuid = d.pop("prompt_uuid")

        content = d.pop("content")

        def _parse_thread_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thread_uuid = _parse_thread_uuid(d.pop("thread_uuid", UNSET))

        turn_number = d.pop("turn_number", UNSET)

        def _parse_category(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        category = _parse_category(d.pop("category", UNSET))

        eval_prompt_schema = cls(
            prompt_uuid=prompt_uuid,
            content=content,
            thread_uuid=thread_uuid,
            turn_number=turn_number,
            category=category,
        )

        eval_prompt_schema.additional_properties = d
        return eval_prompt_schema

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

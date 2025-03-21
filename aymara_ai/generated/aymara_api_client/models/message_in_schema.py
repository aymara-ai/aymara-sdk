from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MessageInSchema")


@_attrs_define
class MessageInSchema:
    """
    Attributes:
        conversation_uuid (str):
        message_text (str):
    """

    conversation_uuid: str
    message_text: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        conversation_uuid = self.conversation_uuid

        message_text = self.message_text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversation_uuid": conversation_uuid,
                "message_text": message_text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        conversation_uuid = d.pop("conversation_uuid")

        message_text = d.pop("message_text")

        message_in_schema = cls(
            conversation_uuid=conversation_uuid,
            message_text=message_text,
        )

        message_in_schema.additional_properties = d
        return message_in_schema

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

import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.message_sender import MessageSender

T = TypeVar("T", bound="MessageSchema")


@_attrs_define
class MessageSchema:
    """
    Attributes:
        message_uuid (str):
        message_text (str):
        message_sender (MessageSender): Message sender types.
        num_turn (int):
        timestamp (datetime.datetime):
    """

    message_uuid: str
    message_text: str
    message_sender: MessageSender
    num_turn: int
    timestamp: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message_uuid = self.message_uuid

        message_text = self.message_text

        message_sender = self.message_sender.value

        num_turn = self.num_turn

        timestamp = self.timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message_uuid": message_uuid,
                "message_text": message_text,
                "message_sender": message_sender,
                "num_turn": num_turn,
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message_uuid = d.pop("message_uuid")

        message_text = d.pop("message_text")

        message_sender = MessageSender(d.pop("message_sender"))

        num_turn = d.pop("num_turn")

        timestamp = isoparse(d.pop("timestamp"))

        message_schema = cls(
            message_uuid=message_uuid,
            message_text=message_text,
            message_sender=message_sender,
            num_turn=num_turn,
            timestamp=timestamp,
        )

        message_schema.additional_properties = d
        return message_schema

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

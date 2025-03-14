from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.conversation_status import ConversationStatus

if TYPE_CHECKING:
    from ..models.message_schema import MessageSchema


T = TypeVar("T", bound="ConversationSchema")


@_attrs_define
class ConversationSchema:
    """
    Attributes:
        conversation_uuid (str):
        status (ConversationStatus): Conversation status.
        current_turn (int):
        max_turns (int):
        messages (List['MessageSchema']):
    """

    conversation_uuid: str
    status: ConversationStatus
    current_turn: int
    max_turns: int
    messages: List["MessageSchema"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        conversation_uuid = self.conversation_uuid

        status = self.status.value

        current_turn = self.current_turn

        max_turns = self.max_turns

        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversation_uuid": conversation_uuid,
                "status": status,
                "current_turn": current_turn,
                "max_turns": max_turns,
                "messages": messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_schema import MessageSchema

        d = src_dict.copy()
        conversation_uuid = d.pop("conversation_uuid")

        status = ConversationStatus(d.pop("status"))

        current_turn = d.pop("current_turn")

        max_turns = d.pop("max_turns")

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = MessageSchema.from_dict(messages_item_data)

            messages.append(messages_item)

        conversation_schema = cls(
            conversation_uuid=conversation_uuid,
            status=status,
            current_turn=current_turn,
            max_turns=max_turns,
            messages=messages,
        )

        conversation_schema.additional_properties = d
        return conversation_schema

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

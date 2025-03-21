from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.message_in_schema import MessageInSchema


T = TypeVar("T", bound="MultiturnContinueInSchema")


@_attrs_define
class MultiturnContinueInSchema:
    """Schema for continuing a specific conversation in a multiturn test.

    Attributes:
        test_uuid (str):
        messages (List['MessageInSchema']):
    """

    test_uuid: str
    messages: List["MessageInSchema"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_uuid = self.test_uuid

        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_uuid": test_uuid,
                "messages": messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_in_schema import MessageInSchema

        d = src_dict.copy()
        test_uuid = d.pop("test_uuid")

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = MessageInSchema.from_dict(messages_item_data)

            messages.append(messages_item)

        multiturn_continue_in_schema = cls(
            test_uuid=test_uuid,
            messages=messages,
        )

        multiturn_continue_in_schema.additional_properties = d
        return multiturn_continue_in_schema

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

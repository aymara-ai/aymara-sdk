from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MultiturnUserResponseSchema")


@_attrs_define
class MultiturnUserResponseSchema:
    """
    Attributes:
        test_uuid (str):
        conversation_uuid (str):
        message_text (str):
    """

    test_uuid: str
    conversation_uuid: str
    message_text: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_uuid = self.test_uuid

        conversation_uuid = self.conversation_uuid

        message_text = self.message_text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_uuid": test_uuid,
                "conversation_uuid": conversation_uuid,
                "message_text": message_text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        test_uuid = d.pop("test_uuid")

        conversation_uuid = d.pop("conversation_uuid")

        message_text = d.pop("message_text")

        multiturn_user_response_schema = cls(
            test_uuid=test_uuid,
            conversation_uuid=conversation_uuid,
            message_text=message_text,
        )

        multiturn_user_response_schema.additional_properties = d
        return multiturn_user_response_schema

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

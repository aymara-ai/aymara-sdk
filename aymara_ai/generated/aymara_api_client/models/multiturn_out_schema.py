from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_score_schema import ConversationScoreSchema


T = TypeVar("T", bound="MultiturnOutSchema")


@_attrs_define
class MultiturnOutSchema:
    """Schema for continuing a specific conversation in a multiturn test.

    Attributes:
        conversations (List['ConversationScoreSchema']):
        test_uuid (str):
        score_run_uuid (Union[None, Unset, str]):
    """

    conversations: List["ConversationScoreSchema"]
    test_uuid: str
    score_run_uuid: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        conversations = []
        for conversations_item_data in self.conversations:
            conversations_item = conversations_item_data.to_dict()
            conversations.append(conversations_item)

        test_uuid = self.test_uuid

        score_run_uuid: Union[None, Unset, str]
        if isinstance(self.score_run_uuid, Unset):
            score_run_uuid = UNSET
        else:
            score_run_uuid = self.score_run_uuid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversations": conversations,
                "test_uuid": test_uuid,
            }
        )
        if score_run_uuid is not UNSET:
            field_dict["score_run_uuid"] = score_run_uuid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversation_score_schema import ConversationScoreSchema

        d = src_dict.copy()
        conversations = []
        _conversations = d.pop("conversations")
        for conversations_item_data in _conversations:
            conversations_item = ConversationScoreSchema.from_dict(conversations_item_data)

            conversations.append(conversations_item)

        test_uuid = d.pop("test_uuid")

        def _parse_score_run_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        score_run_uuid = _parse_score_run_uuid(d.pop("score_run_uuid", UNSET))

        multiturn_out_schema = cls(
            conversations=conversations,
            test_uuid=test_uuid,
            score_run_uuid=score_run_uuid,
        )

        multiturn_out_schema.additional_properties = d
        return multiturn_out_schema

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

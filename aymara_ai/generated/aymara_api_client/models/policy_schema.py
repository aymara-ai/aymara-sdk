from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PolicySchema")


@_attrs_define
class PolicySchema:
    """
    Attributes:
        test_type (str):
        test_language (str):
        aymara_policy_name (str):
        display_name (str):
        policy_text (str):
    """

    test_type: str
    test_language: str
    aymara_policy_name: str
    display_name: str
    policy_text: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_type = self.test_type

        test_language = self.test_language

        aymara_policy_name = self.aymara_policy_name

        display_name = self.display_name

        policy_text = self.policy_text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_type": test_type,
                "test_language": test_language,
                "aymara_policy_name": aymara_policy_name,
                "display_name": display_name,
                "policy_text": policy_text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        test_type = d.pop("test_type")

        test_language = d.pop("test_language")

        aymara_policy_name = d.pop("aymara_policy_name")

        display_name = d.pop("display_name")

        policy_text = d.pop("policy_text")

        policy_schema = cls(
            test_type=test_type,
            test_language=test_language,
            aymara_policy_name=aymara_policy_name,
            display_name=display_name,
            policy_text=policy_text,
        )

        policy_schema.additional_properties = d
        return policy_schema

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

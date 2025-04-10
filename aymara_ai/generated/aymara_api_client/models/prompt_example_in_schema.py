from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.example_type import ExampleType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptExampleInSchema")


@_attrs_define
class PromptExampleInSchema:
    """
    Attributes:
        content (str):
        type (Union[Unset, ExampleType]):  Default: ExampleType.GOOD.
        explanation (Union[None, Unset, str]):
    """

    content: str
    type: Union[Unset, ExampleType] = ExampleType.GOOD
    explanation: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        explanation: Union[None, Unset, str]
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if explanation is not UNSET:
            field_dict["explanation"] = explanation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content")

        _type = d.pop("type", UNSET)
        type: Union[Unset, ExampleType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ExampleType(_type)

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        prompt_example_in_schema = cls(
            content=content,
            type=type,
            explanation=explanation,
        )

        prompt_example_in_schema.additional_properties = d
        return prompt_example_in_schema

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

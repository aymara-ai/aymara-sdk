from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvalTypeSchema")


@_attrs_define
class EvalTypeSchema:
    """Schema for eval eval_types.

    Attributes:
        eval_type_uuid (str):
        name (str):
        slug (str):
        description (str):
        supported_modalities (Union[Unset, List[str]]):
    """

    eval_type_uuid: str
    name: str
    slug: str
    description: str
    supported_modalities: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        eval_type_uuid = self.eval_type_uuid

        name = self.name

        slug = self.slug

        description = self.description

        supported_modalities: Union[Unset, List[str]] = UNSET
        if not isinstance(self.supported_modalities, Unset):
            supported_modalities = self.supported_modalities

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eval_type_uuid": eval_type_uuid,
                "name": name,
                "slug": slug,
                "description": description,
            }
        )
        if supported_modalities is not UNSET:
            field_dict["supported_modalities"] = supported_modalities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        eval_type_uuid = d.pop("eval_type_uuid")

        name = d.pop("name")

        slug = d.pop("slug")

        description = d.pop("description")

        supported_modalities = cast(List[str], d.pop("supported_modalities", UNSET))

        eval_type_schema = cls(
            eval_type_uuid=eval_type_uuid,
            name=name,
            slug=slug,
            description=description,
            supported_modalities=supported_modalities,
        )

        eval_type_schema.additional_properties = d
        return eval_type_schema

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

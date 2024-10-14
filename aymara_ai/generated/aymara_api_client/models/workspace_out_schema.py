from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceOutSchema")


@_attrs_define
class WorkspaceOutSchema:
    """
    Attributes:
        workspace_uuid (str):
        name (str):
        organization_name (str):
    """

    workspace_uuid: str
    name: str
    organization_name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_uuid = self.workspace_uuid

        name = self.name

        organization_name = self.organization_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_uuid": workspace_uuid,
                "name": name,
                "organization_name": organization_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_uuid = d.pop("workspace_uuid")

        name = d.pop("name")

        organization_name = d.pop("organization_name")

        workspace_out_schema = cls(
            workspace_uuid=workspace_uuid,
            name=name,
            organization_name=organization_name,
        )

        workspace_out_schema.additional_properties = d
        return workspace_out_schema

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

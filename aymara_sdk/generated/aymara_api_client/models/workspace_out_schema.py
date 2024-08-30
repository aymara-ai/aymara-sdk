from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.organization_out_schema import OrganizationOutSchema


T = TypeVar("T", bound="WorkspaceOutSchema")


@_attrs_define
class WorkspaceOutSchema:
    """
    Attributes:
        workspace_uuid (str):
        name (str):
        organization (OrganizationOutSchema):
    """

    workspace_uuid: str
    name: str
    organization: "OrganizationOutSchema"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_uuid = self.workspace_uuid

        name = self.name

        organization = self.organization.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_uuid": workspace_uuid,
                "name": name,
                "organization": organization,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.organization_out_schema import OrganizationOutSchema

        d = src_dict.copy()
        workspace_uuid = d.pop("workspace_uuid")

        name = d.pop("name")

        organization = OrganizationOutSchema.from_dict(d.pop("organization"))

        workspace_out_schema = cls(
            workspace_uuid=workspace_uuid,
            name=name,
            organization=organization,
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

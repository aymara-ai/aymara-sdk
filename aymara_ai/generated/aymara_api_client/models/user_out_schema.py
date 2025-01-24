from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.feature_flags import FeatureFlags
    from ..models.organization_out_schema import OrganizationOutSchema


T = TypeVar("T", bound="UserOutSchema")


@_attrs_define
class UserOutSchema:
    """
    Attributes:
        email (str):
        is_admin (bool):
        is_impersonating (bool):
        feature_flags (FeatureFlags):
        organization (Union['OrganizationOutSchema', None, Unset]):
    """

    email: str
    is_admin: bool
    is_impersonating: bool
    feature_flags: "FeatureFlags"
    organization: Union["OrganizationOutSchema", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.organization_out_schema import OrganizationOutSchema

        email = self.email

        is_admin = self.is_admin

        is_impersonating = self.is_impersonating

        feature_flags = self.feature_flags.to_dict()

        organization: Union[Dict[str, Any], None, Unset]
        if isinstance(self.organization, Unset):
            organization = UNSET
        elif isinstance(self.organization, OrganizationOutSchema):
            organization = self.organization.to_dict()
        else:
            organization = self.organization

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "is_admin": is_admin,
                "is_impersonating": is_impersonating,
                "feature_flags": feature_flags,
            }
        )
        if organization is not UNSET:
            field_dict["organization"] = organization

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.feature_flags import FeatureFlags
        from ..models.organization_out_schema import OrganizationOutSchema

        d = src_dict.copy()
        email = d.pop("email")

        is_admin = d.pop("is_admin")

        is_impersonating = d.pop("is_impersonating")

        feature_flags = FeatureFlags.from_dict(d.pop("feature_flags"))

        def _parse_organization(data: object) -> Union["OrganizationOutSchema", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                organization_type_0 = OrganizationOutSchema.from_dict(data)

                return organization_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OrganizationOutSchema", None, Unset], data)

        organization = _parse_organization(d.pop("organization", UNSET))

        user_out_schema = cls(
            email=email,
            is_admin=is_admin,
            is_impersonating=is_impersonating,
            feature_flags=feature_flags,
            organization=organization,
        )

        user_out_schema.additional_properties = d
        return user_out_schema

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

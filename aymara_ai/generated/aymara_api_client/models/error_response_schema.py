from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.error_data_schema import ErrorDataSchema


T = TypeVar("T", bound="ErrorResponseSchema")


@_attrs_define
class ErrorResponseSchema:
    """Standardized error response schema matching AymaraAPIError structure.

    This schema is used to document API error responses in a consistent format.
    It matches the structure returned by the error handling middleware.

        Attributes:
            error (ErrorDataSchema): Schema for the contents of an error response.

                This schema defines the structure of the error data inside the `error` field
                of an API error response.
    """

    error: "ErrorDataSchema"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error_data_schema import ErrorDataSchema

        d = src_dict.copy()
        error = ErrorDataSchema.from_dict(d.pop("error"))

        error_response_schema = cls(
            error=error,
        )

        error_response_schema.additional_properties = d
        return error_response_schema

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

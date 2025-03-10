from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_code import ErrorCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_data_schema_details import ErrorDataSchemaDetails


T = TypeVar("T", bound="ErrorDataSchema")


@_attrs_define
class ErrorDataSchema:
    """Schema for the contents of an error response.

    This schema defines the structure of the error data inside the `error` field
    of an API error response.

        Attributes:
            code (ErrorCode): Enumeration of all error codes used in the API.
            message (str):
            request_id (str):
            details (Union[Unset, ErrorDataSchemaDetails]):
    """

    code: ErrorCode
    message: str
    request_id: str
    details: Union[Unset, "ErrorDataSchemaDetails"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code.value

        message = self.message

        request_id = self.request_id

        details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "request_id": request_id,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error_data_schema_details import ErrorDataSchemaDetails

        d = src_dict.copy()
        code = ErrorCode(d.pop("code"))

        message = d.pop("message")

        request_id = d.pop("request_id")

        _details = d.pop("details", UNSET)
        details: Union[Unset, ErrorDataSchemaDetails]
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = ErrorDataSchemaDetails.from_dict(_details)

        error_data_schema = cls(
            code=code,
            message=message,
            request_id=request_id,
            details=details,
        )

        error_data_schema.additional_properties = d
        return error_data_schema

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

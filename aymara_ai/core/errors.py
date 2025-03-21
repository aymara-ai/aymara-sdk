"""
Aymara AI SDK - Error Handling

This module defines the error handling system for the Aymara AI SDK.
It includes exception classes and utilities for converting API error responses
into appropriate exceptions.
"""

from typing import Dict, Optional, Type, Any, TypeVar, Union
from aymara_ai.generated.aymara_api_client.models.error_code import ErrorCode
from aymara_ai.generated.aymara_api_client.models.error_response_schema import (
    ErrorResponseSchema,
)
from aymara_ai.generated.aymara_api_client.types import Response

T = TypeVar("T")


class AymaraError(Exception):
    """Base exception class for all Aymara SDK errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SERVER_INTERNAL_ERROR,
        request_id: str = "",
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize an AymaraError.

        :param message: Error message
        :param code: Error code
        :param request_id: Request ID for debugging/support
        :param details: Additional error details
        """
        self.code = code
        self.request_id = request_id
        self.details = details or {}
        super().__init__(message)


class AuthError(AymaraError):
    """Exception raised for authentication and authorization errors."""

    pass


class QuotaError(AymaraError):
    """Exception raised for rate limiting and quota errors."""

    pass


class ResourceError(AymaraError):
    """Exception raised for errors related to resources not being found or conflicts."""

    pass


class ValidationError(AymaraError):
    """Exception raised for input validation errors."""

    pass


class ServerError(AymaraError):
    """Exception raised for internal server errors."""

    pass


# Map error code prefixes to exception classes
ERROR_PREFIX_TO_EXCEPTION: Dict[str, Type[AymaraError]] = {
    "auth": AuthError,
    "quota": QuotaError,
    "resource": ResourceError,
    "validation": ValidationError,
    "server": ServerError,
}


def get_exception_class_from_code(code: ErrorCode) -> Type[AymaraError]:
    """Get the appropriate exception class for an error code.

    :param code: Error code
    :return: Exception class
    """
    # Extract the prefix from the error code (e.g., "auth" from "auth.expired_key")
    prefix = code.split(".", 1)[0] if "." in code else code

    # Get the exception class for the prefix, or default to AymaraError
    return ERROR_PREFIX_TO_EXCEPTION.get(prefix, AymaraError)


def raise_from_error_response(response_or_error: ErrorResponseSchema) -> None:
    """Raise an appropriate exception from an API response or error.

    :param response_or_error: Error response from the API or any other error
    :raises AymaraError: An exception of the appropriate subclass
    """
    # If it's not an ErrorResponseSchema, create a generic AymaraError
    if not isinstance(response_or_error, ErrorResponseSchema):
        raise AymaraError(
            message="An unexpected error occurred",
        )

    # Process ErrorResponseSchema objects
    request_id = response_or_error.request_id
    error_data = response_or_error.error
    code = error_data.code
    message = error_data.message

    # Convert the details to a dictionary if present
    details = {}
    if error_data.details:
        details = error_data.details.to_dict()

    exception_class = get_exception_class_from_code(code)

    raise exception_class(
        message=message, code=code, request_id=request_id, details=details
    )


def get_parsed_response(response: Response[Union[Any, T]]) -> T:
    """Process an API response, returning its parsed content or raising an appropriate exception.

    :param response: Response object from an API call
    :returns: The parsed content of the response on success
    :raises AymaraError: An appropriate exception if the response indicates an error
    """

    if int(response.status_code) > 299 or (
        hasattr(response.status_code, "value") and int(response.status_code.value) > 299
    ):
        if isinstance(response.parsed, ErrorResponseSchema):
            raise_from_error_response(response.parsed)

        raise AymaraError(
            message=f"Request failed with status code {response.status_code}"
        )

    # At this point we know it's a success response, so it should be safe to cast
    return response.parsed  # type: ignore

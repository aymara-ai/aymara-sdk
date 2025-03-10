"""
Aymara AI SDK - Error Handling

This module defines the error handling system for the Aymara AI SDK.
It includes exception classes and utilities for converting API error responses
into appropriate exceptions.
"""

from typing import Dict, Optional, Type, Any, TypeVar, Union

from aymara_ai.generated.aymara_api_client.models.error_code import ErrorCode
from aymara_ai.generated.aymara_api_client.models.error_response_schema import ErrorResponseSchema
from aymara_ai.generated.aymara_api_client.types import Response

T = TypeVar('T')


class AymaraError(Exception):
    """Base exception class for all Aymara SDK errors."""

    def __init__(
        self,
        message: str,
        code: str,
        request_id: str,
        details: Optional[Dict[str, Any]] = None
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


class RateLimitError(AymaraError):
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
    "rate_limit": RateLimitError,
    "resource": ResourceError,
    "validation": ValidationError,
    "server": ServerError,
}


# Message templates for error codes
ERROR_MESSAGE_TEMPLATES: Dict[str, str] = {
    ErrorCode.AUTH_EXPIRED_KEY: "API key has expired. Please renew your subscription.",
    ErrorCode.AUTH_INSUFFICIENT_PERMISSIONS: "Insufficient permissions to perform this action.",
    ErrorCode.AUTH_INVALID_KEY: "Invalid API key provided.",
    
    ErrorCode.RATE_LIMIT_QUOTA_EXCEEDED: "Account quota exceeded. Please upgrade your plan.",
    ErrorCode.RATE_LIMIT_REQUEST_LIMIT: "Request rate limit exceeded. Please slow down your requests.",
    ErrorCode.RATE_LIMIT_TEST_QUOTA_EXCEEDED: "Test quota exceeded. Please upgrade your plan for additional tests.",
    
    ErrorCode.RESOURCE_CONFLICT: "Resource conflict: {details}",
    ErrorCode.RESOURCE_NOT_FOUND: "Resource not found.",
    ErrorCode.RESOURCE_POLICY_NOT_FOUND: "Policy not found: {policy_id}",
    ErrorCode.RESOURCE_SCORE_RUN_NOT_FOUND: "Score run not found: {score_run_id}",
    ErrorCode.RESOURCE_TEST_NOT_FOUND: "Test not found: {test_id}",
    
    ErrorCode.VALIDATION_INVALID_FORMAT: "Invalid format: {details}",
    ErrorCode.VALIDATION_INVALID_REQUEST: "Invalid request: {details}",
    ErrorCode.VALIDATION_MISSING_FIELD: "Missing required field: {field}",
    
    ErrorCode.SERVER_INTERNAL_ERROR: "Internal server error. Please contact support with the request ID."
}


def format_error_message(code: str, details: Optional[Dict[str, Any]] = None) -> str:
    """Format an error message using the template for the given error code.
    
    :param code: Error code
    :param details: Error details for message formatting
    :return: Formatted error message
    """
    template = ERROR_MESSAGE_TEMPLATES.get(code, "Unknown error: {code}")
    
    # If no details are provided, or the template doesn't contain format placeholders
    if not details or "{" not in template:
        return template
    
    try:
        # Try to format with the details provided
        return template.format(**details)
    except KeyError:
        # If formatting fails due to missing keys, return the template as is
        return template


def get_exception_class_from_code(code: str) -> Type[AymaraError]:
    """Get the appropriate exception class for an error code.
    
    :param code: Error code
    :return: Exception class
    """
    # Extract the prefix from the error code (e.g., "auth" from "auth.expired_key")
    prefix = code.split(".", 1)[0] if "." in code else code
    
    # Get the exception class for the prefix, or default to AymaraError
    return ERROR_PREFIX_TO_EXCEPTION.get(prefix, AymaraError)


def raise_from_error_response(response_or_error: Any) -> None:
    """Raise an appropriate exception from an API response or error.
    
    :param response_or_error: Error response from the API or any other error
    :raises AymaraError: An exception of the appropriate subclass
    """
    # If it's not an ErrorResponseSchema, create a generic AymaraError
    if not isinstance(response_or_error, ErrorResponseSchema):
        raise AymaraError(
            message="An unexpected error occurred",
            code="server.internal_error",
            request_id="",
            details={}
        )
    
    # Process ErrorResponseSchema objects
    error_data = response_or_error.error
    code = error_data.code.value
    message = error_data.message
    request_id = error_data.request_id
    
    # Convert the details to a dictionary if present
    details = {}
    if error_data.details:
        details = error_data.details.to_dict()
    
    # Get the appropriate exception class and formatted message
    exception_class = get_exception_class_from_code(code)
    formatted_message = format_error_message(code, details) or message
    
    # Raise the exception
    raise exception_class(
        message=formatted_message,
        code=code,
        request_id=request_id,
        details=details
    )


def get_parsed_response(response: Response[Union[ErrorResponseSchema, T]]) -> T:
    """Process an API response, returning its parsed content or raising an appropriate exception.
    
    :param response: Response object from an API call
    :returns: The parsed content of the response on success
    :raises AymaraError: An appropriate exception if the response indicates an error
    """
    if response.status_code > 299:
        if isinstance(response.parsed, ErrorResponseSchema):
            raise_from_error_response(response.parsed)
        else:
            raise AymaraError(
                message=f"Request failed with status code {response.status_code}",
                code="server.internal_error",
                request_id="",
                details={}
            )
    
    # At this point we know it's a success response, so it should be safe to cast
    return response.parsed  # type: ignore
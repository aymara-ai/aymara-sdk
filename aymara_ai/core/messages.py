# Message templates for error codes
from aymara_ai.generated.aymara_api_client.models.error_code import ErrorCode


from typing import Dict


ERROR_MESSAGE_TEMPLATES: Dict[ErrorCode, str] = {
    ErrorCode.AUTH_EXPIRED_KEY: "API key has expired. Please renew your subscription.",
    ErrorCode.AUTH_INSUFFICIENT_PERMISSIONS: "Insufficient permissions to perform this action.",
    ErrorCode.AUTH_INVALID_KEY: "Invalid API key provided.",

    ErrorCode.QUOTA_LIMIT_EXCEEDED: "Account quota exceeded. Please upgrade your plan.",

    ErrorCode.RESOURCE_CONFLICT: "Resource conflict: {details}",
    ErrorCode.RESOURCE_NOT_FOUND: "Resource not found: {resource_id}",

    ErrorCode.VALIDATION_INVALID_FORMAT: "Invalid format: {details}",
    ErrorCode.VALIDATION_INVALID_REQUEST: "Invalid request: {details}",

    ErrorCode.SERVER_INTERNAL_ERROR: "Internal server error. Please contact support with the request ID."
}
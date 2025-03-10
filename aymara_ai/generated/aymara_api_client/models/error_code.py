from enum import Enum


class ErrorCode(str, Enum):
    AUTH_EXPIRED_KEY = "auth.expired_key"
    AUTH_INSUFFICIENT_PERMISSIONS = "auth.insufficient_permissions"
    AUTH_INVALID_KEY = "auth.invalid_key"
    QUOTA_LIMIT_EXCEEDED = "quota.limit_exceeded"
    RESOURCE_CONFLICT = "resource.conflict"
    RESOURCE_NOT_FOUND = "resource.not_found"
    SERVER_INTERNAL_ERROR = "server.internal_error"
    VALIDATION_INVALID_FORMAT = "validation.invalid_format"
    VALIDATION_INVALID_REQUEST = "validation.invalid_request"

    def __str__(self) -> str:
        return str(self.value)

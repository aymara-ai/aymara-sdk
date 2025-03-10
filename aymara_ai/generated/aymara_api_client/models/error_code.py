from enum import Enum


class ErrorCode(str, Enum):
    AUTH_EXPIRED_KEY = "auth.expired_key"
    AUTH_INSUFFICIENT_PERMISSIONS = "auth.insufficient_permissions"
    AUTH_INVALID_KEY = "auth.invalid_key"
    RATE_LIMIT_QUOTA_EXCEEDED = "rate_limit.quota_exceeded"
    RATE_LIMIT_REQUEST_LIMIT = "rate_limit.request_limit"
    RATE_LIMIT_TEST_QUOTA_EXCEEDED = "rate_limit.test_quota_exceeded"
    RESOURCE_CONFLICT = "resource.conflict"
    RESOURCE_NOT_FOUND = "resource.not_found"
    RESOURCE_POLICY_NOT_FOUND = "resource.policy_not_found"
    RESOURCE_SCORE_RUN_NOT_FOUND = "resource.score_run_not_found"
    RESOURCE_TEST_NOT_FOUND = "resource.test_not_found"
    SERVER_INTERNAL_ERROR = "server.internal_error"
    VALIDATION_INVALID_FORMAT = "validation.invalid_format"
    VALIDATION_INVALID_REQUEST = "validation.invalid_request"
    VALIDATION_MISSING_FIELD = "validation.missing_field"

    def __str__(self) -> str:
        return str(self.value)

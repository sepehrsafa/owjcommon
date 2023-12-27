from .schemas import ErrorResponse, ValidationErrorResponse

responses = {
    400: {
        "model": ErrorResponse,
        "description": "An error occurred. Check the error code and message.",
    },
    401: {
        "model": ErrorResponse,
        "description": "Authentication failed. Check the error code and message.",
    },
    422: {
        "model": ValidationErrorResponse,
        "description": "Validation error. The input doesn't match the schema. Check the error code and message.",
    },
    403: {
        "model": ErrorResponse,
        "description": "Permission denied. Check the error code and message.",
    },
}

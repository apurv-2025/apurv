# backend/utils/exceptions.py
from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BusinessLogicException(Exception):
    """Custom exception for business logic errors."""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationException(Exception):
    """Custom exception for validation errors."""

    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

def create_http_exception(
    status_code: int,
    detail: str,
    headers: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a standardized HTTP exception."""
    return HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers
    )

# Common HTTP exceptions
def not_found_exception(resource: str = "Resource") -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found"
    )

def permission_denied_exception(action: str = "perform this action") -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Not enough permissions to {action}"
    )

def validation_exception(message: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )

def conflict_exception(message: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )


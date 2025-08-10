# File: app/schemas/common.py
from typing import Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    status: str
    service: str
    version: str
    timestamp: datetime
    database_status: str
    dependencies: Optional[Dict[str, str]] = None


class ErrorResponse(BaseModel):
    """Schema for error response."""
    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    timestamp: datetime


class SuccessResponse(BaseModel):
    """Schema for success response."""
    message: str
    data: Optional[Any] = None
    timestamp: datetime


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    skip: int = 0
    limit: int = 100
    
    class Config:
        extra = "forbid"


class PaginatedResponse(BaseModel):
    """Schema for paginated response."""
    items: list
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool

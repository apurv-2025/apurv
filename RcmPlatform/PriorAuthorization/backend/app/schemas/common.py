# File: app/schemas/common.py
from typing import Optional, List, Dict, Any, Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime

DataType = TypeVar('DataType')


class MessageResponse(BaseModel):
    """Standard message response"""
    message: str
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    success: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginatedResponse(BaseModel, Generic[DataType]):
    """Paginated response wrapper"""
    items: List[DataType]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class EDIResponse(BaseModel):
    """Base EDI response"""
    edi_content: str
    transaction_type: str  # 275, 278, etc.
    control_number: str
    generated_at: datetime
    message: str


class ValidationError(BaseModel):
    """Validation error details"""
    field: str
    message: str
    value: Optional[Any] = None


class BusinessRuleError(BaseModel):
    """Business rule validation error"""
    rule: str
    message: str
    context: Optional[Dict[str, Any]] = None

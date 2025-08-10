# File: app/schemas/audit.py
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class AuthorizationAuditBase(BaseModel):
    """Base authorization audit schema"""
    request_id: str = Field(..., max_length=50)
    action: str = Field(..., max_length=50)
    actor: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = Field(None, max_length=5000)
    previous_status: Optional[str] = Field(None, max_length=20)
    new_status: Optional[str] = Field(None, max_length=20)
    metadata: Optional[Dict[str, Any]] = None


class AuthorizationAuditCreate(AuthorizationAuditBase):
    """Schema for creating audit entry"""
    pass


class AuthorizationAudit(AuthorizationAuditBase):
    """Complete authorization audit schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AuditSearchRequest(BaseModel):
    """Audit search request schema"""
    request_id: Optional[str] = Field(None, max_length=50)
    action: Optional[str] = Field(None, max_length=50)
    actor: Optional[str] = Field(None, max_length=255)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


class AuditSummary(BaseModel):
    """Audit summary for lists"""
    id: int
    request_id: str
    action: str
    actor: Optional[str] = None
    previous_status: Optional[str] = None
    new_status: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

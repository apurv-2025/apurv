# File: app/schemas/codes.py
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ServiceTypeCodeBase(BaseModel):
    """Base service type code schema"""
    code: str = Field(..., min_length=1, max_length=10)
    description: str = Field(..., min_length=1, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    requires_authorization: bool = True
    is_active: bool = True


class ServiceTypeCodeCreate(ServiceTypeCodeBase):
    """Schema for creating service type code"""
    pass


class ServiceTypeCodeUpdate(BaseModel):
    """Schema for updating service type code"""
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    requires_authorization: Optional[bool] = None
    is_active: Optional[bool] = None


class ServiceTypeCode(ServiceTypeCodeBase):
    """Complete service type code schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProcedureCodeBase(BaseModel):
    """Base procedure code schema"""
    code: str = Field(..., min_length=1, max_length=20)
    description: str = Field(..., min_length=1, max_length=500)
    code_type: Optional[str] = Field(None, max_length=10)  # CPT, HCPCS
    category: Optional[str] = Field(None, max_length=100)
    requires_authorization: bool = False
    is_active: bool = True


class ProcedureCodeCreate(ProcedureCodeBase):
    """Schema for creating procedure code"""
    pass


class ProcedureCodeUpdate(BaseModel):
    """Schema for updating procedure code"""
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    code_type: Optional[str] = Field(None, max_length=10)
    category: Optional[str] = Field(None, max_length=100)
    requires_authorization: Optional[bool] = None
    is_active: Optional[bool] = None


class ProcedureCode(ProcedureCodeBase):
    """Complete procedure code schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DiagnosisCodeBase(BaseModel):
    """Base diagnosis code schema"""
    code: str = Field(..., min_length=1, max_length=20)
    description: str = Field(..., min_length=1, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    is_active: bool = True


class DiagnosisCodeCreate(DiagnosisCodeBase):
    """Schema for creating diagnosis code"""
    pass


class DiagnosisCodeUpdate(BaseModel):
    """Schema for updating diagnosis code"""
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class DiagnosisCode(DiagnosisCodeBase):
    """Complete diagnosis code schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CodeSearchRequest(BaseModel):
    """Code search request schema"""
    search_term: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    active_only: bool = True
    requires_authorization: Optional[bool] = None

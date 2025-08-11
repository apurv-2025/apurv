# Healthcare Codes Schemas
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ServiceTypeCodeBase(BaseModel):
    code: str = Field(..., description="Service type code")
    description: str = Field(..., description="Code description")
    category: Optional[str] = Field(None, description="Code category")
    requires_authorization: bool = Field(True, description="Whether authorization is required")
    is_active: bool = Field(True, description="Whether code is active")


class ServiceTypeCodeCreate(ServiceTypeCodeBase):
    pass


class ServiceTypeCode(ServiceTypeCodeBase):
    id: int = Field(..., description="Code ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    model_config = {"from_attributes": True}


class ProcedureCodeBase(BaseModel):
    code: str = Field(..., description="CPT or HCPCS code")
    description: str = Field(..., description="Code description")
    code_type: Optional[str] = Field(None, description="Code type (CPT, HCPCS)")
    category: Optional[str] = Field(None, description="Code category")
    requires_authorization: bool = Field(False, description="Whether authorization is required")
    is_active: bool = Field(True, description="Whether code is active")


class ProcedureCodeCreate(ProcedureCodeBase):
    pass


class ProcedureCode(ProcedureCodeBase):
    id: int = Field(..., description="Code ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    model_config = {"from_attributes": True}


class DiagnosisCodeBase(BaseModel):
    code: str = Field(..., description="ICD-10 diagnosis code")
    description: str = Field(..., description="Code description")
    category: Optional[str] = Field(None, description="Code category")
    is_active: bool = Field(True, description="Whether code is active")


class DiagnosisCodeCreate(DiagnosisCodeBase):
    pass


class DiagnosisCode(DiagnosisCodeBase):
    id: int = Field(..., description="Code ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    model_config = {"from_attributes": True}


class CodeSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    code_type: Optional[str] = Field(None, description="Type of code to search")
    limit: int = Field(10, description="Maximum number of results")
    offset: int = Field(0, description="Number of results to skip")


class CodeSearchResponse(BaseModel):
    codes: List[ProcedureCode] = Field(..., description="Matching codes")
    total: int = Field(..., description="Total number of matches")
    query: str = Field(..., description="Search query used")

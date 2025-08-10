# File: app/schemas/provider.py
from typing import Optional
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime


class ProviderBase(BaseModel):
    """Base schema for provider."""
    npi: str
    name: str
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[EmailStr] = None
    specialty: Optional[str] = None
    taxonomy_code: Optional[str] = None
    provider_type: Optional[str] = None
    
    @validator('npi')
    def validate_npi(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('NPI must be exactly 10 digits')
        return v


class ProviderCreate(ProviderBase):
    """Schema for creating provider."""
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    dea_number: Optional[str] = None


class ProviderUpdate(BaseModel):
    """Schema for updating provider."""
    name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[EmailStr] = None
    specialty: Optional[str] = None
    taxonomy_code: Optional[str] = None
    provider_type: Optional[str] = None
    is_active: Optional[bool] = None


class Provider(ProviderBase):
    """Schema for provider response."""
    id: int
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    dea_number: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# File: app/schemas/payer.py
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime


class InsurancePayerBase(BaseModel):
    """Base schema for insurance payer."""
    payer_id: str
    payer_name: str
    contact_info: Optional[Dict[str, Any]] = None
    supported_transactions: Optional[List[str]] = None
    endpoint_url: Optional[str] = None
    edi_submitter_id: Optional[str] = None
    edi_receiver_id: Optional[str] = None
    payer_type: Optional[str] = None
    market_area: Optional[List[str]] = None


class InsurancePayerCreate(InsurancePayerBase):
    """Schema for creating insurance payer."""
    api_key: Optional[str] = None
    username: Optional[str] = None
    test_mode: bool = False


class InsurancePayerUpdate(BaseModel):
    """Schema for updating insurance payer."""
    payer_name: Optional[str] = None
    contact_info: Optional[Dict[str, Any]] = None
    supported_transactions: Optional[List[str]] = None
    endpoint_url: Optional[str] = None
    edi_submitter_id: Optional[str] = None
    edi_receiver_id: Optional[str] = None
    is_active: Optional[bool] = None
    test_mode: Optional[bool] = None
    payer_type: Optional[str] = None
    market_area: Optional[List[str]] = None


class InsurancePayer(InsurancePayerBase):
    """Schema for insurance payer response."""
    id: int
    is_active: bool
    test_mode: bool
    response_time_avg_ms: Optional[int] = None
    success_rate: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


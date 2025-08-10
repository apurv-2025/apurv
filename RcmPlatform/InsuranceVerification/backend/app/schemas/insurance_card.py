# File: app/schemas/insurance_card.py
from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime


class InsuranceCardBase(BaseModel):
    """Base schema for insurance card."""
    patient_name: Optional[str] = None
    member_id: Optional[str] = None
    group_number: Optional[str] = None
    plan_name: Optional[str] = None
    insurance_company: Optional[str] = None
    effective_date: Optional[str] = None
    phone_number: Optional[str] = None


class InsuranceCardCreate(InsuranceCardBase):
    """Schema for creating insurance card."""
    member_id: str  # Required for creation
    raw_text: Optional[str] = None
    confidence_score: Optional[float] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class InsuranceCardUpdate(InsuranceCardBase):
    """Schema for updating insurance card."""
    pass


class InsuranceCard(InsuranceCardBase):
    """Schema for insurance card response."""
    id: int
    raw_text: Optional[str] = None
    confidence_score: Optional[float] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    """Schema for file upload response."""
    card_id: int
    extracted_data: InsuranceCard
    raw_text: str
    confidence_score: Optional[float] = None
    processing_time_ms: int

# File: app/schemas/eligibility.py
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, validator
from datetime import datetime, date
from enum import Enum


class ServiceType(str, Enum):
    """Enumeration for service types."""
    HEALTH_BENEFIT_PLAN = "30"
    MEDICAL_CARE = "1"
    PHARMACY = "88"
    PROFESSIONAL_SERVICES = "98"
    SURGICAL = "2"
    CONSULTATION = "3"
    DIAGNOSTIC_XRAY = "4"
    DIAGNOSTIC_LAB = "5"
    RADIATION_THERAPY = "6"
    ANESTHESIA = "7"


class RequestStatus(str, Enum):
    """Enumeration for request status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    TIMEOUT = "timeout"


class EligibilityRequestBase(BaseModel):
    """Base schema for eligibility request."""
    member_id: str
    provider_npi: str
    service_type: ServiceType = ServiceType.HEALTH_BENEFIT_PLAN
    subscriber_first_name: str
    subscriber_last_name: str
    subscriber_dob: date
    
    @validator('provider_npi')
    def validate_npi(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('NPI must be exactly 10 digits')
        return v
    
    @validator('subscriber_dob')
    def validate_dob(cls, v):
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v


class EligibilityRequestCreate(EligibilityRequestBase):
    """Schema for creating eligibility request."""
    insurance_card_id: Optional[int] = None


class EligibilityRequest(EligibilityRequestBase):
    """Schema for eligibility request response."""
    id: int
    request_id: str
    status: RequestStatus
    edi_270_content: str
    submitter_id: Optional[str] = None
    receiver_id: Optional[str] = None
    interchange_control_number: Optional[str] = None
    group_control_number: Optional[str] = None
    transaction_control_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BenefitsInfo(BaseModel):
    """Schema for benefits information."""
    coverage_status: Optional[str] = None
    effective_date: Optional[date] = None
    termination_date: Optional[date] = None
    copay_amount: Optional[float] = None
    deductible_amount: Optional[float] = None
    out_of_pocket_max: Optional[float] = None
    coinsurance_percentage: Optional[float] = None
    benefits: Optional[Dict[str, Any]] = None


class EligibilityResponseBase(BaseModel):
    """Base schema for eligibility response."""
    is_eligible: bool
    benefits_info: Optional[BenefitsInfo] = None
    coverage_status: Optional[str] = None
    payer_id: Optional[str] = None
    payer_name: Optional[str] = None
    response_code: Optional[str] = None


class EligibilityResponse(EligibilityResponseBase):
    """Schema for eligibility response."""
    id: int
    request_id: str
    edi_271_content: str
    processing_time_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class EligibilityInquiryResponse(BaseModel):
    """Schema for eligibility inquiry submission response."""
    request_id: str
    edi_270: str
    status: RequestStatus
    message: str


class EligibilityVerificationResponse(BaseModel):
    """Schema for complete eligibility verification response."""
    request_id: str
    edi_271: str
    is_eligible: bool
    benefits_info: Optional[Dict[str, Any]] = None
    processed_at: datetime
    processing_time_ms: Optional[int] = None

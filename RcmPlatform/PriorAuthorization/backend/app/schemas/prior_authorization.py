# File: app/schemas/prior_authorization.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, date
from enum import Enum


class RequestType(str, Enum):
    """EDI 278 Request Types"""
    INITIAL = "00"
    RECONSIDERATION = "01"
    APPEAL = "02"
    CANCELLATION = "03"
    MODIFICATION = "04"


class CertificationType(str, Enum):
    """EDI 278 Certification Types"""
    INITIAL = "I"
    RENEWAL = "R"
    REVISION = "S"
    CANCELLATION = "C"


class ResponseCode(str, Enum):
    """EDI 278 Response Codes"""
    APPROVED = "A1"
    MODIFIED = "A2"
    DENIED = "A3"
    PENDED = "A4"
    CANCELLED = "A6"


class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"
    UNKNOWN = "U"


class Priority(str, Enum):
    NORMAL = "normal"
    URGENT = "urgent"
    EMERGENCY = "emergency"


class ProcedureCodeInfo(BaseModel):
    """Procedure code information"""
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    modifier: Optional[str] = Field(None, max_length=10)
    units: Optional[int] = Field(1, ge=1)
    code_type: Optional[str] = Field(None, max_length=10)  # CPT, HCPCS
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError('Procedure code cannot be empty')
        return v.strip().upper()


class DiagnosisCodeInfo(BaseModel):
    """Diagnosis code information"""
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    is_primary: bool = False
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError('Diagnosis code cannot be empty')
        return v.strip().upper()


class PriorAuthorizationRequestBase(BaseModel):
    """Base prior authorization request schema"""
    # Patient Information
    patient_first_name: str = Field(..., min_length=1, max_length=100)
    patient_last_name: str = Field(..., min_length=1, max_length=100)
    patient_dob: date
    patient_gender: Gender
    member_id: str = Field(..., min_length=1, max_length=100)
    
    # Provider Information
    requesting_provider_npi: str = Field(..., min_length=10, max_length=10)
    requesting_provider_name: Optional[str] = Field(None, max_length=255)
    servicing_provider_npi: Optional[str] = Field(None, min_length=10, max_length=10)
    servicing_provider_name: Optional[str] = Field(None, max_length=255)
    
    # Authorization Details
    request_type: RequestType = RequestType.INITIAL
    certification_type: CertificationType = CertificationType.INITIAL
    service_type_code: Optional[str] = Field(None, max_length=10)
    
    # Service Information
    procedure_codes: List[ProcedureCodeInfo] = Field(..., min_length=1)
    diagnosis_codes: List[DiagnosisCodeInfo] = Field(..., min_length=1)
    service_date_from: date
    service_date_to: Optional[date] = None
    units_requested: Optional[int] = Field(1, ge=1)
    
    # Clinical Information
    clinical_information: Optional[str] = Field(None, max_length=5000)
    medical_necessity: str = Field(..., min_length=1, max_length=5000)
    
    # Priority
    priority: Priority = Priority.NORMAL
    
    @field_validator('requesting_provider_npi', 'servicing_provider_npi')
    @classmethod
    def validate_npi(cls, v):
        if v is not None:
            if not v.isdigit() or len(v) != 10:
                raise ValueError('NPI must be exactly 10 digits')
        return v
    
    @field_validator('service_date_to')
    @classmethod
    def validate_service_dates(cls, v, info):
        if v is not None and 'service_date_from' in info.data:
            if v < info.data['service_date_from']:
                raise ValueError('Service date to must be after service date from')
        return v


class PriorAuthorizationRequestCreate(PriorAuthorizationRequestBase):
    """Schema for creating a new prior authorization request"""
    pass


class PriorAuthorizationRequest(PriorAuthorizationRequestBase):
    """Complete prior authorization request schema"""
    id: int
    request_id: str
    patient_id: str
    status: str
    edi_278_content: str
    
    # Tracking Information
    submitter_id: Optional[str] = None
    receiver_id: Optional[str] = None
    interchange_control_number: Optional[str] = None
    group_control_number: Optional[str] = None
    transaction_control_number: Optional[str] = None
    
    # Supporting Documentation
    supporting_documentation: Optional[List[Dict[str, Any]]] = None
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AuthorizationDecision(BaseModel):
    """Authorization decision schema"""
    response_code: ResponseCode
    authorization_number: Optional[str] = Field(None, max_length=50)
    effective_date: Optional[date] = None
    expiration_date: Optional[date] = None
    units_approved: Optional[int] = Field(None, ge=0)
    decision_reason: Optional[str] = Field(None, max_length=5000)
    additional_information_required: Optional[str] = Field(None, max_length=5000)
    
    @field_validator('expiration_date')
    @classmethod
    def validate_expiration_date(cls, v, info):
        if v is not None and 'effective_date' in info.data:
            if info.data['effective_date'] and v <= info.data['effective_date']:
                raise ValueError('Expiration date must be after effective date')
        return v


class PriorAuthorizationResponse(BaseModel):
    """Prior authorization response schema"""
    id: int
    request_id: str
    response_code: ResponseCode
    authorization_number: Optional[str] = None
    effective_date: Optional[date] = None
    expiration_date: Optional[date] = None
    approved_services: Optional[Dict[str, Any]] = None
    units_approved: Optional[int] = None
    units_used: Optional[int] = None
    decision_reason: Optional[str] = None
    reviewer_name: Optional[str] = None
    review_date: Optional[datetime] = None
    additional_information_required: Optional[str] = None
    follow_up_required: Optional[bool] = False
    follow_up_date: Optional[date] = None
    edi_278_response_content: str
    processing_time_ms: Optional[int] = None
    payer_id: Optional[str] = None
    payer_name: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PriorAuthorizationInquiryResponse(BaseModel):
    """EDI 278 inquiry response"""
    request_id: str
    edi_278: str
    status: str
    message: str
    control_number: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PriorAuthorizationDecisionResponse(BaseModel):
    """EDI 278 decision response"""
    request_id: str
    edi_278_response: str
    response_code: ResponseCode
    authorization_number: Optional[str] = None
    decision_details: Optional[Dict[str, Any]] = None
    processed_at: datetime
    control_number: Optional[str] = None


class AuthorizationSearchRequest(BaseModel):
    """Authorization search request schema"""
    patient_name: Optional[str] = Field(None, max_length=200)
    member_id: Optional[str] = Field(None, max_length=100)
    provider_npi: Optional[str] = Field(None, min_length=10, max_length=10)
    status: Optional[str] = Field(None, max_length=50)
    service_date_from: Optional[date] = None
    service_date_to: Optional[date] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
    priority: Optional[Priority] = None


class AuthorizationSummary(BaseModel):
    """Authorization summary for lists"""
    id: int
    request_id: str
    patient_first_name: str
    patient_last_name: str
    member_id: str
    requesting_provider_npi: str
    status: str
    priority: Priority
    service_date_from: date
    units_requested: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}

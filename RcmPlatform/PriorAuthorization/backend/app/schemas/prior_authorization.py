# Prior Authorization Schemas
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from enum import Enum


class RequestType(str, Enum):
    INITIAL = "00"
    RECONSIDERATION = "01"
    APPEAL = "02"
    CANCELLATION = "03"
    MODIFICATION = "04"


class CertificationType(str, Enum):
    INITIAL = "I"
    RENEWAL = "R"
    REVISION = "S"
    CANCELLATION = "C"


class ResponseCode(str, Enum):
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
    code: str = Field(..., description="CPT or HCPCS code")
    description: Optional[str] = Field(None, description="Code description")
    modifier: Optional[str] = Field(None, description="Procedure modifier")
    units: Optional[int] = Field(1, description="Number of units")


class DiagnosisCodeInfo(BaseModel):
    code: str = Field(..., description="ICD-10 diagnosis code")
    description: Optional[str] = Field(None, description="Diagnosis description")
    is_primary: bool = Field(False, description="Whether this is the primary diagnosis")


class PriorAuthorizationRequestBase(BaseModel):
    # Patient Information
    patient_first_name: str = Field(..., description="Patient first name")
    patient_last_name: str = Field(..., description="Patient last name")
    patient_dob: date = Field(..., description="Patient date of birth")
    patient_gender: Gender = Field(..., description="Patient gender")
    member_id: str = Field(..., description="Insurance member ID")
    
    # Provider Information
    requesting_provider_npi: str = Field(..., description="Requesting provider NPI")
    requesting_provider_name: Optional[str] = Field(None, description="Requesting provider name")
    servicing_provider_npi: Optional[str] = Field(None, description="Servicing provider NPI")
    servicing_provider_name: Optional[str] = Field(None, description="Servicing provider name")
    
    # Authorization Details
    request_type: RequestType = Field(RequestType.INITIAL, description="Request type")
    certification_type: CertificationType = Field(CertificationType.INITIAL, description="Certification type")
    service_type_code: Optional[str] = Field(None, description="Healthcare service type code")
    
    # Service Information
    procedure_codes: List[ProcedureCodeInfo] = Field(..., description="List of procedure codes")
    diagnosis_codes: List[DiagnosisCodeInfo] = Field(..., description="List of diagnosis codes")
    service_date_from: date = Field(..., description="Service start date")
    service_date_to: Optional[date] = Field(None, description="Service end date")
    units_requested: Optional[int] = Field(1, description="Units requested")
    
    # Clinical Information
    clinical_information: Optional[str] = Field(None, description="Clinical information")
    medical_necessity: str = Field(..., description="Medical necessity statement")
    
    # Priority
    priority: Priority = Field(Priority.NORMAL, description="Request priority")

    @field_validator('requesting_provider_npi')
    @classmethod
    def validate_npi(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('NPI must be exactly 10 digits')
        return v


class PriorAuthorizationRequestCreate(PriorAuthorizationRequestBase):
    pass


class PriorAuthorizationRequest(PriorAuthorizationRequestBase):
    id: int = Field(..., description="Request ID")
    request_id: str = Field(..., description="Unique request identifier")
    patient_id: str = Field(..., description="Patient ID")
    status: str = Field(..., description="Request status")
    edi_278_content: str = Field(..., description="EDI 278 content")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    model_config = {"from_attributes": True}


class AuthorizationDecision(BaseModel):
    response_code: ResponseCode = Field(..., description="Authorization response code")
    authorization_number: Optional[str] = Field(None, description="Authorization number")
    effective_date: Optional[date] = Field(None, description="Authorization effective date")
    expiration_date: Optional[date] = Field(None, description="Authorization expiration date")
    units_approved: Optional[int] = Field(None, description="Units approved")
    decision_reason: Optional[str] = Field(None, description="Decision reason")
    additional_information_required: Optional[str] = Field(None, description="Additional information required")


class PriorAuthorizationResponse(BaseModel):
    id: int = Field(..., description="Response ID")
    request_id: str = Field(..., description="Associated request ID")
    response_code: ResponseCode = Field(..., description="Response code")
    authorization_number: Optional[str] = Field(None, description="Authorization number")
    effective_date: Optional[date] = Field(None, description="Effective date")
    expiration_date: Optional[date] = Field(None, description="Expiration date")
    approved_services: Optional[Dict[str, Any]] = Field(None, description="Approved services details")
    units_approved: Optional[int] = Field(None, description="Units approved")
    decision_reason: Optional[str] = Field(None, description="Decision reason")
    edi_278_response_content: str = Field(..., description="EDI 278 response content")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = {"from_attributes": True}


class PriorAuthorizationInquiryResponse(BaseModel):
    request_id: str = Field(..., description="Request ID")
    edi_278: str = Field(..., description="EDI 278 content")
    status: str = Field(..., description="Request status")
    message: str = Field(..., description="Response message")


class PriorAuthorizationDecisionResponse(BaseModel):
    request_id: str = Field(..., description="Request ID")
    edi_278_response: str = Field(..., description="EDI 278 response content")
    response_code: ResponseCode = Field(..., description="Response code")
    authorization_number: Optional[str] = Field(None, description="Authorization number")
    decision_details: Optional[Dict[str, Any]] = Field(None, description="Decision details")
    processed_at: datetime = Field(..., description="Processing timestamp")


class AuthorizationSummary(BaseModel):
    """Authorization summary for lists"""
    id: int = Field(..., description="Authorization ID")
    request_id: str = Field(..., description="Request ID")
    patient_first_name: str = Field(..., description="Patient first name")
    patient_last_name: str = Field(..., description="Patient last name")
    member_id: str = Field(..., description="Member ID")
    requesting_provider_npi: str = Field(..., description="Requesting provider NPI")
    status: str = Field(..., description="Request status")
    priority: Priority = Field(..., description="Priority")
    service_date_from: date = Field(..., description="Service start date")
    units_requested: Optional[int] = Field(None, description="Units requested")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = {"from_attributes": True}


class AuthorizationSearchRequest(BaseModel):
    """Authorization search request schema"""
    patient_name: Optional[str] = Field(None, description="Patient name")
    member_id: Optional[str] = Field(None, description="Member ID")
    provider_npi: Optional[str] = Field(None, description="Provider NPI")
    status: Optional[str] = Field(None, description="Request status")
    service_date_from: Optional[date] = Field(None, description="Service start date")
    service_date_to: Optional[date] = Field(None, description="Service end date")
    created_from: Optional[datetime] = Field(None, description="Created from date")
    created_to: Optional[datetime] = Field(None, description="Created to date")
    priority: Optional[Priority] = Field(None, description="Priority")

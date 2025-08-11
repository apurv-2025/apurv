# File: app/models/models.py - Database Models for EDI 278/275
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    Date, DECIMAL, ForeignKey, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RequestTypeEnum(enum.Enum):
    """EDI 278 Request Types"""
    INITIAL = "00"  # Initial request
    RECONSIDERATION = "01"  # Reconsideration request
    APPEAL = "02"  # Appeal request
    CANCELLATION = "03"  # Cancellation request
    MODIFICATION = "04"  # Modification request


class CertificationTypeEnum(enum.Enum):
    """EDI 278 Certification Types"""
    INITIAL = "I"  # Initial certification
    RENEWAL = "R"  # Renewal certification
    REVISION = "S"  # Revised certification
    CANCELLATION = "C"  # Cancellation


class ResponseCodeEnum(enum.Enum):
    """EDI 278 Response Codes"""
    APPROVED = "A1"  # Approved
    MODIFIED = "A2"  # Approved with modifications
    DENIED = "A3"  # Denied
    PENDED = "A4"  # Pended for more information
    CANCELLED = "A6"  # Cancelled


class PriorAuthorizationRequest(Base, TimestampMixin):
    """Model for EDI 278 Prior Authorization Requests"""
    __tablename__ = "prior_authorization_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Patient Information
    patient_id = Column(String(100), nullable=False, index=True)
    patient_first_name = Column(String(100), nullable=False)
    patient_last_name = Column(String(100), nullable=False)
    patient_dob = Column(Date, nullable=False)
    patient_gender = Column(String(1))  # M, F, U
    member_id = Column(String(100), nullable=False, index=True)
    
    # Provider Information
    requesting_provider_npi = Column(String(20), nullable=False)
    requesting_provider_name = Column(String(255))
    servicing_provider_npi = Column(String(20))
    servicing_provider_name = Column(String(255))
    
    # Authorization Details
    request_type = Column(SQLEnum(RequestTypeEnum), nullable=False)
    certification_type = Column(SQLEnum(CertificationTypeEnum), nullable=False)
    service_type_code = Column(String(10))  # Healthcare service type
    
    # Service Information
    procedure_codes = Column(JSON)  # Array of CPT/HCPCS codes
    diagnosis_codes = Column(JSON)  # Array of ICD-10 codes
    service_date_from = Column(Date)
    service_date_to = Column(Date)
    units_requested = Column(Integer)
    
    # Clinical Information
    clinical_information = Column(Text)
    medical_necessity = Column(Text)
    supporting_documentation = Column(JSON)  # Attachments metadata
    
    # Request Status
    status = Column(String(20), default="submitted", index=True)
    priority = Column(String(10), default="normal")  # normal, urgent, emergency
    
    # EDI Content
    edi_278_content = Column(Text, nullable=False)
    
    # Tracking Information
    submitter_id = Column(String(50))
    receiver_id = Column(String(50))
    interchange_control_number = Column(String(20))
    group_control_number = Column(String(20))
    transaction_control_number = Column(String(20))
    
    # Relationships
    response = relationship("PriorAuthorizationResponse", back_populates="request", uselist=False)
    patient_info = relationship("PatientInformation", back_populates="authorization_requests")


class PriorAuthorizationResponse(Base, TimestampMixin):
    """Model for EDI 278 Prior Authorization Responses"""
    __tablename__ = "prior_authorization_responses"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), ForeignKey("prior_authorization_requests.request_id"), nullable=False)
    
    # Response Details
    response_code = Column(SQLEnum(ResponseCodeEnum), nullable=False)
    authorization_number = Column(String(50), index=True)
    effective_date = Column(Date)
    expiration_date = Column(Date)
    
    # Approved Services
    approved_services = Column(JSON)  # Details of approved services
    units_approved = Column(Integer)
    units_used = Column(Integer, default=0)
    
    # Decision Information
    decision_reason = Column(Text)
    reviewer_name = Column(String(255))
    review_date = Column(DateTime)
    
    # Additional Requirements
    additional_information_required = Column(Text)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(Date)
    
    # EDI Content
    edi_278_response_content = Column(Text, nullable=False)
    
    # Processing Information
    processing_time_ms = Column(Integer)
    payer_id = Column(String(50))
    payer_name = Column(String(255))
    
    # Relationships
    request = relationship("PriorAuthorizationRequest", back_populates="response")


class PatientInformation(Base, TimestampMixin):
    """Model for EDI 275 Patient Information"""
    __tablename__ = "patient_information"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Demographics
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(1))  # M, F, U
    ssn = Column(String(11))  # Encrypted in production
    
    # Contact Information
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(10))
    zip_code = Column(String(20))
    phone_home = Column(String(20))
    phone_work = Column(String(20))
    phone_mobile = Column(String(20))
    email = Column(String(255))
    
    # Insurance Information
    primary_insurance = Column(JSON)  # Primary insurance details
    secondary_insurance = Column(JSON)  # Secondary insurance details
    member_id_primary = Column(String(100), index=True)
    member_id_secondary = Column(String(100))
    
    # Emergency Contact
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relationship = Column(String(50))
    
    # Medical Information
    primary_care_provider = Column(String(255))
    allergies = Column(JSON)  # Array of allergy information
    medical_conditions = Column(JSON)  # Array of conditions
    medications = Column(JSON)  # Array of current medications
    
    # EDI 275 Information
    edi_275_content = Column(Text)
    last_edi_update = Column(DateTime)
    
    # Consent and Privacy
    hipaa_authorization = Column(Boolean, default=False)
    consent_date = Column(DateTime)
    privacy_preferences = Column(JSON)
    
    # Relationships
    authorization_requests = relationship("PriorAuthorizationRequest", back_populates="patient_info")


class ServiceTypeCode(Base, TimestampMixin):
    """Model for Healthcare Service Type Codes"""
    __tablename__ = "service_type_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=False)
    category = Column(String(100))  # Medical, Surgical, etc.
    requires_authorization = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)


class ProcedureCode(Base, TimestampMixin):
    """Model for CPT/HCPCS Procedure Codes"""
    __tablename__ = "procedure_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=False)
    code_type = Column(String(10))  # CPT, HCPCS
    category = Column(String(100))
    requires_authorization = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class DiagnosisCode(Base, TimestampMixin):
    """Model for ICD-10 Diagnosis Codes"""
    __tablename__ = "diagnosis_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=False)
    category = Column(String(100))
    is_active = Column(Boolean, default=True)


class AuthorizationAudit(Base, TimestampMixin):
    """Model for Authorization Audit Trail"""
    __tablename__ = "authorization_audit"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False)  # submitted, reviewed, approved, etc.
    actor = Column(String(255))  # User who performed action
    notes = Column(Text)
    previous_status = Column(String(20))
    new_status = Column(String(20))
    action_metadata = Column(JSON)  # Additional action metadata

# File: app/schemas/prior_authorization.py - Pydantic Schemas
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator
from datetime import datetime, date
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
    code: str
    description: Optional[str] = None
    modifier: Optional[str] = None
    units: Optional[int] = 1


class DiagnosisCodeInfo(BaseModel):
    code: str
    description: Optional[str] = None
    is_primary: bool = False


class PriorAuthorizationRequestBase(BaseModel):
    # Patient Information
    patient_first_name: str
    patient_last_name: str
    patient_dob: date
    patient_gender: Gender
    member_id: str
    
    # Provider Information
    requesting_provider_npi: str
    requesting_provider_name: Optional[str] = None
    servicing_provider_npi: Optional[str] = None
    servicing_provider_name: Optional[str] = None
    
    # Authorization Details
    request_type: RequestType = RequestType.INITIAL
    certification_type: CertificationType = CertificationType.INITIAL
    service_type_code: Optional[str] = None
    
    # Service Information
    procedure_codes: List[ProcedureCodeInfo]
    diagnosis_codes: List[DiagnosisCodeInfo]
    service_date_from: date
    service_date_to: Optional[date] = None
    units_requested: Optional[int] = 1
    
    # Clinical Information
    clinical_information: Optional[str] = None
    medical_necessity: str
    
    # Priority
    priority: Priority = Priority.NORMAL
    
    @field_validator('requesting_provider_npi')
    @classmethod
    def validate_npi(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('NPI must be exactly 10 digits')
        return v


class PriorAuthorizationRequestCreate(PriorAuthorizationRequestBase):
    pass


class PriorAuthorizationRequest(PriorAuthorizationRequestBase):
    id: int
    request_id: str
    patient_id: str
    status: str
    edi_278_content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AuthorizationDecision(BaseModel):
    response_code: ResponseCode
    authorization_number: Optional[str] = None
    effective_date: Optional[date] = None
    expiration_date: Optional[date] = None
    units_approved: Optional[int] = None
    decision_reason: Optional[str] = None
    additional_information_required: Optional[str] = None


class PriorAuthorizationResponse(BaseModel):
    id: int
    request_id: str
    response_code: ResponseCode
    authorization_number: Optional[str] = None
    effective_date: Optional[date] = None
    expiration_date: Optional[date] = None
    approved_services: Optional[Dict[str, Any]] = None
    units_approved: Optional[int] = None
    decision_reason: Optional[str] = None
    edi_278_response_content: str
    processing_time_ms: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PriorAuthorizationInquiryResponse(BaseModel):
    request_id: str
    edi_278: str
    status: str
    message: str


class PriorAuthorizationDecisionResponse(BaseModel):
    request_id: str
    edi_278_response: str
    response_code: ResponseCode
    authorization_number: Optional[str] = None
    decision_details: Optional[Dict[str, Any]] = None
    processed_at: datetime

# File: app/schemas/patient_information.py - EDI 275 Schemas
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime, date


class InsuranceInfo(BaseModel):
    carrier_name: str
    policy_number: str
    group_number: Optional[str] = None
    effective_date: Optional[date] = None
    copay_amount: Optional[float] = None
    deductible_amount: Optional[float] = None


class EmergencyContact(BaseModel):
    name: str
    phone: str
    relationship: str


class AllergyInfo(BaseModel):
    allergen: str
    reaction: Optional[str] = None
    severity: Optional[str] = None


class MedicalCondition(BaseModel):
    condition: str
    icd_code: Optional[str] = None
    date_diagnosed: Optional[date] = None
    status: Optional[str] = None  # active, inactive, resolved


class Medication(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    prescribing_physician: Optional[str] = None


class PatientInformationBase(BaseModel):
    # Demographics
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    date_of_birth: date
    gender: Gender
    ssn: Optional[str] = None
    
    # Contact Information
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone_home: Optional[str] = None
    phone_work: Optional[str] = None
    phone_mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    
    # Insurance Information
    primary_insurance: Optional[InsuranceInfo] = None
    secondary_insurance: Optional[InsuranceInfo] = None
    member_id_primary: Optional[str] = None
    member_id_secondary: Optional[str] = None
    
    # Emergency Contact
    emergency_contact: Optional[EmergencyContact] = None
    
    # Medical Information
    primary_care_provider: Optional[str] = None
    allergies: Optional[List[AllergyInfo]] = None
    medical_conditions: Optional[List[MedicalCondition]] = None
    medications: Optional[List[Medication]] = None
    
    # Consent
    hipaa_authorization: bool = False
    consent_date: Optional[datetime] = None


class PatientInformationCreate(PatientInformationBase):
    pass


class PatientInformationUpdate(BaseModel):
    # All fields optional for updates
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone_home: Optional[str] = None
    phone_work: Optional[str] = None
    phone_mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    primary_insurance: Optional[InsuranceInfo] = None
    secondary_insurance: Optional[InsuranceInfo] = None
    emergency_contact: Optional[EmergencyContact] = None
    allergies: Optional[List[AllergyInfo]] = None
    medical_conditions: Optional[List[MedicalCondition]] = None
    medications: Optional[List[Medication]] = None


class PatientInformation(PatientInformationBase):
    id: int
    patient_id: str
    edi_275_content: Optional[str] = None
    last_edi_update: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PatientEDI275Response(BaseModel):
    patient_id: str
    edi_275: str
    message: str
    generated_at: datetime

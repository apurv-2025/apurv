# File: app/schemas/patient_information.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator, EmailStr, Field
from datetime import datetime, date
from enum import Enum


class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"
    UNKNOWN = "U"


class InsuranceInfo(BaseModel):
    """Insurance information schema"""
    carrier_name: str = Field(..., min_length=1, max_length=255)
    policy_number: str = Field(..., min_length=1, max_length=100)
    group_number: Optional[str] = Field(None, max_length=100)
    effective_date: Optional[date] = None
    expiration_date: Optional[date] = None
    copay_amount: Optional[float] = Field(None, ge=0)
    deductible_amount: Optional[float] = Field(None, ge=0)
    coverage_type: Optional[str] = Field(None, max_length=50)
    
    @field_validator('copay_amount', 'deductible_amount')
    @classmethod
    def validate_amounts(cls, v):
        if v is not None and v < 0:
            raise ValueError('Amount must be non-negative')
        return v


class EmergencyContact(BaseModel):
    """Emergency contact information"""
    name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=10, max_length=20)
    relationship: str = Field(..., min_length=1, max_length=50)
    address: Optional[str] = Field(None, max_length=500)
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        # Remove non-digit characters for validation
        digits_only = ''.join(filter(str.isdigit, v))
        if len(digits_only) < 10:
            raise ValueError('Phone number must contain at least 10 digits')
        return v


class AllergyInfo(BaseModel):
    """Allergy information"""
    allergen: str = Field(..., min_length=1, max_length=255)
    reaction: Optional[str] = Field(None, max_length=500)
    severity: Optional[str] = Field(None, max_length=50)
    date_identified: Optional[date] = None
    status: Optional[str] = Field("active", max_length=20)  # active, inactive, resolved
    notes: Optional[str] = Field(None, max_length=1000)


class MedicalCondition(BaseModel):
    """Medical condition information"""
    condition: str = Field(..., min_length=1, max_length=255)
    icd_code: Optional[str] = Field(None, max_length=20)
    date_diagnosed: Optional[date] = None
    status: Optional[str] = Field("active", max_length=20)  # active, inactive, resolved
    severity: Optional[str] = Field(None, max_length=50)
    treating_physician: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = Field(None, max_length=1000)


class Medication(BaseModel):
    """Medication information"""
    name: str = Field(..., min_length=1, max_length=255)
    dosage: Optional[str] = Field(None, max_length=100)
    frequency: Optional[str] = Field(None, max_length=100)
    route: Optional[str] = Field(None, max_length=50)  # oral, IV, etc.
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    prescribing_physician: Optional[str] = Field(None, max_length=255)
    ndc_code: Optional[str] = Field(None, max_length=20)  # National Drug Code
    status: Optional[str] = Field("active", max_length=20)  # active, discontinued
    notes: Optional[str] = Field(None, max_length=1000)


class PatientInformationBase(BaseModel):
    """Base patient information schema"""
    # Demographics
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: date
    gender: Gender
    ssn: Optional[str] = Field(None, min_length=9, max_length=11)
    
    # Contact Information
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=10)
    zip_code: Optional[str] = Field(None, max_length=20)
    phone_home: Optional[str] = Field(None, max_length=20)
    phone_work: Optional[str] = Field(None, max_length=20)
    phone_mobile: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    
    # Insurance Information
    primary_insurance: Optional[InsuranceInfo] = None
    secondary_insurance: Optional[InsuranceInfo] = None
    member_id_primary: Optional[str] = Field(None, max_length=100)
    member_id_secondary: Optional[str] = Field(None, max_length=100)
    
    # Emergency Contact
    emergency_contact: Optional[EmergencyContact] = None
    
    # Medical Information
    primary_care_provider: Optional[str] = Field(None, max_length=255)
    allergies: Optional[List[AllergyInfo]] = None
    medical_conditions: Optional[List[MedicalCondition]] = None
    medications: Optional[List[Medication]] = None
    
    # Consent
    hipaa_authorization: bool = False
    consent_date: Optional[datetime] = None
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_dob(cls, v):
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        if v < date(1900, 1, 1):
            raise ValueError('Date of birth cannot be before 1900')
        return v
    
    @field_validator('ssn')
    @classmethod
    def validate_ssn(cls, v):
        if v is not None:
            # Remove non-digit characters
            digits_only = ''.join(filter(str.isdigit, v))
            if len(digits_only) != 9:
                raise ValueError('SSN must contain exactly 9 digits')
        return v


class PatientInformationCreate(PatientInformationBase):
    """Schema for creating a new patient"""
    # All fields from base, no additional requirements
    pass


class PatientInformationUpdate(BaseModel):
    """Schema for updating patient information"""
    # All fields optional for updates
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    ssn: Optional[str] = Field(None, min_length=9, max_length=11)
    
    # Contact Information
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=10)
    zip_code: Optional[str] = Field(None, max_length=20)
    phone_home: Optional[str] = Field(None, max_length=20)
    phone_work: Optional[str] = Field(None, max_length=20)
    phone_mobile: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    
    # Insurance Information
    primary_insurance: Optional[InsuranceInfo] = None
    secondary_insurance: Optional[InsuranceInfo] = None
    member_id_primary: Optional[str] = Field(None, max_length=100)
    member_id_secondary: Optional[str] = Field(None, max_length=100)
    
    # Emergency Contact
    emergency_contact: Optional[EmergencyContact] = None
    
    # Medical Information
    primary_care_provider: Optional[str] = Field(None, max_length=255)
    allergies: Optional[List[AllergyInfo]] = None
    medical_conditions: Optional[List[MedicalCondition]] = None
    medications: Optional[List[Medication]] = None
    
    # Consent
    hipaa_authorization: Optional[bool] = None
    consent_date: Optional[datetime] = None


class PatientInformation(PatientInformationBase):
    """Complete patient information schema with database fields"""
    id: int
    patient_id: str
    edi_275_content: Optional[str] = None
    last_edi_update: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PatientEDI275Response(BaseModel):
    """EDI 275 response schema"""
    patient_id: str
    edi_275: str
    message: str
    generated_at: datetime
    control_number: Optional[str] = None
    status: str = "generated"


class PatientSearchRequest(BaseModel):
    """Patient search request schema"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    member_id: Optional[str] = Field(None, max_length=100)
    ssn: Optional[str] = Field(None, min_length=9, max_length=11)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None


class PatientSummary(BaseModel):
    """Patient summary for lists"""
    id: int
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    member_id_primary: Optional[str] = None
    phone_mobile: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}



# Patient Information Schemas
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from enum import Enum


class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"
    UNKNOWN = "U"


class InsuranceInfo(BaseModel):
    carrier_name: str = Field(..., description="Insurance carrier name")
    policy_number: str = Field(..., description="Policy number")
    group_number: Optional[str] = Field(None, description="Group number")
    effective_date: Optional[date] = Field(None, description="Effective date")
    copay_amount: Optional[float] = Field(None, description="Copay amount")
    deductible_amount: Optional[float] = Field(None, description="Deductible amount")


class EmergencyContact(BaseModel):
    name: str = Field(..., description="Emergency contact name")
    phone: str = Field(..., description="Emergency contact phone")
    relationship: str = Field(..., description="Relationship to patient")


class AllergyInfo(BaseModel):
    allergen: str = Field(..., description="Allergen name")
    reaction: Optional[str] = Field(None, description="Allergic reaction")
    severity: Optional[str] = Field(None, description="Reaction severity")


class MedicalCondition(BaseModel):
    condition: str = Field(..., description="Medical condition")
    icd_code: Optional[str] = Field(None, description="ICD-10 code")
    date_diagnosed: Optional[date] = Field(None, description="Date diagnosed")
    status: Optional[str] = Field(None, description="Condition status")


class Medication(BaseModel):
    name: str = Field(..., description="Medication name")
    dosage: Optional[str] = Field(None, description="Dosage")
    frequency: Optional[str] = Field(None, description="Frequency")
    prescribing_physician: Optional[str] = Field(None, description="Prescribing physician")


class PatientInformationBase(BaseModel):
    # Demographics
    first_name: str = Field(..., description="Patient first name")
    last_name: str = Field(..., description="Patient last name")
    middle_name: Optional[str] = Field(None, description="Patient middle name")
    date_of_birth: date = Field(..., description="Date of birth")
    gender: Gender = Field(..., description="Gender")
    ssn: Optional[str] = Field(None, description="Social Security Number")
    
    # Contact Information
    address_line1: Optional[str] = Field(None, description="Address line 1")
    address_line2: Optional[str] = Field(None, description="Address line 2")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    zip_code: Optional[str] = Field(None, description="ZIP code")
    phone_home: Optional[str] = Field(None, description="Home phone")
    phone_work: Optional[str] = Field(None, description="Work phone")
    phone_mobile: Optional[str] = Field(None, description="Mobile phone")
    email: Optional[EmailStr] = Field(None, description="Email address")
    
    # Insurance Information
    primary_insurance: Optional[InsuranceInfo] = Field(None, description="Primary insurance")
    secondary_insurance: Optional[InsuranceInfo] = Field(None, description="Secondary insurance")
    member_id_primary: Optional[str] = Field(None, description="Primary member ID")
    member_id_secondary: Optional[str] = Field(None, description="Secondary member ID")
    
    # Emergency Contact
    emergency_contact: Optional[EmergencyContact] = Field(None, description="Emergency contact")
    
    # Medical Information
    primary_care_provider: Optional[str] = Field(None, description="Primary care provider")
    allergies: Optional[List[AllergyInfo]] = Field(None, description="Allergies")
    medical_conditions: Optional[List[MedicalCondition]] = Field(None, description="Medical conditions")
    medications: Optional[List[Medication]] = Field(None, description="Current medications")
    
    # Consent
    hipaa_authorization: bool = Field(False, description="HIPAA authorization")
    consent_date: Optional[datetime] = Field(None, description="Consent date")


class PatientInformationCreate(PatientInformationBase):
    pass


class PatientInformationUpdate(BaseModel):
    # All fields optional for updates
    first_name: Optional[str] = Field(None, description="Patient first name")
    last_name: Optional[str] = Field(None, description="Patient last name")
    middle_name: Optional[str] = Field(None, description="Patient middle name")
    address_line1: Optional[str] = Field(None, description="Address line 1")
    address_line2: Optional[str] = Field(None, description="Address line 2")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    zip_code: Optional[str] = Field(None, description="ZIP code")
    phone_home: Optional[str] = Field(None, description="Home phone")
    phone_work: Optional[str] = Field(None, description="Work phone")
    phone_mobile: Optional[str] = Field(None, description="Mobile phone")
    email: Optional[EmailStr] = Field(None, description="Email address")
    primary_insurance: Optional[InsuranceInfo] = Field(None, description="Primary insurance")
    secondary_insurance: Optional[InsuranceInfo] = Field(None, description="Secondary insurance")
    emergency_contact: Optional[EmergencyContact] = Field(None, description="Emergency contact")
    allergies: Optional[List[AllergyInfo]] = Field(None, description="Allergies")
    medical_conditions: Optional[List[MedicalCondition]] = Field(None, description="Medical conditions")
    medications: Optional[List[Medication]] = Field(None, description="Current medications")


class PatientInformation(PatientInformationBase):
    id: int = Field(..., description="Patient ID")
    patient_id: str = Field(..., description="Unique patient identifier")
    edi_275_content: Optional[str] = Field(None, description="EDI 275 content")
    last_edi_update: Optional[datetime] = Field(None, description="Last EDI update")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    model_config = {"from_attributes": True}


class PatientEDI275Response(BaseModel):
    patient_id: str = Field(..., description="Patient ID")
    edi_275: str = Field(..., description="EDI 275 content")
    message: str = Field(..., description="Response message")
    generated_at: datetime = Field(..., description="Generation timestamp")


class PatientSummary(BaseModel):
    """Patient summary for lists"""
    id: int = Field(..., description="Patient ID")
    patient_id: str = Field(..., description="Unique patient identifier")
    first_name: str = Field(..., description="Patient first name")
    last_name: str = Field(..., description="Patient last name")
    date_of_birth: date = Field(..., description="Date of birth")
    gender: Gender = Field(..., description="Gender")
    member_id_primary: Optional[str] = Field(None, description="Primary member ID")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = {"from_attributes": True}


class PatientSearchRequest(BaseModel):
    """Patient search request schema"""
    first_name: Optional[str] = Field(None, description="Patient first name")
    last_name: Optional[str] = Field(None, description="Patient last name")
    member_id: Optional[str] = Field(None, description="Member ID")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    limit: int = Field(10, description="Maximum number of results")
    offset: int = Field(0, description="Number of results to skip")


class PatientStatistics(BaseModel):
    """Patient-specific statistics"""
    patient_id: str = Field(..., description="Patient ID")
    patient_name: str = Field(..., description="Patient name")
    total_requests: int = Field(..., description="Total requests for this patient")
    approved_requests: int = Field(..., description="Approved requests for this patient")
    denied_requests: int = Field(..., description="Denied requests for this patient")
    approval_rate: float = Field(..., description="Patient approval rate")
    total_units_requested: int = Field(..., description="Total units requested")
    total_units_approved: int = Field(..., description="Total units approved")
    last_request_date: Optional[date] = Field(None, description="Date of last request")



# schemas.py
from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
import uuid

# Base schemas
class ChargeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    cpt_code: str = Field(..., max_length=10)
    cpt_description: Optional[str] = Field(None, max_length=255)
    icd_code: str = Field(..., max_length=10)
    icd_description: Optional[str] = Field(None, max_length=255)
    hcpcs_code: Optional[str] = Field(None, max_length=10)
    modifiers: Optional[List[str]] = []
    units: int = Field(default=1, ge=1)
    quantity: int = Field(default=1, ge=1)
    charge_amount: Optional[Decimal] = Field(None)

class ChargeCreate(ChargeBase):
    encounter_id: uuid.UUID
    patient_id: uuid.UUID
    provider_id: uuid.UUID
    capture_method: str = Field(..., pattern="^(point_of_care|post_encounter|batch)$")

class ChargeUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    cpt_code: Optional[str] = Field(None, max_length=10)
    cpt_description: Optional[str] = Field(None, max_length=255)
    icd_code: Optional[str] = Field(None, max_length=10)
    icd_description: Optional[str] = Field(None, max_length=255)
    hcpcs_code: Optional[str] = Field(None, max_length=10)
    modifiers: Optional[List[str]] = None
    units: Optional[int] = Field(None, ge=1)
    quantity: Optional[int] = Field(None, ge=1)
    charge_amount: Optional[Decimal] = Field(None)
    status: Optional[str] = Field(None, pattern="^(draft|submitted|billed|rejected|paid)$")

class ChargeResponse(ChargeBase):
    id: uuid.UUID
    encounter_id: uuid.UUID
    patient_id: uuid.UUID
    provider_id: uuid.UUID
    status: str
    capture_method: str
    captured_at: datetime
    validation_errors: Optional[List[Dict[str, Any]]] = []
    audit_log: Optional[List[Dict[str, Any]]] = []
    created_at: datetime
    updated_at: datetime
    
    # Related data
    patient_name: Optional[str] = None
    provider_name: Optional[str] = None
    encounter_date: Optional[datetime] = None

# Template schemas
class ChargeTemplateBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=100)
    specialty: str = Field(..., max_length=100)
    template_data: Dict[str, Any]

class ChargeTemplateCreate(ChargeTemplateBase):
    provider_id: Optional[uuid.UUID] = None
    is_system_template: bool = False

class ChargeTemplateResponse(ChargeTemplateBase):
    id: uuid.UUID
    provider_id: Optional[uuid.UUID]
    is_active: bool
    is_system_template: bool
    created_at: datetime
    updated_at: datetime

# Encounter schemas
class EncounterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    encounter_date: datetime
    encounter_type: str = Field(..., max_length=50)
    notes: Optional[str] = None

class EncounterCreate(EncounterBase):
    patient_id: uuid.UUID
    provider_id: uuid.UUID

class EncounterResponse(EncounterBase):
    id: uuid.UUID
    patient_id: uuid.UUID
    provider_id: uuid.UUID
    status: str
    patient_name: Optional[str] = None
    provider_name: Optional[str] = None
    charges_count: int = 0
    created_at: datetime

# Patient schemas
class PatientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    date_of_birth: datetime
    mrn: str = Field(..., max_length=50)
    insurance_info: Optional[Dict[str, Any]] = {}

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: uuid.UUID
    created_at: datetime
    full_name: Optional[str] = None

# Provider schemas
class ProviderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    npi: str = Field(..., max_length=10)
    specialty: str = Field(..., max_length=100)

class ProviderCreate(ProviderBase):
    pass

class ProviderResponse(ProviderBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    full_name: Optional[str] = None

# Batch operation schemas
class BatchChargeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    charges: List[ChargeCreate]

class BatchChargeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    success_count: int
    error_count: int
    created_charges: List[ChargeResponse]
    errors: List[Dict[str, Any]]

# Validation schemas
class ValidationError(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    field: str
    message: str
    severity: str = Field(..., pattern="^(error|warning|info)$")

class ChargeValidation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    is_valid: bool
    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

# Search schemas
class ChargeSearchParams(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    patient_id: Optional[uuid.UUID] = None
    provider_id: Optional[uuid.UUID] = None
    encounter_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    cpt_code: Optional[str] = None
    specialty: Optional[str] = None
    page: int = 1
    page_size: int = 20

class ChargeSearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    charges: List[ChargeResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

# Metrics schemas
class ChargeMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    total_charges: int
    total_amount: Decimal
    average_amount: Decimal
    charges_by_status: Dict[str, int]
    charges_by_specialty: Dict[str, int]
    charges_by_month: Dict[str, int]

class ProviderMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    provider_id: uuid.UUID
    provider_name: str
    total_charges: int
    total_amount: Decimal
    average_amount: Decimal
    charges_by_status: Dict[str, int]
    charges_by_month: Dict[str, int]

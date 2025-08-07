# =============================================================================
# FILE: backend/app/schemas/claims.py
# =============================================================================
from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from app.database.models import ClaimType, ClaimStatus, WorkQueueStatus, WorkQueuePriority

class ServiceLineBase(BaseModel):
    line_number: int
    procedure_code: str
    procedure_description: Optional[str] = None
    service_date_from: datetime
    service_date_to: Optional[datetime] = None
    units: int = 1
    charge_amount: Decimal
    diagnosis_code_1: Optional[str] = None
    diagnosis_code_2: Optional[str] = None
    diagnosis_code_3: Optional[str] = None
    diagnosis_code_4: Optional[str] = None

class ServiceLineCreate(ServiceLineBase):
    pass

class ServiceLine(ServiceLineBase):
    id: int
    claim_id: int
    allowed_amount: Optional[Decimal] = None
    paid_amount: Optional[Decimal] = None
    
    class Config:
        from_attributes = True

class DentalDetailBase(BaseModel):
    tooth_number: Optional[str] = None
    tooth_surface: Optional[str] = None
    oral_cavity_area: Optional[str] = None
    treatment_plan_sequence: Optional[int] = None
    months_of_treatment: Optional[int] = None
    prosthetic_replacement: bool = False
    initial_placement_date: Optional[datetime] = None

class DentalDetailCreate(DentalDetailBase):
    pass

class DentalDetail(DentalDetailBase):
    id: int
    claim_id: int
    
    class Config:
        from_attributes = True

class ClaimBase(BaseModel):
    claim_type: ClaimType
    patient_first_name: str
    patient_last_name: str
    patient_dob: datetime
    patient_id: str
    provider_name: str
    provider_npi: str
    provider_taxonomy: Optional[str] = None
    payer_id: int
    total_charge: Decimal

class ClaimCreate(ClaimBase):
    service_lines: List[ServiceLineCreate]
    dental_details: Optional[DentalDetailCreate] = None

class ClaimUpdate(BaseModel):
    status: Optional[ClaimStatus] = None
    validation_errors: Optional[Dict[str, Any]] = None
    allowed_amount: Optional[Decimal] = None
    paid_amount: Optional[Decimal] = None
    patient_responsibility: Optional[Decimal] = None

class Claim(ClaimBase):
    id: int
    claim_number: str
    status: ClaimStatus
    allowed_amount: Optional[Decimal] = None
    paid_amount: Optional[Decimal] = None
    patient_responsibility: Optional[Decimal] = None
    validation_errors: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    service_lines: List[ServiceLine] = []
    dental_details: Optional[DentalDetail] = None
    
    class Config:
        from_attributes = True

class PayerBase(BaseModel):
    name: str
    payer_id: str
    address: Optional[str] = None
    contact_info: Optional[Dict[str, Any]] = None
    companion_guide_url: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None
    transmission_method: str = "FTP"

class PayerCreate(PayerBase):
    pass

class Payer(PayerBase):
    id: int
    is_active: bool
    certification_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Work Queue Schemas
class WorkQueueAssignment(BaseModel):
    assigned_to: str
    priority: WorkQueuePriority = WorkQueuePriority.MEDIUM
    estimated_completion: Optional[datetime] = None
    work_notes: Optional[str] = None

class WorkQueueUpdate(BaseModel):
    status: Optional[WorkQueueStatus] = None
    priority: Optional[WorkQueuePriority] = None
    estimated_completion: Optional[datetime] = None
    work_notes: Optional[str] = None
    action_taken: Optional[str] = None
    result_summary: Optional[str] = None

class WorkQueueItem(BaseModel):
    id: int
    claim_id: int
    claim_number: str
    patient_name: str
    claim_type: ClaimType
    claim_status: ClaimStatus
    assigned_by: str
    assigned_to: str
    assigned_at: datetime
    status: WorkQueueStatus
    priority: WorkQueuePriority
    estimated_completion: Optional[datetime] = None
    actual_completion: Optional[datetime] = None
    work_notes: Optional[str] = None
    action_taken: Optional[str] = None
    result_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class WorkQueueSummary(BaseModel):
    total_items: int
    pending: int
    assigned: int
    in_progress: int
    completed: int
    failed: int
    cancelled: int
    by_priority: Dict[str, int]
    by_assignee: Dict[str, int]


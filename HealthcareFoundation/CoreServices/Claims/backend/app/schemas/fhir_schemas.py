# schemas/fhir_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    active = "active"
    cancelled = "cancelled"
    draft = "draft"
    entered_in_error = "entered-in-error"

class UseEnum(str, Enum):
    claim = "claim"
    preauthorization = "preauthorization"
    predetermination = "predetermination"

class OutcomeEnum(str, Enum):
    queued = "queued"
    complete = "complete"
    error = "error"
    partial = "partial"

# Base schemas
class CodeableConcept(BaseModel):
    coding: Optional[List[Dict[str, Any]]] = None
    text: Optional[str] = None

class Identifier(BaseModel):
    use: Optional[str] = None
    type: Optional[CodeableConcept] = None
    system: Optional[str] = None
    value: Optional[str] = None
    period: Optional[Dict[str, Any]] = None

class Money(BaseModel):
    value: Optional[float] = None
    currency: Optional[str] = None

class Period(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None

# Claim schemas
class ClaimBase(BaseModel):
    identifier: Optional[List[Identifier]] = None
    trace_number: Optional[List[Identifier]] = None
    status: StatusEnum
    type: CodeableConcept
    sub_type: Optional[CodeableConcept] = None
    use: UseEnum
    patient_id: str
    billable_period: Optional[Period] = None
    enterer_id: Optional[str] = None
    insurer_id: str
    provider_id: str
    priority: Optional[CodeableConcept] = None
    funds_reserve: Optional[CodeableConcept] = None
    related: Optional[List[Dict[str, Any]]] = None
    prescription_id: Optional[str] = None
    original_prescription_id: Optional[str] = None
    payee: Optional[Dict[str, Any]] = None
    referral_id: Optional[str] = None
    encounter: Optional[List[str]] = None
    facility_id: Optional[str] = None
    diagnosis_related_group: Optional[CodeableConcept] = None
    event: Optional[List[Dict[str, Any]]] = None
    care_team: Optional[List[Dict[str, Any]]] = None
    supporting_info: Optional[List[Dict[str, Any]]] = None
    diagnosis: Optional[List[Dict[str, Any]]] = None
    procedure: Optional[List[Dict[str, Any]]] = None
    insurance: List[Dict[str, Any]]
    accident: Optional[Dict[str, Any]] = None
    patient_paid: Optional[Money] = None
    item: Optional[List[Dict[str, Any]]] = None
    total: Optional[Money] = None

class ClaimCreate(ClaimBase):
    pass

class ClaimUpdate(BaseModel):
    identifier: Optional[List[Identifier]] = None
    status: Optional[StatusEnum] = None
    type: Optional[CodeableConcept] = None
    sub_type: Optional[CodeableConcept] = None
    use: Optional[UseEnum] = None
    patient_id: Optional[str] = None
    insurer_id: Optional[str] = None
    provider_id: Optional[str] = None
    insurance: Optional[List[Dict[str, Any]]] = None
    # Add other optional fields as needed

class ClaimResponse(ClaimBase):
    id: str
    resource_type: str = "Claim"
    created: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ClaimResponse schemas
class ClaimResponseBase(BaseModel):
    identifier: Optional[List[Identifier]] = None
    trace_number: Optional[List[Identifier]] = None
    status: StatusEnum
    type: CodeableConcept
    sub_type: Optional[CodeableConcept] = None
    use: UseEnum
    patient_id: str
    insurer_id: str
    requestor_id: Optional[str] = None
    request_id: Optional[str] = None
    outcome: OutcomeEnum
    decision: Optional[CodeableConcept] = None
    disposition: Optional[str] = None
    pre_auth_ref: Optional[str] = None
    pre_auth_period: Optional[Period] = None
    event: Optional[List[Dict[str, Any]]] = None
    payee_type: Optional[CodeableConcept] = None
    encounter: Optional[List[str]] = None
    diagnosis_related_group: Optional[CodeableConcept] = None
    item: Optional[List[Dict[str, Any]]] = None
    add_item: Optional[List[Dict[str, Any]]] = None
    adjudication: Optional[List[Dict[str, Any]]] = None
    total: Optional[List[Dict[str, Any]]] = None
    payment: Optional[Dict[str, Any]] = None
    funds_reserve: Optional[CodeableConcept] = None
    form_code: Optional[CodeableConcept] = None
    form: Optional[Dict[str, Any]] = None
    process_note: Optional[List[Dict[str, Any]]] = None
    communication_request: Optional[List[str]] = None
    insurance: Optional[List[Dict[str, Any]]] = None
    error: Optional[List[Dict[str, Any]]] = None

class ClaimResponseCreate(ClaimResponseBase):
    pass

class ClaimResponseUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    outcome: Optional[OutcomeEnum] = None
    decision: Optional[CodeableConcept] = None
    disposition: Optional[str] = None
    # Add other optional fields

class ClaimResponseResponse(ClaimResponseBase):
    id: str
    resource_type: str = "ClaimResponse"
    created: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Coverage schemas
class CoverageBase(BaseModel):
    identifier: Optional[List[Identifier]] = None
    status: StatusEnum
    kind: Optional[str] = None
    payment_by: Optional[List[Dict[str, Any]]] = None
    type: Optional[CodeableConcept] = None
    policy_holder_id: Optional[str] = None
    subscriber_id_ref: Optional[str] = None
    subscriber_id: Optional[List[Dict[str, Any]]] = None
    beneficiary_id: str
    dependent: Optional[str] = None
    relationship: Optional[CodeableConcept] = None
    period: Optional[Period] = None
    insurer_id: str
    class_info: Optional[List[Dict[str, Any]]] = None
    order: Optional[int] = None
    network: Optional[str] = None
    cost_to_beneficiary: Optional[List[Dict[str, Any]]] = None
    subrogation: Optional[bool] = None
    contract: Optional[List[str]] = None

class CoverageCreate(CoverageBase):
    pass

class CoverageUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    beneficiary_id: Optional[str] = None
    insurer_id: Optional[str] = None
    # Add other optional fields

class CoverageResponse(CoverageBase):
    id: str
    resource_type: str = "Coverage"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

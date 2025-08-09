# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    CLINICIAN = "clinician"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"
    BILLING_STAFF = "billing_staff"

class NoteType(str, Enum):
    SOAP = "SOAP"
    DAP = "DAP"
    BIRP = "BIRP"
    PAIP = "PAIP"
    CUSTOM = "Custom"

class AuditAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    SIGN = "sign"
    UNLOCK = "unlock"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    license_number: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    license_number: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Patient schemas
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    medical_record_number: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    is_active: bool = True

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    is_active: Optional[bool] = None

class PatientResponse(PatientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Note Template schemas
class NoteTemplateBase(BaseModel):
    name: str
    template_type: NoteType
    structure: Dict[str, Any]
    is_system_template: bool = False
    is_active: bool = True

class NoteTemplateCreate(NoteTemplateBase):
    pass

class NoteTemplateUpdate(BaseModel):
    name: Optional[str] = None
    template_type: Optional[NoteType] = None
    structure: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class NoteTemplateResponse(NoteTemplateBase):
    id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Progress Note schemas
class ProgressNoteBase(BaseModel):
    patient_id: UUID
    template_id: Optional[UUID] = None
    note_type: NoteType
    session_date: datetime
    content: Dict[str, Any]

class ProgressNoteCreate(ProgressNoteBase):
    pass

class ProgressNoteUpdate(BaseModel):
    template_id: Optional[UUID] = None
    note_type: Optional[NoteType] = None
    session_date: Optional[datetime] = None
    content: Optional[Dict[str, Any]] = None

class ProgressNoteDraftSave(BaseModel):
    content: Dict[str, Any]

class ProgressNoteSign(BaseModel):
    digital_signature: Optional[str] = None

class ProgressNoteUnlock(BaseModel):
    unlock_reason: str

class ProgressNoteResponse(ProgressNoteBase):
    id: UUID
    clinician_id: UUID
    is_draft: bool
    is_signed: bool
    signed_at: Optional[datetime] = None
    signed_by: Optional[UUID] = None
    digital_signature: Optional[str] = None
    is_locked: bool
    locked_by: Optional[UUID] = None
    locked_at: Optional[datetime] = None
    unlock_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    version: int
    
    # Related data
    patient: Optional[PatientResponse] = None
    clinician: Optional[UserResponse] = None
    template: Optional[NoteTemplateResponse] = None

    class Config:
        from_attributes = True

# Note Attachment schemas
class NoteAttachmentBase(BaseModel):
    file_name: str
    file_size: int
    mime_type: str

class NoteAttachmentResponse(NoteAttachmentBase):
    id: UUID
    note_id: UUID
    file_path: str
    uploaded_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Audit Log schemas
class AuditLogResponse(BaseModel):
    id: UUID
    user_id: UUID
    action: AuditAction
    resource_type: str
    resource_id: UUID
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime
    
    # Related data
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Search and filter schemas
class ProgressNoteFilters(BaseModel):
    patient_id: Optional[UUID] = None
    clinician_id: Optional[UUID] = None
    note_type: Optional[NoteType] = None
    is_draft: Optional[bool] = None
    is_signed: Optional[bool] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    search_query: Optional[str] = None
    page: int = 1
    page_size: int = 20

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    
# Dashboard schemas
class DashboardStats(BaseModel):
    total_notes: int
    draft_notes: int
    signed_notes: int
    notes_this_week: int
    notes_this_month: int
    recent_notes: List[ProgressNoteResponse]

# Patient assignment schemas
class PatientClinicianBase(BaseModel):
    patient_id: UUID
    clinician_id: UUID
    is_primary: bool = False

class PatientClinicianCreate(PatientClinicianBase):
    pass

class PatientClinicianResponse(PatientClinicianBase):
    id: UUID
    assigned_at: datetime
    patient: Optional[PatientResponse] = None
    clinician: Optional[UserResponse] = None

    class Config:
        from_attributes = True

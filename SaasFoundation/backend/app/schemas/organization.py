from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
import uuid

from app.schemas.user import UserResponse

class OrganizationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Organization name cannot be empty')
        if len(v.strip()) < 2:
            raise ValueError('Organization name must be at least 2 characters long')
        return v.strip()

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Organization name cannot be empty')
        if v is not None and len(v.strip()) < 2:
            raise ValueError('Organization name must be at least 2 characters long')
        return v.strip() if v else v

class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: Optional[str]
    owner_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class MemberResponse(BaseModel):
    id: uuid.UUID
    user: UserResponse
    role: str
    status: str
    joined_at: datetime
    
    class Config:
        from_attributes = True

# Define all available roles
HEALTHCARE_ROLES = [
    # Management Roles
    'owner',
    'admin',
    'Revenue Cycle Manager',
    'Compliance Officer',
    'RCM Analyst',
    'RCM Systems Analyst',
    'Practice Manager',
    
    # Specialist Roles
    'Insurance Verification Specialist',
    'Pre-Authorization Specialist',
    'Financial Counselor',
    'Registration Clerk',
    'Medical Coder',
    'Clinical Documentation Specialist',
    'Charge Entry Specialist',
    'Billing Specialist / Medical Biller',
    'Accounts Receivable (A/R) Specialist',
    'Payment Poster',
    'Denials Management Specialist',
    'Patient Collections Representative',
    'Scheduler',
    'Health Information Technician',
    
    # Legacy roles for backward compatibility
    'member'
]

# Management roles that have administrative privileges
MANAGEMENT_ROLES = [
    'owner',
    'admin',
    'Revenue Cycle Manager',
    'Compliance Officer',
    'RCM Analyst',
    'RCM Systems Analyst',
    'Practice Manager'
]

def is_management_role(role: str) -> bool:
    """Check if a role has management privileges"""
    return role in MANAGEMENT_ROLES

class MemberUpdate(BaseModel):
    role: str

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in HEALTHCARE_ROLES:
            raise ValueError(f'Role must be one of: {", ".join(HEALTHCARE_ROLES)}')
        return v

class InvitationCreate(BaseModel):
    email: str
    message: str = ''
    role: str = 'member'
    send_welcome_email:bool = True
    
    @field_validator('role')
    def validate_role(cls, v):
        if v not in HEALTHCARE_ROLES:
            raise ValueError(f'Role must be one of: {", ".join(HEALTHCARE_ROLES)}')
        return v

class InvitationResponse(BaseModel):
    id: uuid.UUID
    email: str
    role: str
    invited_by:uuid.UUID
    token: str
    expires_at:datetime
    status:str
    created_at: datetime
    
    class Config:
        from_attributes = True


class InvitationDetailsResponse(BaseModel):
    id: uuid.UUID
    email: str
    role: str
    status: str
    organization: OrganizationResponse
    invited_by: UserResponse
    expires_at: datetime
    created_at: datetime
    user_exists: bool
    
    class Config:
        from_attributes = True

class OrganizationWithRole(BaseModel):
    organization: OrganizationResponse
    current_user_role: str

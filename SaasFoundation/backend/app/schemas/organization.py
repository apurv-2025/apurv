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

class MemberUpdate(BaseModel):
    role: str

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed_roles = ['member', 'admin', 'owner']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v

class InvitationCreate(BaseModel):
    email: str
    message: str = ''
    role: str = 'member'
    send_welcome_email:bool = True
    
    @field_validator('role')
    def validate_role(cls, v):
        allowed_roles = ['member', 'admin', 'owner']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v

class InvitationResponse(BaseModel):
    id: uuid.UUID
    email: str
    role: str
    invited_by:uuid.UUID
    token: str
    expires_at:datetime
    status:str


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

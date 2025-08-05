import re
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, Field
from app.schemas.user import UserResponse 

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class EmailVerify(BaseModel):
    token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse






#Forgot Password Related
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8, max_length=255)
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "token": "abc123def456",
                "password": "NewPassword123"
            }
        }

class TokenVerificationRequest(BaseModel):
    token: str = Field(..., min_length=1, max_length=255)
    
    class Config:
        schema_extra = {
            "example": {
                "token": "abc123def456"
            }
        }

class SuccessResponse(BaseModel):
    message: str
    
class TokenValidationResponse(BaseModel):
    valid: bool
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str
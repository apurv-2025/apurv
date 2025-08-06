from pydantic import BaseModel, EmailStr
from typing import Optional

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialty: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True 
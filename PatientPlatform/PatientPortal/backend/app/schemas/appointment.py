from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .doctor import DoctorResponse

class AppointmentBase(BaseModel):
    appointment_date: datetime
    appointment_type: str
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    doctor_id: int

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    appointment_type: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    patient_id: int
    doctor_id: int
    status: str
    created_at: datetime
    doctor: DoctorResponse

    class Config:
        from_attributes = True 
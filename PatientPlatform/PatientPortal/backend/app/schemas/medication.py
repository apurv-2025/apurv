from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from .doctor import DoctorResponse

class MedicationBase(BaseModel):
    name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    instructions: Optional[str] = None

class MedicationCreate(MedicationBase):
    prescriber_id: int
    refills_remaining: int = 0

class MedicationResponse(MedicationBase):
    id: int
    patient_id: int
    prescriber_id: int
    refills_remaining: int
    is_active: bool
    created_at: datetime
    prescriber: DoctorResponse

    class Config:
        from_attributes = True 
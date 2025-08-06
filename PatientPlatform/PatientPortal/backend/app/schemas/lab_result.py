from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from .doctor import DoctorResponse

class LabResultBase(BaseModel):
    test_name: str
    test_date: date
    result_value: Optional[str] = None
    reference_range: Optional[str] = None
    status: str
    notes: Optional[str] = None

class LabResultCreate(LabResultBase):
    ordering_doctor_id: int

class LabResultResponse(LabResultBase):
    id: int
    patient_id: int
    ordering_doctor_id: int
    file_path: Optional[str] = None
    created_at: datetime
    ordering_doctor: DoctorResponse

    class Config:
        from_attributes = True 
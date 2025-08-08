from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime

class PractitionerAvailabilityBase(BaseModel):
    practitioner_id: str
    availability_date: date
    start_time: time
    end_time: time
    notes: Optional[str] = None

class PractitionerAvailabilityCreate(PractitionerAvailabilityBase):
    pass

class PractitionerAvailabilityUpdate(BaseModel):
    availability_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None

class PractitionerAvailabilityResponse(PractitionerAvailabilityBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PractitionerAvailabilityBulkCreate(BaseModel):
    practitioner_id: str
    availabilities: list[dict] = Field(..., description="List of availability objects with date, start_time, end_time")

class AvailableSlotResponse(BaseModel):
    start_time: str
    end_time: str
    available: bool = True
    duration: int 
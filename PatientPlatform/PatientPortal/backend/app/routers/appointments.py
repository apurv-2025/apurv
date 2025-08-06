from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from .. import crud, schemas
from .. import models

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.get("/", response_model=list[schemas.AppointmentResponse])
def read_appointments(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.get_user_appointments(db, user_id=current_user.id)

@router.post("/", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.create_appointment(db=db, appointment=appointment, user_id=current_user.id)

@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(
    appointment_id: int, 
    appointment_update: schemas.AppointmentUpdate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if not appointment or appointment.patient_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.update_appointment(db=db, appointment_id=appointment_id, appointment_update=appointment_update) 
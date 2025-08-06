from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from .. import crud, schemas
from .. import models

router = APIRouter(prefix="/medications", tags=["medications"])

@router.get("/", response_model=list[schemas.MedicationResponse])
def read_medications(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.get_user_medications(db, user_id=current_user.id)

@router.post("/{medication_id}/refill")
def request_refill(
    medication_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    medication = crud.get_medication(db, medication_id=medication_id)
    if not medication or medication.patient_id != current_user.id:
        raise HTTPException(status_code=404, detail="Medication not found")
    return crud.request_medication_refill(db, medication_id=medication_id) 
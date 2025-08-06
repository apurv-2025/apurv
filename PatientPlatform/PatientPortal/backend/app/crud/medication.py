from sqlalchemy.orm import Session
from .. import models

def get_user_medications(db: Session, user_id: int):
    return db.query(models.Medication).filter(
        models.Medication.patient_id == user_id,
        models.Medication.is_active == True
    ).all()

def get_medication(db: Session, medication_id: int):
    return db.query(models.Medication).filter(models.Medication.id == medication_id).first()

def request_medication_refill(db: Session, medication_id: int):
    # This would typically trigger a workflow to notify the doctor
    # For now, we'll just return success
    medication = db.query(models.Medication).filter(models.Medication.id == medication_id).first()
    if medication:
        # In a real application, this would create a refill request
        # and notify the prescribing doctor
        return {"message": "Refill request submitted successfully"}
    return None 
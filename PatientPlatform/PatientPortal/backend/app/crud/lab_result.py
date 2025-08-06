from sqlalchemy.orm import Session
from .. import models

def get_user_lab_results(db: Session, user_id: int):
    return db.query(models.LabResult).filter(models.LabResult.patient_id == user_id).all() 
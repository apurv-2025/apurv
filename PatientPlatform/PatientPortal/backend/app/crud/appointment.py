from sqlalchemy.orm import Session
from .. import models, schemas

def get_user_appointments(db: Session, user_id: int):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == user_id).all()

def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate, user_id: int):
    db_appointment = models.Appointment(
        patient_id=user_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        appointment_type=appointment.appointment_type,
        notes=appointment.notes
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def update_appointment(db: Session, appointment_id: int, appointment_update: schemas.AppointmentUpdate):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return None
    
    update_data = appointment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_appointment, field, value)
    
    db.commit()
    db.refresh(db_appointment)
    return db_appointment 
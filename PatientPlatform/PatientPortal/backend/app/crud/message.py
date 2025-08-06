from sqlalchemy.orm import Session
from .. import models

def get_user_messages(db: Session, user_id: int):
    return db.query(models.Message).filter(models.Message.recipient_id == user_id).all()

def get_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()

def mark_message_read(db: Session, message_id: int):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        message.is_read = True
        db.commit()
        db.refresh(message)
    return message 
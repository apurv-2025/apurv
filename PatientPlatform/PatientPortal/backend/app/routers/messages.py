from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from .. import crud, schemas
from .. import models

router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("/", response_model=list[schemas.MessageResponse])
def read_messages(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.get_user_messages(db, user_id=current_user.id)

@router.put("/{message_id}/read")
def mark_message_read(
    message_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.mark_message_read(db, message_id=message_id) 
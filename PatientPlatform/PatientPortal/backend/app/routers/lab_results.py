from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from .. import crud, schemas
from .. import models

router = APIRouter(prefix="/lab-results", tags=["lab-results"])

@router.get("/", response_model=list[schemas.LabResultResponse])
def read_lab_results(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.get_user_lab_results(db, user_id=current_user.id) 
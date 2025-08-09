# backend/routes/templates.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.schemas import NoteTemplateCreate, NoteTemplateUpdate, NoteTemplateResponse
from app.services import NoteTemplateService
from app.auth import get_current_active_user, require_admin
from app.models import User

router = APIRouter(prefix="/templates", tags=["note-templates"])

@router.post("/", response_model=NoteTemplateResponse)
async def create_template(
    template_create: NoteTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new note template."""
    return NoteTemplateService.create_template(db, template_create, current_user.id)

@router.get("/", response_model=List[NoteTemplateResponse])
async def get_templates(
    template_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get note templates."""
    return NoteTemplateService.get_templates(db, template_type)

@router.get("/{template_id}", response_model=NoteTemplateResponse)
async def get_template(
    template_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get template by ID."""
    template = NoteTemplateService.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return template


from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date

from app.database import get_db
from app.schemas import (
    ProgressNoteCreate, ProgressNoteUpdate, ProgressNoteResponse,
    ProgressNoteDraftSave, ProgressNoteSign, ProgressNoteUnlock,
    ProgressNoteFilters, PaginatedResponse, DashboardStats, NoteType
)
from app.services import ProgressNoteService
from app.auth import get_current_active_user, require_supervisor
from app.models import User

router = APIRouter(prefix="/notes", tags=["progress-notes"])

@router.post("/", response_model=ProgressNoteResponse)
async def create_note(
    note_create: ProgressNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new progress note."""
    return ProgressNoteService.create_note(db, note_create, current_user.id)

@router.get("/", response_model=PaginatedResponse)
async def get_notes(
    patient_id: Optional[UUID] = Query(None),
    note_type: Optional[NoteType] = Query(None),
    is_draft: Optional[bool] = Query(None),
    is_signed: Optional[bool] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    search_query: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get progress notes with filtering and pagination."""
    print("Get progress notes with filtering and pagination.")
    filters = ProgressNoteFilters(
        patient_id=patient_id,
        note_type=note_type,
        is_draft=is_draft,
        is_signed=is_signed,
        date_from=date_from,
        date_to=date_to,
        search_query=search_query,
        page=page,
        page_size=page_size
    )
    
    return ProgressNoteService.get_notes(db, filters, current_user)

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard statistics."""
    return ProgressNoteService.get_dashboard_stats(db, current_user)

@router.get("/{note_id}", response_model=ProgressNoteResponse)
async def get_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get progress note by ID."""
    note = ProgressNoteService.get_note_by_id(db, note_id, current_user)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note

@router.put("/{note_id}", response_model=ProgressNoteResponse)
async def update_note(
    note_id: UUID,
    note_update: ProgressNoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update progress note."""
    note = ProgressNoteService.update_note(db, note_id, note_update, current_user)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )
    
    return note

@router.post("/{note_id}/draft", response_model=ProgressNoteResponse)
async def save_draft(
    note_id: UUID,
    draft_data: ProgressNoteDraftSave,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Save note as draft (auto-save)."""
    note = ProgressNoteService.save_draft(db, note_id, draft_data.content, current_user)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )
    
    return note

@router.post("/{note_id}/sign", response_model=ProgressNoteResponse)
async def sign_note(
    note_id: UUID,
    sign_data: ProgressNoteSign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Sign a progress note."""
    note = ProgressNoteService.sign_note(db, note_id, current_user, sign_data.digital_signature)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )
    
    return note

@router.post("/{note_id}/unlock", response_model=ProgressNoteResponse)
async def unlock_note(
    note_id: UUID,
    unlock_data: ProgressNoteUnlock,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisor)
):
    """Unlock a signed note (supervisor/admin only)."""
    note = ProgressNoteService.unlock_note(db, note_id, unlock_data.unlock_reason, current_user)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


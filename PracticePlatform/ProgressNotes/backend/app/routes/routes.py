# backend/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas import Token, LoginRequest, UserResponse
from app.services import UserService
from app.auth import verify_password, create_access_token, get_current_active_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    user = UserService.get_user_by_email(db, login_data.email)
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

# backend/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..schemas import UserCreate, UserUpdate, UserResponse
from ..services import UserService
from ..auth import get_current_active_user, require_admin
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new user (admin only)."""
    existing_user = UserService.get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return UserService.create_user(db, user_create)

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get list of users (admin only)."""
    return UserService.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID."""
    # Users can view their own profile, admins can view any
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update user."""
    # Users can update their own profile, admins can update any
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = UserService.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

# backend/routes/patients.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..schemas import PatientCreate, PatientUpdate, PatientResponse
from ..services import PatientService
from ..auth import get_current_active_user
from ..models import User

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientResponse)
async def create_patient(
    patient_create: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new patient."""
    return PatientService.create_patient(db, patient_create)

@router.get("/", response_model=List[PatientResponse])
async def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of patients."""
    if current_user.role == "clinician":
        return PatientService.get_patients_for_clinician(db, current_user.id)
    else:
        return PatientService.get_patients(db, skip=skip, limit=limit)

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get patient by ID."""
    patient = PatientService.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: UUID,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update patient."""
    patient = PatientService.update_patient(db, patient_id, patient_update)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return patient

# backend/routes/notes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date

from ..database import get_db
from ..schemas import (
    ProgressNoteCreate, ProgressNoteUpdate, ProgressNoteResponse,
    ProgressNoteDraftSave, ProgressNoteSign, ProgressNoteUnlock,
    ProgressNoteFilters, PaginatedResponse, DashboardStats, NoteType
)
from ..services import ProgressNoteService
from ..auth import get_current_active_user, require_supervisor
from ..models import User

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

# backend/routes/templates.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..database import get_db
from ..schemas import NoteTemplateCreate, NoteTemplateUpdate, NoteTemplateResponse
from ..services import NoteTemplateService
from ..auth import get_current_active_user, require_admin
from ..models import User

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

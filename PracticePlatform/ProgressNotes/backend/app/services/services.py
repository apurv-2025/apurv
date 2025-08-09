from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID
import json
from fastapi.encoders import jsonable_encoder

from app.models import (
    User, Patient, ProgressNote, NoteTemplate, 
    NoteAttachment, AuditLog, PatientClinician
)
from app.schemas import (
    UserCreate, UserUpdate, PatientCreate, PatientUpdate,
    ProgressNoteCreate, ProgressNoteUpdate, NoteTemplateCreate,
    ProgressNoteFilters, PaginatedResponse
)
from app.auth import get_password_hash

class AuditService:
    """Service for handling audit logging."""
    
    @staticmethod
    def log_action(
        db: Session,
        user_id: UUID,
        action: str,
        resource_type: str,
        resource_id: UUID,
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """Create an audit log entry."""
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(audit_log)
        db.commit()

class UserService:
    """Service for user management."""
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_create.password)
        user = User(
            email=user_create.email,
            password_hash=hashed_password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            role=user_create.role,
            license_number=user_create.license_number,
            is_active=user_create.is_active
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users."""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        """Update a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            db.commit()
            db.refresh(user)
        return user

class PatientService:
    """Service for patient management."""
    
    @staticmethod
    def create_patient(db: Session, patient_create: PatientCreate) -> Patient:
        """Create a new patient."""
        patient = Patient(**patient_create.model_dump())
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient
    
    @staticmethod
    def get_patient_by_id(db: Session, patient_id: UUID) -> Optional[Patient]:
        """Get patient by ID."""
        return db.query(Patient).filter(Patient.id == patient_id).first()
    
    @staticmethod
    def get_patients_for_clinician(db: Session, clinician_id: UUID) -> List[Patient]:
        """Get patients assigned to a clinician."""
        return db.query(Patient).join(PatientClinician).filter(
            PatientClinician.clinician_id == clinician_id
        ).all()
    
    @staticmethod
    def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Get list of patients."""
        return db.query(Patient).filter(Patient.is_active == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_patient(db: Session, patient_id: UUID, patient_update: PatientUpdate) -> Optional[Patient]:
        """Update a patient."""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            update_data = patient_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(patient, field, value)
            db.commit()
            db.refresh(patient)
        return patient

class NoteTemplateService:
    """Service for note template management."""
    
    @staticmethod
    def create_template(db: Session, template_create: NoteTemplateCreate, created_by: UUID) -> NoteTemplate:
        """Create a new note template."""
        template = NoteTemplate(
            **template_create.model_dump(),
            created_by=created_by
        )
        db.add(template)
        db.commit()
        db.refresh(template)
        return template
    
    @staticmethod
    def get_templates(db: Session, template_type: Optional[str] = None) -> List[NoteTemplate]:
        """Get note templates."""
        query = db.query(NoteTemplate).filter(NoteTemplate.is_active == True)
        if template_type:
            query = query.filter(NoteTemplate.template_type == template_type)
        return query.all()
    
    @staticmethod
    def get_template_by_id(db: Session, template_id: UUID) -> Optional[NoteTemplate]:
        """Get template by ID."""
        return db.query(NoteTemplate).filter(NoteTemplate.id == template_id).first()

class ProgressNoteService:
    """Service for progress note management."""
    
    @staticmethod
    def create_note(db: Session, note_create: ProgressNoteCreate, clinician_id: UUID) -> ProgressNote:
        """Create a new progress note."""
        note = ProgressNote(
            **note_create.model_dump(),
            clinician_id=clinician_id
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        
        # Log audit entry
        AuditService.log_action(
            db, clinician_id, "create", "progress_note", note.id,
            new_values={"note_type": note.note_type, "patient_id": str(note.patient_id)}
        )
        
        return note
    
    @staticmethod
    def get_note_by_id(db: Session, note_id: UUID, user: User) -> Optional[ProgressNote]:
        """Get note by ID with access control."""
        query = db.query(ProgressNote).options(
            joinedload(ProgressNote.patient),
            joinedload(ProgressNote.clinician),
            joinedload(ProgressNote.template)
        ).filter(ProgressNote.id == note_id)
        
        # Apply access control
        if user.role == "clinician":
            query = query.filter(ProgressNote.clinician_id == user.id)
        elif user.role == "billing_staff":
            query = query.filter(ProgressNote.is_signed == True)
        
        note = query.first()
        
        # Log audit entry for read access
        if note:
            AuditService.log_action(
                db, user.id, "read", "progress_note", note.id
            )
        
        return note
    
    @staticmethod
    def get_notes(db: Session, filters: ProgressNoteFilters, user: User) -> PaginatedResponse:
        """Get notes with filtering and pagination."""
        query = db.query(ProgressNote).options(
            joinedload(ProgressNote.patient),
            joinedload(ProgressNote.clinician),
            joinedload(ProgressNote.template)
        )
        
        print("get_notes, with role",user.role)
        # Apply access control
        if user.role == "clinician":
            query = query.filter(ProgressNote.clinician_id == user.id)
        elif user.role == "billing_staff":
            query = query.filter(ProgressNote.is_signed == True)
        
        # Apply filters
        if filters.patient_id:
            query = query.filter(ProgressNote.patient_id == filters.patient_id)
        if filters.clinician_id and user.role in ["supervisor", "admin"]:
            query = query.filter(ProgressNote.clinician_id == filters.clinician_id)
        if filters.note_type:
            query = query.filter(ProgressNote.note_type == filters.note_type)
        if filters.is_draft is not None:
            query = query.filter(ProgressNote.is_draft == filters.is_draft)
        if filters.is_signed is not None:
            query = query.filter(ProgressNote.is_signed == filters.is_signed)
        if filters.date_from:
            query = query.filter(ProgressNote.session_date >= filters.date_from)
        if filters.date_to:
            query = query.filter(ProgressNote.session_date <= filters.date_to)
        if filters.search_query:
            search_term = f"%{filters.search_query}%"
            query = query.filter(
                or_(
                    func.cast(ProgressNote.content, db.String).ilike(search_term),
                    func.concat(Patient.first_name, ' ', Patient.last_name).ilike(search_term)
                )
            ).join(Patient)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        skip = (filters.page - 1) * filters.page_size
        notes = query.order_by(desc(ProgressNote.session_date)).offset(skip).limit(filters.page_size).all()
        
        print("Number of Notes ",total)

        encoded_notes = jsonable_encoder(notes)

        return PaginatedResponse(
            items=encoded_notes,  # Use encoded notes instead of raw SQLAlchemy objects
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            total_pages=(total + filters.page_size - 1) // filters.page_size
        )

    
    @staticmethod
    def update_note(
        db: Session, 
        note_id: UUID, 
        note_update: ProgressNoteUpdate, 
        user: User
    ) -> Optional[ProgressNote]:
        """Update a progress note."""
        note = db.query(ProgressNote).filter(ProgressNote.id == note_id).first()
        
        if not note:
            return None
        
        # Check permissions
        if user.role == "clinician" and note.clinician_id != user.id:
            return None
        
        if note.is_signed and user.role not in ["supervisor", "admin"]:
            return None
        
        # Store old values for audit
        old_values = {
            "content": note.content,
            "note_type": note.note_type,
            "session_date": note.session_date.isoformat() if note.session_date else None
        }
        
        # Update fields
        update_data = note_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(note, field, value)
        
        note.version += 1
        db.commit()
        db.refresh(note)
        
        # Log audit entry
        AuditService.log_action(
            db, user.id, "update", "progress_note", note.id,
            old_values=old_values,
            new_values=update_data
        )
        
        return note
    
    @staticmethod
    def save_draft(db: Session, note_id: UUID, content: Dict[str, Any], user: User) -> Optional[ProgressNote]:
        """Save note as draft (auto-save functionality)."""
        note = db.query(ProgressNote).filter(ProgressNote.id == note_id).first()
        
        if not note or (user.role == "clinician" and note.clinician_id != user.id):
            return None
        
        if note.is_signed:
            return None
        
        note.content = content
        db.commit()
        db.refresh(note)
        
        return note
    
    @staticmethod
    def sign_note(db: Session, note_id: UUID, user: User, digital_signature: Optional[str] = None) -> Optional[ProgressNote]:
        """Sign a progress note."""
        note = db.query(ProgressNote).filter(ProgressNote.id == note_id).first()
        
        if not note or (user.role == "clinician" and note.clinician_id != user.id):
            return None
        
        if note.is_signed:
            return None
        
        note.is_draft = False
        note.is_signed = True
        note.signed_at = datetime.utcnow()
        note.signed_by = user.id
        note.digital_signature = digital_signature
        note.is_locked = True
        
        db.commit()
        db.refresh(note)
        
        # Log audit entry
        AuditService.log_action(
            db, user.id, "sign", "progress_note", note.id,
            new_values={"signed_at": note.signed_at.isoformat()}
        )
        
        return note
    
    @staticmethod
    def unlock_note(db: Session, note_id: UUID, unlock_reason: str, user: User) -> Optional[ProgressNote]:
        """Unlock a signed note (supervisor/admin only)."""
        if user.role not in ["supervisor", "admin"]:
            return None
        
        note = db.query(ProgressNote).filter(ProgressNote.id == note_id).first()
        
        if not note or not note.is_signed:
            return None
        
        note.is_locked = False
        note.locked_by = user.id
        note.locked_at = datetime.utcnow()
        note.unlock_reason = unlock_reason
        
        db.commit()
        db.refresh(note)
        
        # Log audit entry
        AuditService.log_action(
            db, user.id, "unlock", "progress_note", note.id,
            new_values={"unlock_reason": unlock_reason, "unlocked_at": note.locked_at.isoformat()}
        )
        
        return note
    
    @staticmethod
    def get_dashboard_stats(db: Session, user: User) -> Dict[str, Any]:
        """Get dashboard statistics for a user."""
        query = db.query(ProgressNote)
        
        if user.role == "clinician":
            query = query.filter(ProgressNote.clinician_id == user.id)
        
        total_notes = query.count()
        draft_notes = query.filter(ProgressNote.is_draft == True).count()
        signed_notes = query.filter(ProgressNote.is_signed == True).count()
        
        # Notes this week
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        notes_this_week = query.filter(ProgressNote.created_at >= week_ago).count()
        
        # Notes this month
        month_ago = datetime.utcnow() - timedelta(days=30)
        notes_this_month = query.filter(ProgressNote.created_at >= month_ago).count()
        
        # Recent notes
        recent_notes = query.options(
            joinedload(ProgressNote.patient)
        ).order_by(desc(ProgressNote.created_at)).limit(5).all()
        
        return {
            "total_notes": total_notes,
            "draft_notes": draft_notes,
            "signed_notes": signed_notes,
            "notes_this_week": notes_this_week,
            "notes_this_month": notes_this_month,
            "recent_notes": recent_notes
        }

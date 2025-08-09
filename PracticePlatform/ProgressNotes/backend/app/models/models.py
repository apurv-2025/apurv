# backend/models.py
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, JSON, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)  # clinician, supervisor, admin, billing_staff
    license_number = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    created_notes = relationship("ProgressNote", foreign_keys="ProgressNote.clinician_id", back_populates="clinician")
    signed_notes = relationship("ProgressNote", foreign_keys="ProgressNote.signed_by", back_populates="signer")
    created_templates = relationship("NoteTemplate", back_populates="creator")
    patient_assignments = relationship("PatientClinician", back_populates="clinician")

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    medical_record_number = Column(String(50), unique=True, nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    progress_notes = relationship("ProgressNote", back_populates="patient")
    clinician_assignments = relationship("PatientClinician", back_populates="patient")

class NoteTemplate(Base):
    __tablename__ = "note_templates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    template_type = Column(String(50), nullable=False)  # SOAP, DAP, BIRP, PAIP, Custom
    structure = Column(JSON, nullable=False)
    is_system_template = Column(Boolean, default=False)
    created_by = Column(String(36), ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="created_templates")
    progress_notes = relationship("ProgressNote", back_populates="template")

class ProgressNote(Base):
    __tablename__ = "progress_notes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    clinician_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    template_id = Column(String(36), ForeignKey("note_templates.id"))
    note_type = Column(String(50), nullable=False)
    session_date = Column(DateTime(timezone=True), nullable=False)
    content = Column(JSON, nullable=False)
    is_draft = Column(Boolean, default=True)
    is_signed = Column(Boolean, default=False)
    signed_at = Column(DateTime(timezone=True))
    signed_by = Column(String(36), ForeignKey("users.id"))
    digital_signature = Column(Text)
    is_locked = Column(Boolean, default=False)
    locked_by = Column(String(36), ForeignKey("users.id"))
    locked_at = Column(DateTime(timezone=True))
    unlock_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    version = Column(Integer, default=1)
    
    # Relationships
    patient = relationship("Patient", back_populates="progress_notes")
    clinician = relationship("User", foreign_keys=[clinician_id], back_populates="created_notes")
    signer = relationship("User", foreign_keys=[signed_by], back_populates="signed_notes")
    template = relationship("NoteTemplate", back_populates="progress_notes")
    attachments = relationship("NoteAttachment", back_populates="note", cascade="all, delete-orphan")

class NoteAttachment(Base):
    __tablename__ = "note_attachments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    note_id = Column(String(36), ForeignKey("progress_notes.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    uploaded_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    note = relationship("ProgressNote", back_populates="attachments")
    uploader = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)  # create, read, update, delete, sign, unlock
    resource_type = Column(String(50), nullable=False)  # progress_note, template, user
    resource_id = Column(String(36), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))  # IP address as string
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")

class PatientClinician(Base):
    __tablename__ = "patient_clinicians"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    clinician_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    is_primary = Column(Boolean, default=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="clinician_assignments")
    clinician = relationship("User", back_populates="patient_assignments")

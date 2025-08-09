"""
Scheduling2.0 - SQLAlchemy Models
Merged models from both MBH-Scheduling and Scheduling projects
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Text, Date, Time, JSON, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from datetime import datetime, timezone
from uuid import UUID as PyUUID
from app.database import Base
from app.utils.enums import (
    AppointmentStatus, ServiceType, AppointmentType, SessionType,
    BillingType, WaitlistPriority, WaitlistStatus, UserRole
)

# ============================================================================
# Organization Model (from Scheduling project)
# ============================================================================
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default="uuid_generate_v4()")
    fhir_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    alias = Column(ARRAY(Text))  # Alternative names
    description = Column(Text)
    identifiers = Column(JSONB)  # NPI, Tax ID
    type = Column(JSONB)  # CodeableConcept
    telecom = Column(JSONB)  # Contact information
    addresses = Column(JSONB)  # Addresses
    part_of = Column(UUID(as_uuid=True))  # Parent organization
    contact = Column(JSONB)  # Contact persons
    endpoints = Column(JSONB)  # Technical connections
    active = Column(Boolean, default=True)
    fhir_resource = Column(JSONB)  # FHIR Metadata
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    locations = relationship("Location", back_populates="organization")
    practitioners = relationship("Practitioner", back_populates="organization")
    patients = relationship("Patient", back_populates="organization")
    clients = relationship("Client", back_populates="organization")

# ============================================================================
# User Model (from Scheduling project)
# ============================================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum('admin', 'practitioner', 'nurse', 'receptionist', 'therapist', 'psychiatrist', name="user_role_enum"), nullable=False)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    practitioner = relationship("Practitioner", back_populates="user", uselist=False)
    created_appointments = relationship("Appointment", foreign_keys="Appointment.created_by", back_populates="created_by_user")

# ============================================================================
# Location Model (from MBH-Scheduling)
# ============================================================================
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    is_telehealth = Column(Boolean, default=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="locations")
    appointments = relationship("Appointment", back_populates="location")
    notification_settings = relationship("NotificationSettings", back_populates="organization")

# ============================================================================
# Service Code Model (from MBH-Scheduling)
# ============================================================================
class ServiceCode(Base):
    __tablename__ = "service_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    default_fee = Column(Integer, nullable=False)  # Fee in cents
    duration_minutes = Column(Integer, nullable=False)
    service_type = Column(Enum('THERAPY', 'CONSULTATION', 'ASSESSMENT', 'MEDICAL', 'MENTAL_HEALTH', 'FOLLOW_UP', 'EMERGENCY', name="service_type_enum"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="service_code")

# ============================================================================
# Specialty Model (from Scheduling project)
# ============================================================================
class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    practitioner_specialties = relationship("PractitionerSpecialty", back_populates="specialty")

# ============================================================================
# Appointment Type Model (from Scheduling project)
# ============================================================================
class AppointmentType(Base):
    __tablename__ = "appointment_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=30)
    color = Column(String(7), default="#3498db")
    description = Column(Text)
    service_type = Column(Enum('THERAPY', 'CONSULTATION', 'ASSESSMENT', 'MEDICAL', 'MENTAL_HEALTH', 'FOLLOW_UP', 'EMERGENCY', name="service_type_enum"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="appointment_type")

# ============================================================================
# Practitioner Model (merged from both projects)
# ============================================================================
class Practitioner(Base):
    __tablename__ = "practitioners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    fhir_id = Column(String(255), unique=True)
    
    # Basic Identity
    family_name = Column(String(255), nullable=False)
    given_names = Column(ARRAY(String))  # Array of given names
    prefix = Column(String(50))
    suffix = Column(String(50))
    
    # Credentials and Role
    qualifications = Column(JSONB)
    specialties = Column(JSONB)
    roles = Column(JSONB)
    
    # Identifiers
    identifiers = Column(JSONB)
    
    # Contact Info
    telecom = Column(JSONB)
    addresses = Column(JSONB)
    
    # Associated Organization
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    
    # Availability
    availability = Column(JSONB)
    
    # FHIR resource
    fhir_resource = Column(JSONB)
    
    # Audit Fields
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="practitioner")
    organization = relationship("Organization", back_populates="practitioners")
    appointments = relationship("Appointment", back_populates="practitioner")
    waitlist_entries = relationship("WaitlistEntry", back_populates="practitioner")
    practitioner_specialties = relationship("PractitionerSpecialty", back_populates="practitioner")
    availability = relationship("PractitionerAvailability", back_populates="practitioner")

# ============================================================================
# Practitioner Specialty Junction Model (from Scheduling project)
# ============================================================================
class PractitionerSpecialty(Base):
    __tablename__ = "practitioner_specialties"

    practitioner_id = Column(Integer, ForeignKey("practitioners.id", ondelete="CASCADE"), primary_key=True)
    specialty_id = Column(Integer, ForeignKey("specialties.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    practitioner = relationship("Practitioner", back_populates="practitioner_specialties")
    specialty = relationship("Specialty", back_populates="practitioner_specialties")

# ============================================================================
# Patient Model (from Scheduling project)
# ============================================================================
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), index=True)
    phone = Column(String(20), nullable=False, index=True)
    date_of_birth = Column(Date)
    address = Column(Text)
    insurance_info = Column(Text)
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    medical_notes = Column(Text)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    waitlist_entries = relationship("WaitlistEntry", back_populates="patient")
    notification_preferences = relationship("PatientNotificationPreferences", back_populates="patient", uselist=False)

# ============================================================================
# Client Model (from MBH-Scheduling)
# ============================================================================
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), index=True)
    phone = Column(String(20))
    date_of_birth = Column(Date)
    emergency_contact = Column(Text)
    is_active = Column(Boolean, default=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="clients")
    appointments = relationship("Appointment", back_populates="client")
    waitlist_entries = relationship("WaitlistEntry", back_populates="client")
    notification_preferences = relationship("ClientNotificationPreferences", back_populates="client", uselist=False)

# ============================================================================
# Practitioner Availability Model (from Scheduling project)
# ============================================================================
class PractitionerAvailability(Base):
    __tablename__ = "practitioner_availability"

    id = Column(Integer, primary_key=True, index=True)
    practitioner_id = Column(Integer, ForeignKey("practitioners.id", ondelete="CASCADE"), nullable=False)
    availability_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    practitioner = relationship("Practitioner", back_populates="availability")
    
    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_practitioner_availability_date', 'practitioner_id', 'availability_date'),
    )

# ============================================================================
# Appointment Model (merged from both projects)
# ============================================================================
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Patient/Client references (support both)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"))
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))
    
    # Practitioner and appointment details
    practitioner_id = Column(Integer, ForeignKey("practitioners.id", ondelete="CASCADE"), nullable=False)
    appointment_type_id = Column(Integer, ForeignKey("appointment_types.id"))
    service_code_id = Column(Integer, ForeignKey("service_codes.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    
    # Appointment details
    appointment_type = Column(Enum('APPOINTMENT', 'CONSULTATION', 'FOLLOW_UP', 'INITIAL', 'EMERGENCY', name="appointment_type_enum"), nullable=False)
    session_type = Column(Enum('INDIVIDUAL', 'COUPLE', 'FAMILY', 'GROUP', 'TELEHEALTH', 'IN_PERSON', name="session_type_enum"), nullable=False)
    appointment_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    service_type = Column(Enum('THERAPY', 'CONSULTATION', 'ASSESSMENT', 'MEDICAL', 'MENTAL_HEALTH', 'FOLLOW_UP', 'EMERGENCY', name="service_type_enum"), nullable=False)
    status = Column(Enum('SCHEDULED', 'CONFIRMED', 'PENDING', 'CANCELLED', 'NO_SHOW', 'COMPLETED', name="appointment_status_enum"), default='SCHEDULED', index=True)
    billing_type = Column(Enum('SELF_PAY', 'INSURANCE', 'SLIDING_SCALE', 'MEDICARE', 'MEDICAID', name="billing_type_enum"), nullable=False)
    fee_amount = Column(Integer)  # Amount in cents
    notes = Column(Text)
    reason_for_visit = Column(Text)
    is_telehealth = Column(Boolean, default=False)
    
    # Audit fields
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    client = relationship("Client", back_populates="appointments")
    practitioner = relationship("Practitioner", back_populates="appointments")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="created_appointments")
    appointment_type = relationship("AppointmentType", back_populates="appointments")
    service_code = relationship("ServiceCode", back_populates="appointments")
    location = relationship("Location", back_populates="appointments")
    reminders = relationship("AppointmentReminder", back_populates="appointment")
    notification_history = relationship("NotificationHistory", back_populates="appointment")

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "(patient_id IS NOT NULL AND client_id IS NULL) OR (patient_id IS NULL AND client_id IS NOT NULL)",
            name="check_patient_or_client"
        ),
    )

# ============================================================================
# Waitlist Entry Model (from MBH-Scheduling)
# ============================================================================
class WaitlistEntry(Base):
    __tablename__ = "waitlist_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    practitioner_id = Column(Integer, ForeignKey("practitioners.id"), nullable=True)
    appointment_type_id = Column(Integer, ForeignKey("appointment_types.id"), nullable=True)
    preferred_date = Column(Date, nullable=True)
    preferred_time_start = Column(Time, nullable=True)
    preferred_time_end = Column(Time, nullable=True)
    priority = Column(Enum('LOW', 'MEDIUM', 'HIGH', 'URGENT', name="waitlist_priority_enum"), default='MEDIUM')
    status = Column(Enum('WAITING', 'CONTACTED', 'SCHEDULED', 'CANCELLED', name="waitlist_status_enum"), default='WAITING')
    notes = Column(Text, nullable=True)
    contact_attempts = Column(Integer, default=0)
    last_contact_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="waitlist_entries")
    patient = relationship("Patient", back_populates="waitlist_entries")
    client = relationship("Client", back_populates="waitlist_entries")
    practitioner = relationship("Practitioner", back_populates="waitlist_entries")
    appointment_type = relationship("AppointmentType", back_populates="waitlist_entries")
    notification_history = relationship("NotificationHistory", back_populates="waitlist_entry")
    
    __table_args__ = (
        CheckConstraint(
            'patient_id IS NOT NULL OR client_id IS NOT NULL',
            name='waitlist_patient_or_client_required'
        ),
    ) 
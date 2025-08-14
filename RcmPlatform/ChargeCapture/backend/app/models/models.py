# models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Numeric, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

Base = declarative_base()

class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    npi = Column(String(10), unique=True, nullable=False)
    specialty = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    charges = relationship("Charge", back_populates="provider", foreign_keys="Charge.provider_id")
    templates = relationship("ChargeTemplate", back_populates="provider")

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    mrn = Column(String(50), unique=True, nullable=False)  # Medical Record Number
    insurance_info = Column(JSONB)  # Store insurance details as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    encounters = relationship("Encounter", back_populates="patient")
    charges = relationship("Charge", back_populates="patient")

class Encounter(Base):
    __tablename__ = "encounters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False)
    encounter_date = Column(DateTime, nullable=False)
    encounter_type = Column(String(50), nullable=False)  # office_visit, procedure, consultation, etc.
    status = Column(String(20), default="scheduled")  # scheduled, in_progress, completed, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="encounters")
    provider = relationship("Provider")
    charges = relationship("Charge", back_populates="encounter")

class Charge(Base):
    __tablename__ = "charges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False)
    
    # Charge details
    cpt_code = Column(String(10), nullable=False)
    cpt_description = Column(String(255))
    icd_code = Column(String(10), nullable=False)
    icd_description = Column(String(255))
    hcpcs_code = Column(String(10))
    
    # Modifiers and quantities
    modifiers = Column(JSONB)  # Array of modifier codes
    units = Column(Integer, default=1)
    quantity = Column(Integer, default=1)
    charge_amount = Column(Numeric(10, 2))
    
    # Status and workflow
    status = Column(String(20), default="draft")  # draft, submitted, billed, rejected, paid
    capture_method = Column(String(20))  # point_of_care, post_encounter, batch
    captured_at = Column(DateTime, default=datetime.utcnow)
    captured_by = Column(UUID(as_uuid=True), ForeignKey("providers.id"))
    
    # Billing integration
    claim_id = Column(String(50))  # Reference to billing system
    submitted_to_billing_at = Column(DateTime)
    
    # Compliance and audit
    validation_errors = Column(JSONB)  # Store validation issues
    audit_log = Column(JSONB)  # Track changes
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    encounter = relationship("Encounter", back_populates="charges")
    patient = relationship("Patient", back_populates="charges")
    provider = relationship("Provider", back_populates="charges", foreign_keys=[provider_id])

class ChargeTemplate(Base):
    __tablename__ = "charge_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    specialty = Column(String(100), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"))  # NULL for system-wide templates
    
    # Template configuration
    template_data = Column(JSONB, nullable=False)  # Store template structure
    is_active = Column(Boolean, default=True)
    is_system_template = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    provider = relationship("Provider", back_populates="templates")

class ChargeValidationRule(Base):
    __tablename__ = "charge_validation_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_name = Column(String(100), nullable=False)
    rule_type = Column(String(50), nullable=False)  # code_combination, payer_specific, etc.
    specialty = Column(String(100))  # NULL for all specialties
    payer = Column(String(100))  # NULL for all payers
    
    rule_config = Column(JSONB, nullable=False)  # Store rule logic
    is_active = Column(Boolean, default=True)
    error_message = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)

# Indexes for performance
Index('ix_charges_encounter_id', Charge.encounter_id)
Index('ix_charges_patient_id', Charge.patient_id)
Index('ix_charges_provider_id', Charge.provider_id)
Index('ix_charges_status', Charge.status)
Index('ix_charges_captured_at', Charge.captured_at)
Index('ix_encounters_date', Encounter.encounter_date)
Index('ix_encounters_provider', Encounter.provider_id)

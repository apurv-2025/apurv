# =============================================================================
# FILE: backend/app/database/models.py
# =============================================================================
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base
import enum

class ClaimType(str, enum.Enum):
    DENTAL = "837D"
    PROFESSIONAL = "837P" 
    INSTITUTIONAL = "837I"

class ClaimStatus(str, enum.Enum):
    QUEUED = "queued"
    VALIDATING = "validating"
    VALIDATED = "validated"
    REJECTED = "rejected"
    SENT = "sent"
    ACCEPTED = "accepted"
    DENIED = "denied"
    PAID = "paid"
    ADJUSTED = "adjusted"

class AgentTaskStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_HUMAN = "requires_human"

class AgentTaskType(str, enum.Enum):
    PROCESS_CLAIM = "process_claim"
    VALIDATE_CLAIM = "validate_claim"
    ANALYZE_REJECTION = "analyze_rejection"
    RECONCILE_PAYMENT = "reconcile_payment"
    GENERATE_REPORT = "generate_report"
    ANSWER_QUESTION = "answer_question"
    TROUBLESHOOT = "troubleshoot"

class WorkQueueStatus(str, enum.Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class WorkQueuePriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(Integer, primary_key=True, index=True)
    claim_number = Column(String(50), unique=True, index=True)
    claim_type = Column(Enum(ClaimType), nullable=False)
    status = Column(Enum(ClaimStatus), default=ClaimStatus.QUEUED)
    
    # Patient Information
    patient_first_name = Column(String(100))
    patient_last_name = Column(String(100))
    patient_dob = Column(DateTime)
    patient_id = Column(String(50))
    
    # Provider Information
    provider_name = Column(String(200))
    provider_npi = Column(String(10))
    provider_taxonomy = Column(String(10))
    
    # Payer Information
    payer_id = Column(Integer, ForeignKey("payers.id"))
    payer = relationship("Payer", back_populates="claims")
    
    # Financial Information
    total_charge = Column(Numeric(10, 2))
    allowed_amount = Column(Numeric(10, 2))
    paid_amount = Column(Numeric(10, 2))
    patient_responsibility = Column(Numeric(10, 2))
    
    # EDI Information
    raw_edi_data = Column(Text)
    parsed_data = Column(JSON)
    validation_errors = Column(JSON)
    
    # Work Queue Information
    work_queue_status = Column(Enum(WorkQueueStatus), default=WorkQueueStatus.PENDING)
    work_queue_priority = Column(Enum(WorkQueuePriority), default=WorkQueuePriority.MEDIUM)
    assigned_to = Column(String(100))  # User ID or agent ID
    assigned_at = Column(DateTime)
    estimated_completion = Column(DateTime)
    work_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    submitted_at = Column(DateTime)
    processed_at = Column(DateTime)
    
    # Relationships
    service_lines = relationship("ServiceLine", back_populates="claim")
    dental_details = relationship("DentalDetail", back_populates="claim", uselist=False)
    agent_tasks = relationship("AgentTask", back_populates="claim")

class ServiceLine(Base):
    __tablename__ = "service_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    line_number = Column(Integer)
    
    # Procedure Information
    procedure_code = Column(String(10))  # CPT/CDT codes
    procedure_description = Column(String(500))
    modifier_1 = Column(String(2))
    modifier_2 = Column(String(2))
    modifier_3 = Column(String(2))
    modifier_4 = Column(String(2))
    
    # Service Details
    service_date_from = Column(DateTime)
    service_date_to = Column(DateTime)
    units = Column(Integer, default=1)
    
    # Financial
    charge_amount = Column(Numeric(10, 2))
    allowed_amount = Column(Numeric(10, 2))
    paid_amount = Column(Numeric(10, 2))
    
    # Diagnosis
    diagnosis_code_1 = Column(String(10))
    diagnosis_code_2 = Column(String(10))
    diagnosis_code_3 = Column(String(10))
    diagnosis_code_4 = Column(String(10))
    
    claim = relationship("Claim", back_populates="service_lines")

class DentalDetail(Base):
    __tablename__ = "dental_details"
    
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    
    # Tooth-specific information
    tooth_number = Column(String(3))  # Universal numbering system
    tooth_surface = Column(String(10))  # M, O, D, L, B, I combinations
    oral_cavity_area = Column(String(2))
    
    # Treatment information
    treatment_plan_sequence = Column(Integer)
    months_of_treatment = Column(Integer)  # For orthodontics
    
    # Additional dental data
    prosthetic_replacement = Column(Boolean, default=False)
    initial_placement_date = Column(DateTime)
    
    claim = relationship("Claim", back_populates="dental_details")

class Payer(Base):
    __tablename__ = "payers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    payer_id = Column(String(50), unique=True)  # Electronic payer ID
    address = Column(String(500))
    contact_info = Column(JSON)
    
    # Configuration
    companion_guide_url = Column(String(500))
    validation_rules = Column(JSON)
    transmission_method = Column(String(20))  # FTP, AS2, API
    
    # Status
    is_active = Column(Boolean, default=True)
    certification_status = Column(String(50))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    claims = relationship("Claim", back_populates="payer")

class AgentTask(Base):
    __tablename__ = "agent_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(100), unique=True, index=True)
    task_type = Column(Enum(AgentTaskType), nullable=False)
    status = Column(Enum(AgentTaskStatus), default=AgentTaskStatus.PENDING)
    
    # User and context
    user_id = Column(String(100), nullable=False)
    description = Column(Text)
    context = Column(JSON)
    
    # Related claim (optional)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    claim = relationship("Claim", back_populates="agent_tasks")
    
    # Results
    result = Column(JSON)
    insights = Column(JSON)
    suggestions = Column(JSON)
    error_message = Column(Text)
    
    # Metrics
    confidence_score = Column(Numeric(3, 2))
    processing_time_seconds = Column(Numeric(10, 3))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class WorkQueue(Base):
    __tablename__ = "work_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    claim = relationship("Claim")
    
    # Assignment information
    assigned_by = Column(String(100), nullable=False)  # User who assigned the claim
    assigned_to = Column(String(100), nullable=False)  # User or agent assigned to work on it
    assigned_at = Column(DateTime, server_default=func.now())
    
    # Work queue details
    status = Column(Enum(WorkQueueStatus), default=WorkQueueStatus.PENDING)
    priority = Column(Enum(WorkQueuePriority), default=WorkQueuePriority.MEDIUM)
    estimated_completion = Column(DateTime)
    actual_completion = Column(DateTime)
    
    # Work details
    work_notes = Column(Text)
    action_taken = Column(Text)
    result_summary = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

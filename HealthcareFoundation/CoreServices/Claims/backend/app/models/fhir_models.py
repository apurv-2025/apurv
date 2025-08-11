# models/fhir_models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from models.database import Base
import uuid
from datetime import datetime

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    resource_type = Column(String, default="Claim", nullable=False)
    identifier = Column(JSON)  # Array of identifiers
    trace_number = Column(JSON)  # Array of trace numbers
    status = Column(String, nullable=False)  # active|cancelled|draft|entered-in-error
    type = Column(JSON, nullable=False)  # CodeableConcept
    sub_type = Column(JSON)  # CodeableConcept
    use = Column(String, nullable=False)  # claim|preauthorization|predetermination
    patient_id = Column(String, nullable=False)  # Reference(Patient)
    billable_period = Column(JSON)  # Period
    created = Column(DateTime, default=datetime.utcnow)
    enterer_id = Column(String)  # Reference(Practitioner|PractitionerRole)
    insurer_id = Column(String, nullable=False)  # Reference(Organization)
    provider_id = Column(String, nullable=False)  # Reference(Practitioner|PractitionerRole|Organization)
    priority = Column(JSON)  # CodeableConcept
    funds_reserve = Column(JSON)  # CodeableConcept
    related = Column(JSON)  # Array of related claims
    prescription_id = Column(String)  # Reference
    original_prescription_id = Column(String)  # Reference
    payee = Column(JSON)  # Payee information
    referral_id = Column(String)  # Reference(ServiceRequest)
    encounter = Column(JSON)  # Array of References(Encounter)
    facility_id = Column(String)  # Reference(Location)
    diagnosis_related_group = Column(JSON)  # CodeableConcept
    event = Column(JSON)  # Array of events
    care_team = Column(JSON)  # Array of care team members
    supporting_info = Column(JSON)  # Array of supporting information
    diagnosis = Column(JSON)  # Array of diagnoses
    procedure = Column(JSON)  # Array of procedures
    insurance = Column(JSON, nullable=False)  # Array of insurance information
    accident = Column(JSON)  # Accident information
    patient_paid = Column(JSON)  # Money
    item = Column(JSON)  # Array of claim items
    total = Column(JSON)  # Money
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    responses = relationship("ClaimResponse", back_populates="claim")
    explanations = relationship("ExplanationOfBenefit", back_populates="claim")

class ClaimResponse(Base):
    __tablename__ = "claim_responses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    resource_type = Column(String, default="ClaimResponse", nullable=False)
    identifier = Column(JSON)  # Array of identifiers
    trace_number = Column(JSON)  # Array of trace numbers
    status = Column(String, nullable=False)
    type = Column(JSON, nullable=False)  # CodeableConcept
    sub_type = Column(JSON)  # CodeableConcept
    use = Column(String, nullable=False)
    patient_id = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    insurer_id = Column(String, nullable=False)
    requestor_id = Column(String)
    request_id = Column(String, ForeignKey("claims.id"))  # Reference to Claim
    outcome = Column(String, nullable=False)  # queued|complete|error|partial
    decision = Column(JSON)  # CodeableConcept
    disposition = Column(String)
    pre_auth_ref = Column(String)
    pre_auth_period = Column(JSON)  # Period
    event = Column(JSON)  # Array of events
    payee_type = Column(JSON)  # CodeableConcept
    encounter = Column(JSON)  # Array of References
    diagnosis_related_group = Column(JSON)  # CodeableConcept
    item = Column(JSON)  # Array of response items
    add_item = Column(JSON)  # Array of added items
    adjudication = Column(JSON)  # Array of adjudications
    total = Column(JSON)  # Array of totals
    payment = Column(JSON)  # Payment information
    funds_reserve = Column(JSON)  # CodeableConcept
    form_code = Column(JSON)  # CodeableConcept
    form = Column(JSON)  # Attachment
    process_note = Column(JSON)  # Array of notes
    communication_request = Column(JSON)  # Array of References
    insurance = Column(JSON)  # Array of insurance info
    error = Column(JSON)  # Array of errors
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    claim = relationship("Claim", back_populates="responses")

class ExplanationOfBenefit(Base):
    __tablename__ = "explanation_of_benefits"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    resource_type = Column(String, default="ExplanationOfBenefit", nullable=False)
    identifier = Column(JSON)  # Array of identifiers
    trace_number = Column(JSON)  # Array of trace numbers
    status = Column(String, nullable=False)
    type = Column(JSON, nullable=False)  # CodeableConcept
    sub_type = Column(JSON)  # CodeableConcept
    use = Column(String, nullable=False)
    patient_id = Column(String, nullable=False)
    billable_period = Column(JSON)  # Period
    created = Column(DateTime, default=datetime.utcnow)
    enterer_id = Column(String)
    insurer_id = Column(String, nullable=False)
    provider_id = Column(String, nullable=False)
    priority = Column(JSON)  # CodeableConcept
    funds_reserve_requested = Column(JSON)  # CodeableConcept
    funds_reserve = Column(JSON)  # CodeableConcept
    related = Column(JSON)  # Array of related claims
    prescription_id = Column(String)
    original_prescription_id = Column(String)
    event = Column(JSON)  # Array of events
    payee = Column(JSON)  # Payee information
    referral_id = Column(String)
    encounter = Column(JSON)  # Array of References
    facility_id = Column(String)
    claim_id = Column(String, ForeignKey("claims.id"))
    claim_response_id = Column(String, ForeignKey("claim_responses.id"))
    outcome = Column(String, nullable=False)
    decision = Column(JSON)  # CodeableConcept
    disposition = Column(String)
    pre_auth_ref = Column(JSON)  # Array of strings
    pre_auth_ref_period = Column(JSON)  # Array of Periods
    diagnosis_related_group = Column(JSON)  # CodeableConcept
    care_team = Column(JSON)  # Array of care team
    supporting_info = Column(JSON)  # Array of supporting info
    diagnosis = Column(JSON)  # Array of diagnoses
    procedure = Column(JSON)  # Array of procedures
    precedence = Column(Integer)
    insurance = Column(JSON, nullable=False)  # Array of insurance
    accident = Column(JSON)  # Accident information
    patient_paid = Column(JSON)  # Money
    item = Column(JSON)  # Array of items
    add_item = Column(JSON)  # Array of added items
    adjudication = Column(JSON)  # Array of adjudications
    total = Column(JSON)  # Array of totals
    payment = Column(JSON)  # Payment information
    form_code = Column(JSON)  # CodeableConcept
    form = Column(JSON)  # Attachment
    process_note = Column(JSON)  # Array of notes
    benefit_period = Column(JSON)  # Period
    benefit_balance = Column(JSON)  # Array of benefit balances
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    claim = relationship("Claim", back_populates="explanations")

class Coverage(Base):
    __tablename__ = "coverages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    resource_type = Column(String, default="Coverage", nullable=False)
    identifier = Column(JSON)  # Array of identifiers
    status = Column(String, nullable=False)
    kind = Column(String)  # insurance|self-pay|other
    payment_by = Column(JSON)  # Array of payment responsibility
    type = Column(JSON)  # CodeableConcept
    policy_holder_id = Column(String)
    subscriber_id_ref = Column(String)
    subscriber_id = Column(JSON)  # Array with extensions
    beneficiary_id = Column(String, nullable=False)
    dependent = Column(String)
    relationship = Column(JSON)  # CodeableConcept
    period = Column(JSON)  # Period
    insurer_id = Column(String, nullable=False)
    class_info = Column(JSON)  # Array of class information
    order = Column(Integer)
    network = Column(String)
    cost_to_beneficiary = Column(JSON)  # Array of costs
    subrogation = Column(Boolean)
    contract = Column(JSON)  # Array of References
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


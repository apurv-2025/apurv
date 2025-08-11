-- FHIR Claims Database Initialization Script
-- PostgreSQL 12+ with JSON support

-- Create database and user (run as postgres superuser)
-- CREATE DATABASE fhir_claims_db;
-- CREATE USER fhir_user WITH PASSWORD 'fhir_password_2024!';
-- GRANT ALL PRIVILEGES ON DATABASE fhir_claims_db TO fhir_user;

-- Connect to fhir_claims_db and run the following:

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable JSON operations
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create custom types for FHIR status values
CREATE TYPE fhir_status AS ENUM ('active', 'cancelled', 'draft', 'entered-in-error');
CREATE TYPE fhir_use AS ENUM ('claim', 'preauthorization', 'predetermination');
CREATE TYPE fhir_outcome AS ENUM ('queued', 'complete', 'error', 'partial');
CREATE TYPE coverage_kind AS ENUM ('insurance', 'self-pay', 'other');

-- Claims table - FHIR Claim resource
CREATE TABLE claims (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    resource_type VARCHAR(50) DEFAULT 'Claim' NOT NULL,
    
    -- Core identifiers
    identifier JSONB, -- Array of identifiers
    trace_number JSONB, -- Array of trace numbers
    
    -- Status and classification
    status fhir_status NOT NULL,
    type JSONB NOT NULL, -- CodeableConcept for claim type
    sub_type JSONB, -- CodeableConcept for sub-classification
    use fhir_use NOT NULL,
    
    -- Patient and provider references
    patient_id VARCHAR(255) NOT NULL,
    insurer_id VARCHAR(255) NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    enterer_id VARCHAR(255),
    
    -- Dates and periods
    billable_period JSONB, -- Period
    created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Administrative information
    priority JSONB, -- CodeableConcept
    funds_reserve JSONB, -- CodeableConcept
    related JSONB, -- Array of related claims
    prescription_id VARCHAR(255),
    original_prescription_id VARCHAR(255),
    payee JSONB, -- Payee information
    referral_id VARCHAR(255),
    encounter JSONB, -- Array of encounter references
    facility_id VARCHAR(255),
    diagnosis_related_group JSONB, -- CodeableConcept
    
    -- Events and workflow
    event JSONB, -- Array of events with timing
    
    -- Clinical information
    care_team JSONB, -- Array of care team members
    supporting_info JSONB, -- Array of supporting information
    diagnosis JSONB, -- Array of diagnoses
    procedure JSONB, -- Array of procedures
    
    -- Financial information
    insurance JSONB NOT NULL, -- Array of insurance information
    accident JSONB, -- Accident information
    patient_paid JSONB, -- Money - amount paid by patient
    item JSONB, -- Array of claim line items
    total JSONB, -- Money - total claim amount
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ClaimResponse table - FHIR ClaimResponse resource
CREATE TABLE claim_responses (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    resource_type VARCHAR(50) DEFAULT 'ClaimResponse' NOT NULL,
    
    -- Core identifiers
    identifier JSONB, -- Array of identifiers
    trace_number JSONB, -- Array of trace numbers
    
    -- Status and classification
    status fhir_status NOT NULL,
    type JSONB NOT NULL, -- CodeableConcept
    sub_type JSONB, -- CodeableConcept
    use fhir_use NOT NULL,
    
    -- References
    patient_id VARCHAR(255) NOT NULL,
    insurer_id VARCHAR(255) NOT NULL,
    requestor_id VARCHAR(255),
    request_id VARCHAR(36) REFERENCES claims(id) ON DELETE SET NULL,
    
    -- Adjudication results
    outcome fhir_outcome NOT NULL,
    decision JSONB, -- CodeableConcept for decision
    disposition TEXT,
    
    -- Authorization information
    pre_auth_ref VARCHAR(255),
    pre_auth_period JSONB, -- Period
    
    -- Events and workflow
    event JSONB, -- Array of events
    
    -- Administrative
    payee_type JSONB, -- CodeableConcept
    encounter JSONB, -- Array of encounter references
    diagnosis_related_group JSONB, -- CodeableConcept
    
    -- Response details
    item JSONB, -- Array of item adjudications
    add_item JSONB, -- Array of added items
    adjudication JSONB, -- Array of header-level adjudications
    total JSONB, -- Array of total categories
    
    -- Payment information
    payment JSONB, -- Payment details
    funds_reserve JSONB, -- CodeableConcept
    
    -- Forms and communication
    form_code JSONB, -- CodeableConcept
    form JSONB, -- Attachment
    process_note JSONB, -- Array of processing notes
    communication_request JSONB, -- Array of communication requests
    
    -- Insurance and errors
    insurance JSONB, -- Array of insurance information
    error JSONB, -- Array of processing errors
    
    -- Dates
    created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ExplanationOfBenefit table - FHIR ExplanationOfBenefit resource
CREATE TABLE explanation_of_benefits (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    resource_type VARCHAR(50) DEFAULT 'ExplanationOfBenefit' NOT NULL,
    
    -- Core identifiers
    identifier JSONB, -- Array of identifiers
    trace_number JSONB, -- Array of trace numbers
    
    -- Status and classification
    status fhir_status NOT NULL,
    type JSONB NOT NULL, -- CodeableConcept
    sub_type JSONB, -- CodeableConcept
    use fhir_use NOT NULL,
    
    -- Patient and provider references
    patient_id VARCHAR(255) NOT NULL,
    insurer_id VARCHAR(255) NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    enterer_id VARCHAR(255),
    
    -- Dates and periods
    billable_period JSONB, -- Period
    created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Administrative information
    priority JSONB, -- CodeableConcept
    funds_reserve_requested JSONB, -- CodeableConcept
    funds_reserve JSONB, -- CodeableConcept
    related JSONB, -- Array of related claims
    prescription_id VARCHAR(255),
    original_prescription_id VARCHAR(255),
    event JSONB, -- Array of events
    payee JSONB, -- Payee information
    referral_id VARCHAR(255),
    encounter JSONB, -- Array of encounter references
    facility_id VARCHAR(255),
    
    -- Claim references
    claim_id VARCHAR(36) REFERENCES claims(id) ON DELETE SET NULL,
    claim_response_id VARCHAR(36) REFERENCES claim_responses(id) ON DELETE SET NULL,
    
    -- Adjudication results
    outcome fhir_outcome NOT NULL,
    decision JSONB, -- CodeableConcept
    disposition TEXT,
    pre_auth_ref JSONB, -- Array of preauth references
    pre_auth_ref_period JSONB, -- Array of periods
    diagnosis_related_group JSONB, -- CodeableConcept
    
    -- Clinical information
    care_team JSONB, -- Array of care team members
    supporting_info JSONB, -- Array of supporting information
    diagnosis JSONB, -- Array of diagnoses
    procedure JSONB, -- Array of procedures
    precedence INTEGER,
    
    -- Financial information
    insurance JSONB NOT NULL, -- Array of insurance information
    accident JSONB, -- Accident information
    patient_paid JSONB, -- Money
    item JSONB, -- Array of benefit items
    add_item JSONB, -- Array of added items
    adjudication JSONB, -- Array of adjudications
    total JSONB, -- Array of totals
    payment JSONB, -- Payment information
    
    -- Forms and notes
    form_code JSONB, -- CodeableConcept
    form JSONB, -- Attachment
    process_note JSONB, -- Array of notes
    
    -- Benefit information
    benefit_period JSONB, -- Period
    benefit_balance JSONB, -- Array of benefit balances
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Coverage table - FHIR Coverage resource
CREATE TABLE coverages (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    resource_type VARCHAR(50) DEFAULT 'Coverage' NOT NULL,
    
    -- Core identifiers
    identifier JSONB, -- Array of identifiers
    
    -- Status and classification
    status fhir_status NOT NULL,
    kind coverage_kind,
    payment_by JSONB, -- Array of payment responsibility
    type JSONB, -- CodeableConcept
    
    -- Subscriber information
    policy_holder_id VARCHAR(255),
    subscriber_id_ref VARCHAR(255),
    subscriber_id JSONB, -- Array with extensions
    beneficiary_id VARCHAR(255) NOT NULL,
    dependent VARCHAR(50),
    relationship JSONB, -- CodeableConcept
    
    -- Coverage period and insurer
    period JSONB, -- Period
    insurer_id VARCHAR(255) NOT NULL,
    
    -- Classification and network
    class_info JSONB, -- Array of class information
    order_priority INTEGER,
    network VARCHAR(255),
    
    -- Cost information
    cost_to_beneficiary JSONB, -- Array of cost information
    subrogation BOOLEAN DEFAULT FALSE,
    contract JSONB, -- Array of contract references
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_claims_patient_id ON claims(patient_id);
CREATE INDEX idx_claims_status ON claims(status);
CREATE INDEX idx_claims_insurer_id ON claims(insurer_id);
CREATE INDEX idx_claims_provider_id ON claims(provider_id);
CREATE INDEX idx_claims_created_at ON claims(created_at);
CREATE INDEX idx_claims_use ON claims(use);

CREATE INDEX idx_claim_responses_request_id ON claim_responses(request_id);
CREATE INDEX idx_claim_responses_patient_id ON claim_responses(patient_id);
CREATE INDEX idx_claim_responses_status ON claim_responses(status);
CREATE INDEX idx_claim_responses_outcome ON claim_responses(outcome);
CREATE INDEX idx_claim_responses_created_at ON claim_responses(created_at);

CREATE INDEX idx_eob_claim_id ON explanation_of_benefits(claim_id);
CREATE INDEX idx_eob_claim_response_id ON explanation_of_benefits(claim_response_id);
CREATE INDEX idx_eob_patient_id ON explanation_of_benefits(patient_id);
CREATE INDEX idx_eob_status ON explanation_of_benefits(status);
CREATE INDEX idx_eob_created_at ON explanation_of_benefits(created_at);

CREATE INDEX idx_coverages_beneficiary_id ON coverages(beneficiary_id);
CREATE INDEX idx_coverages_insurer_id ON coverages(insurer_id);
CREATE INDEX idx_coverages_status ON coverages(status);
CREATE INDEX idx_coverages_kind ON coverages(kind);

-- Create GIN indexes for JSON columns to support JSONB queries
CREATE INDEX idx_claims_identifier_gin ON claims USING GIN (identifier);
CREATE INDEX idx_claims_type_gin ON claims USING GIN (type);
CREATE INDEX idx_claims_diagnosis_gin ON claims USING GIN (diagnosis);
CREATE INDEX idx_claims_item_gin ON claims USING GIN (item);

CREATE INDEX idx_claim_responses_adjudication_gin ON claim_responses USING GIN (adjudication);
CREATE INDEX idx_claim_responses_item_gin ON claim_responses USING GIN (item);

CREATE INDEX idx_coverages_type_gin ON coverages USING GIN (type);

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_claims_updated_at 
    BEFORE UPDATE ON claims 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_claim_responses_updated_at 
    BEFORE UPDATE ON claim_responses 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_explanation_of_benefits_updated_at 
    BEFORE UPDATE ON explanation_of_benefits 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_coverages_updated_at 
    BEFORE UPDATE ON coverages 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views for common queries
CREATE VIEW active_claims AS
SELECT 
    id,
    patient_id,
    provider_id,
    insurer_id,
    status,
    use,
    type,
    total,
    created_at
FROM claims 
WHERE status = 'active';

CREATE VIEW claim_summary AS
SELECT 
    c.id,
    c.patient_id,
    c.provider_id,
    c.status as claim_status,
    c.total as claim_total,
    cr.outcome as response_outcome,
    cr.disposition,
    c.created_at as claim_created,
    cr.created as response_created
FROM claims c
LEFT JOIN claim_responses cr ON c.id = cr.request_id;

-- Insert sample data for testing
INSERT INTO claims (
    id, status, type, use, patient_id, insurer_id, provider_id, 
    insurance, total, created_at
) VALUES 
(
    'claim-001',
    'active',
    '{"text": "Professional", "coding": [{"system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "professional"}]}',
    'claim',
    'patient-123',
    'insurer-456',
    'provider-789',
    '[{"sequence": 1, "focal": true, "coverage": {"reference": "Coverage/coverage-001"}}]',
    '{"value": 1250.00, "currency": "USD"}',
    CURRENT_TIMESTAMP
),
(
    'claim-002', 
    'draft',
    '{"text": "Institutional", "coding": [{"system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "institutional"}]}',
    'preauthorization',
    'patient-456',
    'insurer-456', 
    'provider-999',
    '[{"sequence": 1, "focal": true, "coverage": {"reference": "Coverage/coverage-002"}}]',
    '{"value": 2500.00, "currency": "USD"}',
    CURRENT_TIMESTAMP
);

INSERT INTO coverages (
    id, status, kind, beneficiary_id, insurer_id, type, created_at
) VALUES 
(
    'coverage-001',
    'active',
    'insurance',
    'patient-123',
    'insurer-456',
    '{"text": "Medical", "coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "EHCPOL"}]}',
    CURRENT_TIMESTAMP
),
(
    'coverage-002',
    'active', 
    'insurance',
    'patient-456',
    'insurer-456',
    '{"text": "Dental", "coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "DENTPRG"}]}',
    CURRENT_TIMESTAMP
);

-- Grant permissions to fhir_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fhir_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fhir_user;
GRANT USAGE ON SCHEMA public TO fhir_user;

-- Analyze tables for better query planning
ANALYZE claims;
ANALYZE claim_responses;
ANALYZE explanation_of_benefits;
ANALYZE coverages;

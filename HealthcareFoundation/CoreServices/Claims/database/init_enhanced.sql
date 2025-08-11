-- Enhanced FHIR Claims Database Schema with DenialPrediction Integration
-- PostgreSQL 12+ with JSON support

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable JSON operations
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create custom types for FHIR status values
CREATE TYPE fhir_status AS ENUM ('active', 'cancelled', 'draft', 'entered-in-error');
CREATE TYPE fhir_use AS ENUM ('claim', 'preauthorization', 'predetermination');
CREATE TYPE fhir_outcome AS ENUM ('queued', 'complete', 'error', 'partial');
CREATE TYPE coverage_kind AS ENUM ('insurance', 'self-pay', 'other');
CREATE TYPE risk_level AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
CREATE TYPE resolution_status AS ENUM ('pending', 'in_progress', 'resolved', 'failed', 'cancelled');

-- Enhanced Claims table with ML prediction fields
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
    
    -- ML Prediction Fields (DenialPrediction Integration)
    denial_probability FLOAT,
    risk_level risk_level,
    prediction_timestamp TIMESTAMP WITH TIME ZONE,
    model_version VARCHAR(50),
    top_risk_factors JSONB,
    recommended_actions JSONB,
    shap_values JSONB,
    
    -- Denial Information
    is_denied BOOLEAN DEFAULT FALSE,
    denial_date TIMESTAMP WITH TIME ZONE,
    denial_codes JSONB,
    denial_reason TEXT,
    
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
    
    -- Outcome and decision
    outcome fhir_outcome NOT NULL,
    decision JSONB, -- CodeableConcept
    disposition VARCHAR(500),
    
    -- Administrative
    pre_auth_ref VARCHAR(255),
    pre_auth_period JSONB, -- Period
    event JSONB, -- Array of events
    payee_type JSONB, -- CodeableConcept
    
    -- Clinical
    encounter JSONB, -- Array of References
    diagnosis_related_group JSONB, -- CodeableConcept
    
    -- Financial
    item JSONB, -- Array of response items
    add_item JSONB, -- Array of added items
    adjudication JSONB, -- Array of adjudications
    total JSONB, -- Array of totals
    payment JSONB, -- Payment information
    funds_reserve JSONB, -- CodeableConcept
    
    -- Documentation
    form_code JSONB, -- CodeableConcept
    form JSONB, -- Attachment
    process_note JSONB, -- Array of notes
    communication_request JSONB, -- Array of References
    insurance JSONB, -- Array of insurance info
    error JSONB, -- Array of errors
    
    -- Timestamps
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
    
    -- References
    patient_id VARCHAR(255) NOT NULL,
    billable_period JSONB, -- Period
    created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    enterer_id VARCHAR(255),
    insurer_id VARCHAR(255) NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    
    -- Administrative
    priority JSONB, -- CodeableConcept
    funds_reserve_requested JSONB, -- CodeableConcept
    funds_reserve JSONB, -- CodeableConcept
    related JSONB, -- Array of related claims
    prescription_id VARCHAR(255),
    original_prescription_id VARCHAR(255),
    event JSONB, -- Array of events
    payee JSONB, -- Payee information
    referral_id VARCHAR(255),
    encounter JSONB, -- Array of References
    facility_id VARCHAR(255),
    claim_id VARCHAR(36) REFERENCES claims(id) ON DELETE SET NULL,
    claim_response_id VARCHAR(36) REFERENCES claim_responses(id) ON DELETE SET NULL,
    
    -- Outcome and decision
    outcome fhir_outcome NOT NULL,
    decision JSONB, -- CodeableConcept
    disposition VARCHAR(500),
    pre_auth_ref JSONB, -- Array of strings
    pre_auth_ref_period JSONB, -- Array of Periods
    diagnosis_related_group JSONB, -- CodeableConcept
    
    -- Clinical
    care_team JSONB, -- Array of care team
    supporting_info JSONB, -- Array of supporting info
    diagnosis JSONB, -- Array of diagnoses
    procedure JSONB, -- Array of procedures
    precedence INTEGER,
    
    -- Financial
    insurance JSONB NOT NULL, -- Array of insurance
    accident JSONB, -- Accident information
    patient_paid JSONB, -- Money
    item JSONB, -- Array of items
    add_item JSONB, -- Array of added items
    adjudication JSONB, -- Array of adjudications
    total JSONB, -- Array of totals
    payment JSONB, -- Payment information
    form_code JSONB, -- CodeableConcept
    form JSONB, -- Attachment
    process_note JSONB, -- Array of notes
    benefit_period JSONB, -- Period
    benefit_balance JSONB, -- Array of benefit balances
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Coverage table - FHIR Coverage resource
CREATE TABLE coverages (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    resource_type VARCHAR(50) DEFAULT 'Coverage' NOT NULL,
    
    -- Core identifiers
    identifier JSONB, -- Array of identifiers
    status fhir_status NOT NULL,
    kind coverage_kind,
    payment_by JSONB, -- Array of payment responsibility
    type JSONB, -- CodeableConcept
    policy_holder_id VARCHAR(255),
    subscriber_id_ref VARCHAR(255),
    subscriber_id JSONB, -- Array with extensions
    beneficiary_id VARCHAR(255) NOT NULL,
    dependent VARCHAR(255),
    relationship JSONB, -- CodeableConcept
    period JSONB, -- Period
    insurer_id VARCHAR(255) NOT NULL,
    class_info JSONB, -- Array of class information
    order_num INTEGER,
    network VARCHAR(255),
    cost_to_beneficiary JSONB, -- Array of costs
    subrogation BOOLEAN,
    contract JSONB, -- Array of References
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced Predictions table for ML predictions
CREATE TABLE predictions (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    claim_id VARCHAR(36) REFERENCES claims(id) ON DELETE CASCADE,
    model_version VARCHAR(50) NOT NULL,
    denial_probability FLOAT NOT NULL CHECK (denial_probability >= 0 AND denial_probability <= 1),
    risk_level risk_level NOT NULL,
    top_risk_factors JSONB,
    recommended_actions JSONB,
    shap_values JSONB,
    prediction_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actual_outcome BOOLEAN,
    feedback_received BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced Denial Records table
CREATE TABLE denial_records (
    id SERIAL PRIMARY KEY,
    claim_id VARCHAR(36) UNIQUE REFERENCES claims(id) ON DELETE CASCADE,
    denial_date TIMESTAMP WITH TIME ZONE NOT NULL,
    denial_codes JSONB,
    denial_reason_text TEXT,
    classification_result JSONB,
    resolution_status resolution_status DEFAULT 'pending',
    workflow_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Remediation Actions table
CREATE TABLE remediation_actions (
    id SERIAL PRIMARY KEY,
    denial_record_id INTEGER REFERENCES denial_records(id) ON DELETE CASCADE,
    action_type VARCHAR(100) NOT NULL,
    action_data JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    success_probability FLOAT,
    executed_at TIMESTAMP WITH TIME ZONE,
    result JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Model Versions table for tracking ML models
CREATE TABLE model_versions (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    mlflow_run_id VARCHAR(100),
    performance_metrics JSONB,
    training_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Feature Store table for caching computed features
CREATE TABLE feature_store (
    id SERIAL PRIMARY KEY,
    entity_key VARCHAR(255) NOT NULL, -- e.g., "provider_id:PROV_123"
    feature_name VARCHAR(100) NOT NULL,
    feature_value FLOAT NOT NULL,
    computed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(entity_key, feature_name)
);

-- Audit Log table for compliance
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(100),
    details JSONB,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_claims_patient_id ON claims(patient_id);
CREATE INDEX idx_claims_status ON claims(status);
CREATE INDEX idx_claims_insurer_id ON claims(insurer_id);
CREATE INDEX idx_claims_provider_id ON claims(provider_id);
CREATE INDEX idx_claims_created_at ON claims(created_at);
CREATE INDEX idx_claims_use ON claims(use);
CREATE INDEX idx_claims_denial_probability ON claims(denial_probability);
CREATE INDEX idx_claims_risk_level ON claims(risk_level);
CREATE INDEX idx_claims_is_denied ON claims(is_denied);

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

CREATE INDEX idx_predictions_claim_id ON predictions(claim_id);
CREATE INDEX idx_predictions_model_version ON predictions(model_version);
CREATE INDEX idx_predictions_denial_probability ON predictions(denial_probability);
CREATE INDEX idx_predictions_risk_level ON predictions(risk_level);
CREATE INDEX idx_predictions_timestamp ON predictions(prediction_timestamp);

CREATE INDEX idx_denial_records_claim_id ON denial_records(claim_id);
CREATE INDEX idx_denial_records_resolution_status ON denial_records(resolution_status);
CREATE INDEX idx_denial_records_denial_date ON denial_records(denial_date);

CREATE INDEX idx_feature_store_entity_key ON feature_store(entity_key);
CREATE INDEX idx_feature_store_expires_at ON feature_store(expires_at);

CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_resource_type ON audit_log(resource_type);

-- Create GIN indexes for JSON fields
CREATE INDEX idx_claims_identifier_gin ON claims USING GIN (identifier);
CREATE INDEX idx_claims_type_gin ON claims USING GIN (type);
CREATE INDEX idx_claims_diagnosis_gin ON claims USING GIN (diagnosis);
CREATE INDEX idx_claims_item_gin ON claims USING GIN (item);
CREATE INDEX idx_claims_top_risk_factors_gin ON claims USING GIN (top_risk_factors);
CREATE INDEX idx_claims_denial_codes_gin ON claims USING GIN (denial_codes);

CREATE INDEX idx_claim_responses_adjudication_gin ON claim_responses USING GIN (adjudication);
CREATE INDEX idx_claim_responses_item_gin ON claim_responses USING GIN (item);

CREATE INDEX idx_coverages_type_gin ON coverages USING GIN (type);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
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

CREATE TRIGGER update_denial_records_updated_at 
    BEFORE UPDATE ON denial_records 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create useful views
CREATE VIEW active_claims AS
SELECT 
    c.*,
    p.denial_probability,
    p.risk_level,
    p.model_version,
    p.prediction_timestamp
FROM claims c
LEFT JOIN predictions p ON c.id = p.claim_id
WHERE c.status = 'active'
ORDER BY c.created_at DESC;

CREATE VIEW claim_summary AS
SELECT 
    status,
    COUNT(*) as total_claims,
    AVG(COALESCE(denial_probability, 0)) as avg_denial_probability,
    COUNT(CASE WHEN is_denied THEN 1 END) as denied_claims,
    COUNT(CASE WHEN risk_level = 'HIGH' THEN 1 END) as high_risk_claims
FROM claims
GROUP BY status;

CREATE VIEW prediction_performance AS
SELECT 
    model_version,
    COUNT(*) as total_predictions,
    AVG(denial_probability) as avg_prediction,
    COUNT(CASE WHEN actual_outcome IS NOT NULL THEN 1 END) as feedback_count,
    COUNT(CASE WHEN actual_outcome = TRUE THEN 1 END) as actual_denials
FROM predictions
GROUP BY model_version
ORDER BY total_predictions DESC;

-- Insert sample data for testing
INSERT INTO model_versions (model_name, version, is_active, performance_metrics) VALUES
('denial_predictor', 'v1.0.0', TRUE, '{"accuracy": 0.85, "precision": 0.82, "recall": 0.78, "f1_score": 0.80}'),
('denial_classifier', 'v1.0.0', TRUE, '{"accuracy": 0.88, "precision": 0.85, "recall": 0.83, "f1_score": 0.84}');

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fhir_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fhir_user; 
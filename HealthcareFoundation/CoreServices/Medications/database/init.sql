-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- FHIR Medication Resource
-- ============================================================================
CREATE TABLE medications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,

    -- Code (medication)
    code JSONB, -- CodeableConcept (RxNorm, NDC, etc.)

    -- Status
    status VARCHAR(50) CHECK (status IN ('active', 'inactive', 'entered-in-error')),

    -- Manufacturer
    manufacturer UUID,

    -- Form
    form JSONB, -- CodeableConcept

    -- Amount
    amount JSONB, -- Ratio object

    -- Ingredients
    ingredients JSONB, -- Array of ingredient objects

    -- Batch
    batch JSONB, -- Batch object

    -- FHIR Metadata
    fhir_resource JSONB,

    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FHIR MedicationRequest Resource
-- ============================================================================
CREATE TABLE medication_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,

    -- Status
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'active', 'on-hold', 'cancelled', 'completed',
        'entered-in-error', 'stopped', 'draft', 'unknown'
    )),

    -- Intent
    intent VARCHAR(50) NOT NULL CHECK (intent IN (
        'proposal', 'plan', 'order', 'original-order',
        'reflex-order', 'filler-order', 'instance-order', 'option'
    )),

    -- Category
    category JSONB, -- Array of CodeableConcept

    -- Priority
    priority VARCHAR(50) CHECK (priority IN ('routine', 'urgent', 'asap', 'stat')),

    -- Do Not Perform
    do_not_perform BOOLEAN DEFAULT FALSE,

    -- Reported
    reported_boolean BOOLEAN,
    reported_reference UUID,

    -- Medication (reference or CodeableConcept)
    medication_id UUID,
    medication_codeable_concept JSONB,

    -- Subject (patient)
    subject_patient_id UUID NOT NULL,

    -- Encounter
    encounter_id UUID,

    -- Supporting Information
    supporting_information JSONB, -- Array of references

    -- Authored On
    authored_on TIMESTAMP WITH TIME ZONE,

    -- Requester
    requester UUID,

    -- Performer
    performer UUID,
    performer_type JSONB, -- CodeableConcept

    -- Recorder
    recorder UUID,

    -- Reason Code
    reason_codes JSONB, -- Array of CodeableConcept

    -- Reason Reference
    reason_references JSONB, -- Array of references

    -- Instantiates Canonical
    instantiates_canonical TEXT[],

    -- Instantiates Uri
    instantiates_uri TEXT[],

    -- Based On
    based_on JSONB, -- Array of references

    -- Group Identifier
    group_identifier JSONB, -- Identifier object

    -- Course of Therapy Type
    course_of_therapy_type JSONB, -- CodeableConcept

    -- Insurance
    insurance JSONB, -- Array of references

    -- Notes
    notes JSONB, -- Array of Annotation

    -- Dosage Instructions
    dosage_instructions JSONB, -- Array of Dosage objects

    -- Dispense Request
    dispense_request JSONB, -- Dispense request object

    -- Substitution
    substitution JSONB, -- Substitution object

    -- Prior Prescription
    prior_prescription UUID,

    -- Detection Issue
    detection_issue JSONB, -- Array of references

    -- Event History
    event_history JSONB, -- Array of references

    -- FHIR Metadata
    fhir_resource JSONB,

    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Keys (removed to make it self-contained)
    -- FOREIGN KEY (medication_id) REFERENCES medications(id),
    -- FOREIGN KEY (prior_prescription) REFERENCES medication_requests(id)

    -- Self-referencing foreign key for prior prescription
    CONSTRAINT fk_prior_prescription FOREIGN KEY (prior_prescription) REFERENCES medication_requests(id)
);

-- Create indexes for better performance
CREATE INDEX idx_medications_fhir_id ON medications(fhir_id);
CREATE INDEX idx_medications_status ON medications(status);
CREATE INDEX idx_medications_created_at ON medications(created_at);

CREATE INDEX idx_medication_requests_fhir_id ON medication_requests(fhir_id);
CREATE INDEX idx_medication_requests_status ON medication_requests(status);
CREATE INDEX idx_medication_requests_intent ON medication_requests(intent);
CREATE INDEX idx_medication_requests_subject_patient_id ON medication_requests(subject_patient_id);
CREATE INDEX idx_medication_requests_medication_id ON medication_requests(medication_id);
CREATE INDEX idx_medication_requests_authored_on ON medication_requests(authored_on);
CREATE INDEX idx_medication_requests_created_at ON medication_requests(created_at);

-- Create triggers to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_medications_updated_at 
    BEFORE UPDATE ON medications 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_medication_requests_updated_at 
    BEFORE UPDATE ON medication_requests 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample medications
INSERT INTO medications (
    fhir_id, code, status, form, ingredients, batch
) VALUES 
(
    'med-001', 
    '{"text": "Lisinopril 10mg", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "314076", "display": "Lisinopril 10mg"}]}'::jsonb,
    'active',
    '{"text": "Tablet", "coding": [{"system": "http://snomed.info/sct", "code": "385055001", "display": "Tablet"}]}'::jsonb,
    '[{"item_codeable_concept": {"text": "Lisinopril", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "29046", "display": "Lisinopril"}]}, "is_active": true, "strength": {"numerator": {"value": 10, "unit": "mg"}, "denominator": {"value": 1, "unit": "tablet"}}}]'::jsonb,
    '{"lot_number": "ABC123", "expiration_date": "2025-12-31"}'::jsonb
),
(
    'med-002', 
    '{"text": "Metformin 500mg", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "860975", "display": "Metformin 500mg"}]}'::jsonb,
    'active',
    '{"text": "Tablet", "coding": [{"system": "http://snomed.info/sct", "code": "385055001", "display": "Tablet"}]}'::jsonb,
    '[{"item_codeable_concept": {"text": "Metformin hydrochloride", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "6809", "display": "Metformin"}]}, "is_active": true, "strength": {"numerator": {"value": 500, "unit": "mg"}, "denominator": {"value": 1, "unit": "tablet"}}}]'::jsonb,
    '{"lot_number": "XYZ789", "expiration_date": "2026-06-30"}'::jsonb
),
(
    'med-003', 
    '{"text": "Amoxicillin 250mg/5ml", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "308182", "display": "Amoxicillin 250mg/5ml"}]}'::jsonb,
    'active',
    '{"text": "Oral Suspension", "coding": [{"system": "http://snomed.info/sct", "code": "387048002", "display": "Oral suspension"}]}'::jsonb,
    '[{"item_codeable_concept": {"text": "Amoxicillin", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "723", "display": "Amoxicillin"}]}, "is_active": true, "strength": {"numerator": {"value": 250, "unit": "mg"}, "denominator": {"value": 5, "unit": "ml"}}}]'::jsonb,
    '{"lot_number": "DEF456", "expiration_date": "2025-03-15"}'::jsonb
);

-- Insert sample medication requests
INSERT INTO medication_requests (
    fhir_id, status, intent, priority, subject_patient_id, medication_id, 
    medication_codeable_concept, authored_on, dosage_instructions, dispense_request
) VALUES 
(
    'medreq-001',
    'active',
    'order',
    'routine',
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    (SELECT id FROM medications WHERE fhir_id = 'med-001'),
    '{"text": "Lisinopril 10mg", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "314076", "display": "Lisinopril 10mg"}]}'::jsonb,
    '2024-01-15 10:30:00+00:00',
    '[{"text": "Take 1 tablet by mouth once daily", "timing": {"repeat": {"frequency": 1, "period": 1, "periodUnit": "day"}}}]'::jsonb,
    '{"quantity": {"value": 30, "unit": "tablet"}, "expected_supply_duration": {"value": 30, "unit": "day"}}'::jsonb
),
(
    'medreq-002',
    'active',
    'order',
    'routine',
    '550e8400-e29b-41d4-a716-446655440002'::uuid,
    (SELECT id FROM medications WHERE fhir_id = 'med-002'),
    '{"text": "Metformin 500mg", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "860975", "display": "Metformin 500mg"}]}'::jsonb,
    '2024-01-16 14:15:00+00:00',
    '[{"text": "Take 1 tablet by mouth twice daily with meals", "timing": {"repeat": {"frequency": 2, "period": 1, "periodUnit": "day"}}}]'::jsonb,
    '{"quantity": {"value": 60, "unit": "tablet"}, "expected_supply_duration": {"value": 30, "unit": "day"}}'::jsonb
),
(
    'medreq-003',
    'completed',
    'order',
    'urgent',
    '550e8400-e29b-41d4-a716-446655440003'::uuid,
    (SELECT id FROM medications WHERE fhir_id = 'med-003'),
    '{"text": "Amoxicillin 250mg/5ml", "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "308182", "display": "Amoxicillin 250mg/5ml"}]}'::jsonb,
    '2024-01-10 09:00:00+00:00',
    '[{"text": "Take 5ml by mouth three times daily for 10 days", "timing": {"repeat": {"frequency": 3, "period": 1, "periodUnit": "day"}}}]'::jsonb,
    '{"quantity": {"value": 150, "unit": "ml"}, "expected_supply_duration": {"value": 10, "unit": "day"}}'::jsonb
);

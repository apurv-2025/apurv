-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create patients table (simplified for demo)
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create encounters table (simplified for demo)
CREATE TABLE IF NOT EXISTS encounters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(id),
    encounter_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- FHIR AllergyIntolerance Resource
CREATE TABLE allergy_intolerances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Clinical Status
    clinical_status VARCHAR(50) CHECK (clinical_status IN (
        'active', 'inactive', 'resolved'
    )),
    
    -- Verification Status
    verification_status VARCHAR(50) CHECK (verification_status IN (
        'unconfirmed', 'confirmed', 'refuted', 'entered-in-error'
    )),
    
    -- Type
    type VARCHAR(50) CHECK (type IN ('allergy', 'intolerance')),
    
    -- Category
    categories TEXT[] CHECK (array_length(categories, 1) IS NULL OR 
        categories <@ ARRAY['food', 'medication', 'environment', 'biologic']),
    
    -- Criticality
    criticality VARCHAR(50) CHECK (criticality IN ('low', 'high', 'unable-to-assess')),
    
    -- Code (substance)
    code JSONB, -- CodeableConcept
    
    -- Patient
    patient_id UUID NOT NULL,
    
    -- Encounter
    encounter_id UUID,
    
    -- Onset
    onset_date_time TIMESTAMP WITH TIME ZONE,
    onset_age JSONB,
    onset_period JSONB,
    onset_range JSONB,
    onset_string VARCHAR(500),
    
    -- Recorded Date
    recorded_date TIMESTAMP WITH TIME ZONE,
    
    -- Recorder
    recorder UUID,
    
    -- Asserter
    asserter UUID,
    
    -- Last Occurrence
    last_occurrence TIMESTAMP WITH TIME ZONE,
    
    -- Notes
    notes JSONB, -- Array of Annotation
    
    -- Reactions
    reactions JSONB, -- Array of reaction objects
    
    -- FHIR Metadata
    fhir_resource JSONB,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(id)
);

-- Indexes
CREATE INDEX idx_allergies_fhir_id ON allergy_intolerances(fhir_id);
CREATE INDEX idx_allergies_patient ON allergy_intolerances(patient_id);
CREATE INDEX idx_allergies_code ON allergy_intolerances USING GIN(code);
CREATE INDEX idx_allergies_clinical_status ON allergy_intolerances(clinical_status);

-- Insert sample patients
INSERT INTO patients (id, name) VALUES 
    ('550e8400-e29b-41d4-a716-446655440001', 'John Doe'),
    ('550e8400-e29b-41d4-a716-446655440002', 'Jane Smith'),
    ('550e8400-e29b-41d4-a716-446655440003', 'Bob Johnson');

-- Insert sample allergies
INSERT INTO allergy_intolerances (
    fhir_id, clinical_status, verification_status, type, categories, criticality,
    code, patient_id, onset_string, recorded_date
) VALUES 
    (
        'allergy-001', 'active', 'confirmed', 'allergy', ARRAY['food'], 'high',
        '{"text": "Peanuts", "coding": [{"system": "http://snomed.info/sct", "code": "256349002", "display": "Peanut"}]}',
        '550e8400-e29b-41d4-a716-446655440001', 'Since childhood', CURRENT_TIMESTAMP
    ),
    (
        'allergy-002', 'active', 'confirmed', 'allergy', ARRAY['medication'], 'high',
        '{"text": "Penicillin", "coding": [{"system": "http://snomed.info/sct", "code": "387517004", "display": "Penicillin"}]}',
        '550e8400-e29b-41d4-a716-446655440002', 'Discovered in 2020', CURRENT_TIMESTAMP
    ),
    (
        'intolerance-001', 'active', 'confirmed', 'intolerance', ARRAY['food'], 'low',
        '{"text": "Lactose", "coding": [{"system": "http://snomed.info/sct", "code": "226529007", "display": "Lactose"}]}',
        '550e8400-e29b-41d4-a716-446655440003', 'Adult onset', CURRENT_TIMESTAMP
    );

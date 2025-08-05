-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create patients table (referenced by other tables)
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    name JSONB,
    gender VARCHAR(10),
    birth_date DATE,
    address JSONB,
    telecom JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create organizations table (referenced by encounters)
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    name VARCHAR(255),
    type JSONB,
    address JSONB,
    telecom JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FHIR Encounter Resource
-- ============================================================================
CREATE TABLE IF NOT EXISTS encounters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Status
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'planned', 'arrived', 'triaged', 'in-progress', 'onleave', 
        'finished', 'cancelled', 'entered-in-error', 'unknown'
    )),
    
    -- Class (inpatient, outpatient, emergency, etc.)
    class JSONB, -- Coding object
    
    -- Type of encounter
    type JSONB, -- Array of CodeableConcept
    
    -- Service Type
    service_type JSONB, -- CodeableConcept
    
    -- Priority
    priority JSONB, -- CodeableConcept
    
    -- Subject (patient)
    subject_patient_id UUID NOT NULL,
    
    -- Episode of Care
    episode_of_care JSONB,
    
    -- Incoming Referral
    incoming_referral JSONB,
    
    -- Participants (practitioners, etc.)
    participants JSONB, -- Array of participant objects
    
    -- Appointment
    appointment UUID,
    
    -- Period
    period_start TIMESTAMP WITH TIME ZONE,
    period_end TIMESTAMP WITH TIME ZONE,
    
    -- Length of encounter
    length_value DECIMAL,
    length_unit VARCHAR(50),
    
    -- Reason for encounter
    reason_code JSONB, -- Array of CodeableConcept
    reason_reference JSONB, -- Array of references
    
    -- Diagnosis
    diagnosis JSONB, -- Array of diagnosis objects
    
    -- Account
    account JSONB,
    
    -- Hospitalization details
    hospitalization JSONB,
    
    -- Location
    locations JSONB, -- Array of location objects
    
    -- Service Provider
    service_provider UUID,
    
    -- Part of (parent encounter)
    part_of UUID,
    
    -- FHIR Metadata
    fhir_resource JSONB,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (subject_patient_id) REFERENCES patients(id),
    FOREIGN KEY (service_provider) REFERENCES organizations(id),
    FOREIGN KEY (part_of) REFERENCES encounters(id)
);

-- ============================================================================
-- FHIR Observation Resource
-- ============================================================================
CREATE TABLE IF NOT EXISTS observations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Status
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'registered', 'preliminary', 'final', 'amended', 
        'corrected', 'cancelled', 'entered-in-error', 'unknown'
    )),
    
    -- Category
    category JSONB, -- Array of CodeableConcept
    
    -- Code (what was observed)
    code JSONB NOT NULL, -- CodeableConcept (LOINC, SNOMED, etc.)
    
    -- Subject (patient)
    subject_patient_id UUID NOT NULL,
    
    -- Encounter
    encounter_id UUID,
    
    -- Effective time
    effective_date_time TIMESTAMP WITH TIME ZONE,
    effective_period_start TIMESTAMP WITH TIME ZONE,
    effective_period_end TIMESTAMP WITH TIME ZONE,
    effective_instant TIMESTAMP WITH TIME ZONE,
    
    -- Issued (when result made available)
    issued TIMESTAMP WITH TIME ZONE,
    
    -- Performer
    performers JSONB, -- Array of references
    
    -- Value (the result)
    value_quantity_value DECIMAL,
    value_quantity_unit VARCHAR(100),
    value_quantity_system VARCHAR(500),
    value_quantity_code VARCHAR(100),
    value_codeable_concept JSONB,
    value_string TEXT,
    value_boolean BOOLEAN,
    value_integer INTEGER,
    value_range JSONB,
    value_ratio JSONB,
    value_sampled_data JSONB,
    value_time TIME,
    value_date_time TIMESTAMP WITH TIME ZONE,
    value_period JSONB,
    
    -- Data absent reason
    data_absent_reason JSONB,
    
    -- Interpretation
    interpretation JSONB, -- Array of CodeableConcept
    
    -- Notes
    notes JSONB, -- Array of Annotation
    
    -- Body Site
    body_site JSONB, -- CodeableConcept
    
    -- Method
    method JSONB, -- CodeableConcept
    
    -- Specimen
    specimen UUID,
    
    -- Device
    device UUID,
    
    -- Reference Range
    reference_ranges JSONB, -- Array of reference range objects
    
    -- Has Member (for group observations)
    has_member JSONB, -- Array of references
    
    -- Derived From
    derived_from JSONB, -- Array of references
    
    -- Components (for multi-component observations)
    components JSONB, -- Array of component objects
    
    -- FHIR Metadata
    fhir_resource JSONB,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (subject_patient_id) REFERENCES patients(id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(id)
);

-- ============================================================================
-- FHIR Condition Resource
-- ============================================================================
CREATE TABLE IF NOT EXISTS conditions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Clinical Status
    clinical_status VARCHAR(50) CHECK (clinical_status IN (
        'active', 'recurrence', 'relapse', 'inactive', 
        'remission', 'resolved', 'unknown'
    )),
    
    -- Verification Status
    verification_status VARCHAR(50) CHECK (verification_status IN (
        'unconfirmed', 'provisional', 'differential', 
        'confirmed', 'refuted', 'entered-in-error'
    )),
    
    -- Category
    category JSONB, -- Array of CodeableConcept
    
    -- Severity
    severity JSONB, -- CodeableConcept
    
    -- Code (the condition)
    code JSONB, -- CodeableConcept (ICD-10, SNOMED)
    
    -- Body Site
    body_sites JSONB, -- Array of CodeableConcept
    
    -- Subject (patient)
    subject_patient_id UUID NOT NULL,
    
    -- Encounter
    encounter_id UUID,
    
    -- Onset
    onset_date_time TIMESTAMP WITH TIME ZONE,
    onset_age JSONB, -- Age object
    onset_period JSONB, -- Period object
    onset_range JSONB, -- Range object
    onset_string VARCHAR(500),
    
    -- Abatement
    abatement_date_time TIMESTAMP WITH TIME ZONE,
    abatement_age JSONB,
    abatement_period JSONB,
    abatement_range JSONB,
    abatement_string VARCHAR(500),
    abatement_boolean BOOLEAN,
    
    -- Recorded Date
    recorded_date DATE,
    
    -- Recorder
    recorder UUID,
    
    -- Asserter
    asserter UUID,
    
    -- Stage
    stages JSONB, -- Array of stage objects
    
    -- Evidence
    evidence JSONB, -- Array of evidence objects
    
    -- Notes
    notes JSONB, -- Array of Annotation
    
    -- FHIR Metadata
    fhir_resource JSONB,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (subject_patient_id) REFERENCES patients(id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(id)
);

-- Create Indexes
CREATE INDEX IF NOT EXISTS idx_encounters_fhir_id ON encounters(fhir_id);
CREATE INDEX IF NOT EXISTS idx_encounters_patient ON encounters(subject_patient_id);
CREATE INDEX IF NOT EXISTS idx_encounters_status ON encounters(status);
CREATE INDEX IF NOT EXISTS idx_encounters_period ON encounters(period_start, period_end);

CREATE INDEX IF NOT EXISTS idx_observations_fhir_id ON observations(fhir_id);
CREATE INDEX IF NOT EXISTS idx_observations_patient ON observations(subject_patient_id);
CREATE INDEX IF NOT EXISTS idx_observations_encounter ON observations(encounter_id);
CREATE INDEX IF NOT EXISTS idx_observations_effective ON observations(effective_date_time);
CREATE INDEX IF NOT EXISTS idx_observations_status ON observations(status);

-- Insert sample data
INSERT INTO patients (fhir_id, name, gender, birth_date) VALUES 
('patient-001', '{"given": ["John"], "family": "Doe"}', 'male', '1980-01-01'),
('patient-002', '{"given": ["Jane"], "family": "Smith"}', 'female', '1975-05-15'),
('patient-003', '{"given": ["Bob"], "family": "Johnson"}', 'male', '1990-12-10')
ON CONFLICT (fhir_id) DO NOTHING;

INSERT INTO organizations (fhir_id, name, type) VALUES 
('org-001', 'General Hospital', '{"coding": [{"code": "prov", "display": "Healthcare Provider"}]}'),
('org-002', 'City Clinic', '{"coding": [{"code": "prov", "display": "Healthcare Provider"}]}')
ON CONFLICT (fhir_id) DO NOTHING;

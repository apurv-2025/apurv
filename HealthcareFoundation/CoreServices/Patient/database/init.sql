-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- FHIR Patient Resource
-- ============================================================================
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,

    -- Demographics
    family_name VARCHAR(255),
    given_names TEXT[], -- Array for multiple given names
    prefix VARCHAR(50),
    suffix VARCHAR(50),

    -- Identifiers (SSN, MRN, etc.)
    identifiers JSONB, -- Array of identifier objects

    -- Contact Information
    telecom JSONB, -- Phone, email, etc.
    addresses JSONB, -- Array of address objects

    -- Basic Demographics
    gender VARCHAR(20) CHECK (gender IN ('male', 'female', 'other', 'unknown')),
    birth_date DATE,
    deceased_boolean BOOLEAN DEFAULT FALSE,
    deceased_date_time TIMESTAMP WITH TIME ZONE,

    -- Marital Status
    marital_status_code VARCHAR(50),
    marital_status_display VARCHAR(100),

    -- Communication
    communication JSONB, -- Languages, preferences

    -- General Practitioner
    general_practitioner JSONB, -- Array of practitioner references

    -- Managing Organization
    managing_organization UUID,

    -- Photo
    photo JSONB, -- Array of attachment objects

    -- Links to other patients
    links JSONB,

    -- Active status
    active BOOLEAN DEFAULT TRUE,

    -- FHIR Metadata
    fhir_resource JSONB, -- Complete FHIR resource

    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_patients_fhir_id ON patients(fhir_id);
CREATE INDEX idx_patients_family_name ON patients(family_name);
CREATE INDEX idx_patients_given_names ON patients USING GIN(given_names);
CREATE INDEX idx_patients_active ON patients(active);
CREATE INDEX idx_patients_gender ON patients(gender);
CREATE INDEX idx_patients_birth_date ON patients(birth_date);
CREATE INDEX idx_patients_created_at ON patients(created_at);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_patients_updated_at 
    BEFORE UPDATE ON patients 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO patients (
    fhir_id, family_name, given_names, gender, birth_date, 
    telecom, addresses, active
) VALUES 
(
    'patient-001', 
    'Smith', 
    ARRAY['John', 'Michael'], 
    'male', 
    '1985-03-15',
    '[{"system": "phone", "value": "+1-555-0123", "use": "home"}]'::jsonb,
    '[{"use": "home", "line": ["123 Main St"], "city": "Boston", "state": "MA", "postal_code": "02101", "country": "USA"}]'::jsonb,
    true
),
(
    'patient-002', 
    'Johnson', 
    ARRAY['Sarah', 'Anne'], 
    'female', 
    '1990-07-22',
    '[{"system": "email", "value": "sarah.johnson@email.com", "use": "home"}, {"system": "phone", "value": "+1-555-0456", "use": "mobile"}]'::jsonb,
    '[{"use": "home", "line": ["456 Oak Ave"], "city": "Cambridge", "state": "MA", "postal_code": "02139", "country": "USA"}]'::jsonb,
    true
),
(
    'patient-003', 
    'Williams', 
    ARRAY['Robert'], 
    'male', 
    '1978-12-03',
    '[{"system": "phone", "value": "+1-555-0789", "use": "work"}]'::jsonb,
    '[{"use": "work", "line": ["789 Business Blvd", "Suite 100"], "city": "Somerville", "state": "MA", "postal_code": "02143", "country": "USA"}]'::jsonb,
    true
);

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

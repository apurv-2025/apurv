-- ChargeCapture Database Schema
-- This file contains the complete database schema for the Charge Capture System

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create providers table
CREATE TABLE providers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    npi VARCHAR(10) UNIQUE NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create patients table
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth TIMESTAMP NOT NULL,
    mrn VARCHAR(50) UNIQUE NOT NULL,  -- Medical Record Number
    insurance_info JSONB,  -- Store insurance details as JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create encounters table
CREATE TABLE encounters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    provider_id UUID NOT NULL REFERENCES providers(id),
    encounter_date TIMESTAMP NOT NULL,
    encounter_type VARCHAR(50) NOT NULL,  -- office_visit, procedure, consultation, etc.
    status VARCHAR(20) DEFAULT 'scheduled',  -- scheduled, in_progress, completed, cancelled
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create charges table
CREATE TABLE charges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    encounter_id UUID NOT NULL REFERENCES encounters(id),
    patient_id UUID NOT NULL REFERENCES patients(id),
    provider_id UUID NOT NULL REFERENCES providers(id),
    
    -- Charge details
    cpt_code VARCHAR(10) NOT NULL,
    cpt_description VARCHAR(255),
    icd_code VARCHAR(10) NOT NULL,
    icd_description VARCHAR(255),
    hcpcs_code VARCHAR(10),
    
    -- Modifiers and quantities
    modifiers JSONB,  -- Array of modifier codes
    units INTEGER DEFAULT 1,
    quantity INTEGER DEFAULT 1,
    charge_amount NUMERIC(10, 2),
    
    -- Status and workflow
    status VARCHAR(20) DEFAULT 'draft',  -- draft, submitted, billed, rejected, paid
    capture_method VARCHAR(20),  -- point_of_care, post_encounter, batch
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    captured_by UUID REFERENCES providers(id),
    
    -- Billing integration
    claim_id VARCHAR(50),  -- Reference to billing system
    submitted_to_billing_at TIMESTAMP,
    
    -- Compliance and audit
    validation_errors JSONB,  -- Store validation issues
    audit_log JSONB,  -- Track changes
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create charge_templates table
CREATE TABLE charge_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    provider_id UUID REFERENCES providers(id),  -- NULL for system-wide templates
    
    -- Template configuration
    template_data JSONB NOT NULL,  -- Store template structure
    is_active BOOLEAN DEFAULT TRUE,
    is_system_template BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create charge_validation_rules table
CREATE TABLE charge_validation_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_name VARCHAR(100) NOT NULL,
    rule_type VARCHAR(50) NOT NULL,  -- code_combination, payer_specific, etc.
    specialty VARCHAR(100),  -- NULL for all specialties
    payer VARCHAR(100),  -- NULL for all payers
    
    rule_config JSONB NOT NULL,  -- Store rule logic
    is_active BOOLEAN DEFAULT TRUE,
    error_message VARCHAR(255),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX ix_charges_encounter_id ON charges(encounter_id);
CREATE INDEX ix_charges_patient_id ON charges(patient_id);
CREATE INDEX ix_charges_provider_id ON charges(provider_id);
CREATE INDEX ix_charges_status ON charges(status);
CREATE INDEX ix_charges_captured_at ON charges(captured_at);
CREATE INDEX ix_encounters_date ON encounters(encounter_date);
CREATE INDEX ix_encounters_provider ON encounters(provider_id);

-- Create indexes for JSONB columns for better query performance
CREATE INDEX ix_patients_insurance_info ON patients USING GIN (insurance_info);
CREATE INDEX ix_charges_modifiers ON charges USING GIN (modifiers);
CREATE INDEX ix_charges_validation_errors ON charges USING GIN (validation_errors);
CREATE INDEX ix_charges_audit_log ON charges USING GIN (audit_log);
CREATE INDEX ix_charge_templates_template_data ON charge_templates USING GIN (template_data);
CREATE INDEX ix_charge_validation_rules_rule_config ON charge_validation_rules USING GIN (rule_config);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables with updated_at column
CREATE TRIGGER update_charges_updated_at BEFORE UPDATE ON charges
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_charge_templates_updated_at BEFORE UPDATE ON charge_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing
INSERT INTO providers (first_name, last_name, npi, specialty) VALUES
('John', 'Smith', '1234567890', 'Cardiology'),
('Sarah', 'Johnson', '0987654321', 'Orthopedics'),
('Michael', 'Brown', '1122334455', 'Primary Care');

INSERT INTO patients (first_name, last_name, date_of_birth, mrn, insurance_info) VALUES
('Alice', 'Wilson', '1985-03-15', 'MRN001', '{"provider": "Blue Cross", "policy_number": "BC123456"}'),
('Bob', 'Davis', '1978-07-22', 'MRN002', '{"provider": "Aetna", "policy_number": "AE789012"}'),
('Carol', 'Miller', '1992-11-08', 'MRN003', '{"provider": "Cigna", "policy_number": "CG345678"}');

INSERT INTO encounters (patient_id, provider_id, encounter_date, encounter_type, status) VALUES
((SELECT id FROM patients WHERE mrn = 'MRN001'), (SELECT id FROM providers WHERE npi = '1234567890'), '2024-01-15 09:00:00', 'office_visit', 'completed'),
((SELECT id FROM patients WHERE mrn = 'MRN002'), (SELECT id FROM providers WHERE npi = '0987654321'), '2024-01-16 14:30:00', 'consultation', 'completed'),
((SELECT id FROM patients WHERE mrn = 'MRN003'), (SELECT id FROM providers WHERE npi = '1122334455'), '2024-01-17 10:15:00', 'procedure', 'scheduled');

INSERT INTO charge_templates (name, specialty, template_data, is_system_template) VALUES
('Standard Office Visit', 'Primary Care', '{"cpt_code": "99213", "icd_code": "Z00.00", "units": 1}', TRUE),
('Cardiology Consultation', 'Cardiology', '{"cpt_code": "99244", "icd_code": "I10", "units": 1}', TRUE),
('Orthopedic Procedure', 'Orthopedics', '{"cpt_code": "20610", "icd_code": "M79.3", "units": 1}', TRUE);

INSERT INTO charge_validation_rules (rule_name, rule_type, rule_config, error_message) VALUES
('CPT-ICD Combination Check', 'code_combination', '{"cpt_codes": ["99213"], "valid_icd_codes": ["Z00.00", "Z00.01"]}', 'Invalid CPT-ICD code combination'),
('Modifier Validation', 'modifier_check', '{"required_modifiers": ["25"], "cpt_codes": ["99213"]}', 'Required modifier missing'),
('Payer Specific Rules', 'payer_specific', '{"payer": "Medicare", "rules": {"max_units": 1}}', 'Exceeds payer-specific limits');

-- Grant permissions (adjust as needed for your environment)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO chargecapture_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO chargecapture_user;

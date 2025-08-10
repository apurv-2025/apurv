-- Health Insurance Verification Database Schema
-- PostgreSQL Database Initialization Script

-- Create database extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
CREATE TYPE request_type_enum AS ENUM ('00', '01', '02', '03', '04');
CREATE TYPE certification_type_enum AS ENUM ('I', 'R', 'S', 'C');
CREATE TYPE response_code_enum AS ENUM ('A1', 'A2', 'A3', 'A4', 'A6');

-- Table: service_type_codes
CREATE TABLE IF NOT EXISTS service_type_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    requires_authorization BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table: procedure_codes
CREATE TABLE IF NOT EXISTS procedure_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(500) NOT NULL,
    code_type VARCHAR(10), -- CPT, HCPCS
    category VARCHAR(100),
    requires_authorization BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table: diagnosis_codes
CREATE TABLE IF NOT EXISTS diagnosis_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table: patient_information
CREATE TABLE IF NOT EXISTS patient_information (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    date_of_birth DATE NOT NULL,
    gender VARCHAR(1) CHECK (gender IN ('M', 'F', 'U')),
    ssn VARCHAR(11), -- Encrypted in production
    
    -- Contact Information
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(10),
    zip_code VARCHAR(20),
    phone_home VARCHAR(20),
    phone_work VARCHAR(20),
    phone_mobile VARCHAR(20),
    email VARCHAR(255),
    
    -- Insurance Information
    primary_insurance JSONB,
    secondary_insurance JSONB,
    member_id_primary VARCHAR(100),
    member_id_secondary VARCHAR(100),
    
    -- Emergency Contact
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relationship VARCHAR(50),
    
    -- Medical Information
    primary_care_provider VARCHAR(255),
    allergies JSONB,
    medical_conditions JSONB,
    medications JSONB,
    
    -- EDI 275 Information
    edi_275_content TEXT,
    last_edi_update TIMESTAMP WITH TIME ZONE,
    
    -- Consent and Privacy
    hipaa_authorization BOOLEAN DEFAULT FALSE,
    consent_date TIMESTAMP WITH TIME ZONE,
    privacy_preferences JSONB,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    -- Indexes
    CONSTRAINT idx_patient_member_id_primary UNIQUE (member_id_primary)
);

-- Table: prior_authorization_requests
CREATE TABLE IF NOT EXISTS prior_authorization_requests (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Patient Information
    patient_id VARCHAR(100) NOT NULL,
    patient_first_name VARCHAR(100) NOT NULL,
    patient_last_name VARCHAR(100) NOT NULL,
    patient_dob DATE NOT NULL,
    patient_gender VARCHAR(1) CHECK (patient_gender IN ('M', 'F', 'U')),
    member_id VARCHAR(100) NOT NULL,
    
    -- Provider Information
    requesting_provider_npi VARCHAR(20) NOT NULL,
    requesting_provider_name VARCHAR(255),
    servicing_provider_npi VARCHAR(20),
    servicing_provider_name VARCHAR(255),
    
    -- Authorization Details
    request_type request_type_enum NOT NULL,
    certification_type certification_type_enum NOT NULL,
    service_type_code VARCHAR(10),
    
    -- Service Information
    procedure_codes JSONB, -- Array of CPT/HCPCS codes
    diagnosis_codes JSONB, -- Array of ICD-10 codes
    service_date_from DATE,
    service_date_to DATE,
    units_requested INTEGER,
    
    -- Clinical Information
    clinical_information TEXT,
    medical_necessity TEXT,
    supporting_documentation JSONB, -- Attachments metadata
    
    -- Request Status
    status VARCHAR(20) DEFAULT 'submitted',
    priority VARCHAR(10) DEFAULT 'normal' CHECK (priority IN ('normal', 'urgent', 'emergency')),
    
    -- EDI Content
    edi_278_content TEXT NOT NULL,
    
    -- Tracking Information
    submitter_id VARCHAR(50),
    receiver_id VARCHAR(50),
    interchange_control_number VARCHAR(20),
    group_control_number VARCHAR(20),
    transaction_control_number VARCHAR(20),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    -- Foreign Keys
    FOREIGN KEY (patient_id) REFERENCES patient_information(patient_id)
);

-- Table: prior_authorization_responses
CREATE TABLE IF NOT EXISTS prior_authorization_responses (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) NOT NULL,
    
    -- Response Details
    response_code response_code_enum NOT NULL,
    authorization_number VARCHAR(50),
    effective_date DATE,
    expiration_date DATE,
    
    -- Approved Services
    approved_services JSONB, -- Details of approved services
    units_approved INTEGER,
    units_used INTEGER DEFAULT 0,
    
    -- Decision Information
    decision_reason TEXT,
    reviewer_name VARCHAR(255),
    review_date TIMESTAMP WITH TIME ZONE,
    
    -- Additional Requirements
    additional_information_required TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    
    -- EDI Content
    edi_278_response_content TEXT NOT NULL,
    
    -- Processing Information
    processing_time_ms INTEGER,
    payer_id VARCHAR(50),
    payer_name VARCHAR(255),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    -- Foreign Keys
    FOREIGN KEY (request_id) REFERENCES prior_authorization_requests(request_id)
);

-- Table: authorization_audit
CREATE TABLE IF NOT EXISTS authorization_audit (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL, -- submitted, reviewed, approved, etc.
    actor VARCHAR(255), -- User who performed action
    notes TEXT,
    previous_status VARCHAR(20),
    new_status VARCHAR(20),
    metadata JSONB, -- Additional action metadata
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_patient_info_patient_id ON patient_information(patient_id);
CREATE INDEX IF NOT EXISTS idx_patient_info_member_id ON patient_information(member_id_primary);
CREATE INDEX IF NOT EXISTS idx_patient_info_dob ON patient_information(date_of_birth);

CREATE INDEX IF NOT EXISTS idx_prior_auth_req_request_id ON prior_authorization_requests(request_id);
CREATE INDEX IF NOT EXISTS idx_prior_auth_req_patient_id ON prior_authorization_requests(patient_id);
CREATE INDEX IF NOT EXISTS idx_prior_auth_req_member_id ON prior_authorization_requests(member_id);
CREATE INDEX IF NOT EXISTS idx_prior_auth_req_status ON prior_authorization_requests(status);
CREATE INDEX IF NOT EXISTS idx_prior_auth_req_provider_npi ON prior_authorization_requests(requesting_provider_npi);

CREATE INDEX IF NOT EXISTS idx_prior_auth_resp_request_id ON prior_authorization_responses(request_id);
CREATE INDEX IF NOT EXISTS idx_prior_auth_resp_auth_number ON prior_authorization_responses(authorization_number);

CREATE INDEX IF NOT EXISTS idx_service_type_codes_code ON service_type_codes(code);
CREATE INDEX IF NOT EXISTS idx_procedure_codes_code ON procedure_codes(code);
CREATE INDEX IF NOT EXISTS idx_diagnosis_codes_code ON diagnosis_codes(code);

CREATE INDEX IF NOT EXISTS idx_authorization_audit_request_id ON authorization_audit(request_id);
CREATE INDEX IF NOT EXISTS idx_authorization_audit_action ON authorization_audit(action);

-- Create update triggers for updated_at columns
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_patient_information_updated_at BEFORE UPDATE ON patient_information FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_prior_authorization_requests_updated_at BEFORE UPDATE ON prior_authorization_requests FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_prior_authorization_responses_updated_at BEFORE UPDATE ON prior_authorization_responses FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_service_type_codes_updated_at BEFORE UPDATE ON service_type_codes FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_procedure_codes_updated_at BEFORE UPDATE ON procedure_codes FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_diagnosis_codes_updated_at BEFORE UPDATE ON diagnosis_codes FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_authorization_audit_updated_at BEFORE UPDATE ON authorization_audit FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Insert sample service type codes
INSERT INTO service_type_codes (code, description, category, requires_authorization) VALUES
('1', 'Medical Care', 'Medical', TRUE),
('2', 'Surgical', 'Surgical', TRUE),
('3', 'Consultation', 'Medical', FALSE),
('4', 'Diagnostic X-Ray', 'Diagnostic', TRUE),
('5', 'Diagnostic Lab', 'Diagnostic', FALSE),
('6', 'Radiation Therapy', 'Therapeutic', TRUE),
('12', 'Durable Medical Equipment Purchase', 'Equipment', TRUE),
('13', 'Durable Medical Equipment Rental', 'Equipment', TRUE),
('14', 'Prosthetic Device', 'Equipment', TRUE),
('18', 'Durable Medical Equipment', 'Equipment', TRUE);

-- Insert sample procedure codes (CPT codes)
INSERT INTO procedure_codes (code, description, code_type, category, requires_authorization) VALUES
('99213', 'Office visit, established patient, moderate complexity', 'CPT', 'Evaluation & Management', FALSE),
('99214', 'Office visit, established patient, moderate to high complexity', 'CPT', 'Evaluation & Management', FALSE),
('10120', 'Incision and removal of foreign body', 'CPT', 'Surgery', TRUE),
('71020', 'Chest X-ray, 2 views', 'CPT', 'Radiology', FALSE),
('80053', 'Comprehensive metabolic panel', 'CPT', 'Laboratory', FALSE),
('93000', 'Electrocardiogram', 'CPT', 'Cardiovascular', FALSE),
('J7030', 'Infusion, normal saline solution', 'HCPCS', 'Drugs', FALSE);

-- Insert sample diagnosis codes (ICD-10)
INSERT INTO diagnosis_codes (code, description, category) VALUES
('Z00.00', 'Encounter for general adult medical examination without abnormal findings', 'Health Status'),
('I10', 'Essential hypertension', 'Cardiovascular'),
('E11.9', 'Type 2 diabetes mellitus without complications', 'Endocrine'),
('M79.3', 'Panniculitis, unspecified', 'Musculoskeletal'),
('R06.02', 'Shortness of breath', 'Respiratory'),
('K21.9', 'Gastro-esophageal reflux disease without esophagitis', 'Digestive'),
('F32.9', 'Major depressive disorder, single episode, unspecified', 'Mental Health');
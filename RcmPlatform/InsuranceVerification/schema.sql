-- PostgreSQL Database Schema for Health Insurance Verification System
-- File: database/schema.sql

-- Create database
CREATE DATABASE health_insurance_db;

-- Connect to the database
\c health_insurance_db;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Insurance Cards Table
CREATE TABLE insurance_cards (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(255),
    member_id VARCHAR(100) NOT NULL,
    group_number VARCHAR(100),
    plan_name VARCHAR(255),
    insurance_company VARCHAR(255),
    effective_date VARCHAR(20),
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Eligibility Requests Table (EDI 270)
CREATE TABLE eligibility_requests (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) UNIQUE NOT NULL,
    member_id VARCHAR(100) NOT NULL,
    provider_npi VARCHAR(20) NOT NULL,
    service_type VARCHAR(10) DEFAULT '30',
    subscriber_first_name VARCHAR(100),
    subscriber_last_name VARCHAR(100),
    subscriber_dob DATE,
    edi_270_content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Eligibility Responses Table (EDI 271)
CREATE TABLE eligibility_responses (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) NOT NULL,
    edi_271_content TEXT NOT NULL,
    is_eligible BOOLEAN NOT NULL DEFAULT FALSE,
    benefits_info JSONB,
    coverage_status VARCHAR(50),
    effective_date DATE,
    termination_date DATE,
    copay_amount DECIMAL(10,2),
    deductible_amount DECIMAL(10,2),
    out_of_pocket_max DECIMAL(10,2),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES eligibility_requests(request_id)
);

-- Providers Table
CREATE TABLE providers (
    id SERIAL PRIMARY KEY,
    npi VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(10),
    zip_code VARCHAR(20),
    phone VARCHAR(20),
    specialty VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insurance Payers Table
CREATE TABLE insurance_payers (
    id SERIAL PRIMARY KEY,
    payer_id VARCHAR(50) UNIQUE NOT NULL,
    payer_name VARCHAR(255) NOT NULL,
    contact_info JSONB,
    supported_transactions VARCHAR[],
    endpoint_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transaction Log Table
CREATE TABLE transaction_logs (
    id SERIAL PRIMARY KEY,
    transaction_type VARCHAR(10) NOT NULL, -- '270' or '271'
    request_id VARCHAR(50),
    sender_id VARCHAR(50),
    receiver_id VARCHAR(50),
    transaction_content TEXT,
    status VARCHAR(20),
    error_message TEXT,
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Log Table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    record_id INTEGER NOT NULL,
    old_values JSONB,
    new_values JSONB,
    user_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_insurance_cards_member_id ON insurance_cards(member_id);
CREATE INDEX idx_eligibility_requests_request_id ON eligibility_requests(request_id);
CREATE INDEX idx_eligibility_requests_member_id ON eligibility_requests(member_id);
CREATE INDEX idx_eligibility_requests_status ON eligibility_requests(status);
CREATE INDEX idx_eligibility_responses_request_id ON eligibility_responses(request_id);
CREATE INDEX idx_transaction_logs_request_id ON transaction_logs(request_id);
CREATE INDEX idx_transaction_logs_created_at ON transaction_logs(created_at);

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_insurance_cards_updated_at BEFORE UPDATE ON insurance_cards
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_eligibility_requests_updated_at BEFORE UPDATE ON eligibility_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO providers (npi, name, address_line1, city, state, zip_code, phone, specialty) VALUES
('1234567890', 'Dr. John Smith', '123 Medical Plaza', 'Boston', 'MA', '02101', '617-555-0100', 'Internal Medicine'),
('0987654321', 'Springfield Medical Group', '456 Health Ave', 'Springfield', 'MA', '01109', '413-555-0200', 'Family Practice'),
('1122334455', 'Boston General Hospital', '789 Hospital Way', 'Boston', 'MA', '02115', '617-555-0300', 'Hospital');

INSERT INTO insurance_payers (payer_id, payer_name, contact_info, supported_transactions, endpoint_url, is_active) VALUES
('AETNA001', 'Aetna Health Insurance', '{"phone": "800-123-4567", "email": "edi@aetna.com"}', ARRAY['270', '271'], 'https://edi.aetna.com/eligibility', TRUE),
('BCBS001', 'Blue Cross Blue Shield', '{"phone": "800-234-5678", "email": "edi@bcbs.com"}', ARRAY['270', '271'], 'https://edi.bcbs.com/eligibility', TRUE),
('CIGNA001', 'Cigna Healthcare', '{"phone": "800-345-6789", "email": "edi@cigna.com"}', ARRAY['270', '271'], 'https://edi.cigna.com/eligibility', TRUE);

-- Create views for reporting
CREATE VIEW eligibility_summary AS
SELECT 
    er.request_id,
    er.member_id,
    er.provider_npi,
    p.name as provider_name,
    er.status,
    er.created_at as request_date,
    ersp.is_eligible,
    ersp.coverage_status,
    ersp.processed_at
FROM eligibility_requests er
LEFT JOIN eligibility_responses ersp ON er.request_id = ersp.request_id
LEFT JOIN providers p ON er.provider_npi = p.npi
ORDER BY er.created_at DESC;

-- Create a view for daily statistics
CREATE VIEW daily_stats AS
SELECT 
    DATE(created_at) as request_date,
    COUNT(*) as total_requests,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_requests,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_requests,
    COUNT(CASE WHEN status = 'error' THEN 1 END) as error_requests
FROM eligibility_requests
GROUP BY DATE(created_at)
ORDER BY request_date DESC;

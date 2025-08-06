-- Database Initialization Script for EDI Claims Processing
-- This script sets up the complete database schema with sample data
-- Schema is aligned with SQLAlchemy models in models.py

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the main tables first, before inserting any data

-- Create payers table
CREATE TABLE IF NOT EXISTS payers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    payer_id VARCHAR(50) UNIQUE NOT NULL,
    address VARCHAR(500),
    contact_info JSONB,
    companion_guide_url VARCHAR(500),
    validation_rules JSONB,
    transmission_method VARCHAR(20), -- FTP, AS2, API
    is_active BOOLEAN DEFAULT true,
    certification_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create claims table
CREATE TABLE IF NOT EXISTS claims (
    id SERIAL PRIMARY KEY,
    claim_number VARCHAR(50) UNIQUE NOT NULL,
    claim_type VARCHAR(10) NOT NULL, -- 837D, 837P, 837I
    status VARCHAR(20) NOT NULL, -- queued, validating, validated, sent, rejected, paid, etc.
    patient_first_name VARCHAR(100),
    patient_last_name VARCHAR(100),
    patient_dob TIMESTAMP,
    patient_id VARCHAR(50),
    provider_name VARCHAR(200),
    provider_npi VARCHAR(10),
    provider_taxonomy VARCHAR(10),
    payer_id INTEGER REFERENCES payers(id),
    total_charge DECIMAL(10,2),
    allowed_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    patient_responsibility DECIMAL(10,2),
    raw_edi_data TEXT,
    parsed_data JSONB,
    validation_errors JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    processed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create service_lines table
CREATE TABLE IF NOT EXISTS service_lines (
    id SERIAL PRIMARY KEY,
    claim_id INTEGER REFERENCES claims(id) ON DELETE CASCADE,
    line_number INTEGER NOT NULL,
    procedure_code VARCHAR(10) NOT NULL,
    procedure_description VARCHAR(500),
    service_date_from TIMESTAMP,
    service_date_to TIMESTAMP,
    units INTEGER DEFAULT 1,
    charge_amount DECIMAL(10,2) NOT NULL,
    allowed_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    diagnosis_code_1 VARCHAR(10),
    diagnosis_code_2 VARCHAR(10),
    diagnosis_code_3 VARCHAR(10),
    diagnosis_code_4 VARCHAR(10),
    modifier_1 VARCHAR(2),
    modifier_2 VARCHAR(2),
    modifier_3 VARCHAR(2),
    modifier_4 VARCHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(claim_id, line_number)
);

-- Create dental_details table for dental-specific information
CREATE TABLE IF NOT EXISTS dental_details (
    id SERIAL PRIMARY KEY,
    claim_id INTEGER REFERENCES claims(id) ON DELETE CASCADE,
    tooth_number VARCHAR(3), -- Universal numbering system
    tooth_surface VARCHAR(10), -- M, O, D, L, B, I combinations
    oral_cavity_area VARCHAR(2),
    treatment_plan_sequence INTEGER,
    months_of_treatment INTEGER, -- For orthodontics
    prosthetic_replacement BOOLEAN DEFAULT false,
    initial_placement_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample payers
INSERT INTO payers (name, payer_id, address, contact_info, companion_guide_url, validation_rules, transmission_method, is_active, certification_status) VALUES
('Delta Dental of California', 'DELTA001', '100 First Street, San Francisco, CA 94105', 
 '{"phone": "800-765-6003", "contact_email": "provider@delta.org"}',
 'https://www.deltadentalca.org/providers/claim-submission-guidelines',
 '{"max_procedures_per_claim": 20, "require_predetermination": ["D2740", "D2750"], "frequency_limits": {"D1110": "6_months", "D0274": "12_months"}}',
 'SFTP', true, 'certified'),

('Blue Cross Blue Shield', 'BCBS001', '225 N Michigan Ave, Chicago, IL 60601',
 '{"phone": "800-810-2583", "contact_email": "provider@bcbs.com"}',
 'https://www.bcbs.com/providers/edi-companion-guide',
 '{"require_diagnosis_code": true, "max_service_lines": 50, "prior_auth_required": ["99213", "99214"]}',
 'AS2', true, 'certified'),

('Medicare', 'CMS001', '7500 Security Blvd, Baltimore, MD 21244',
 '{"phone": "800-633-4227", "contact_email": "provider@cms.gov"}',
 'https://www.cms.gov/medicare/billing/electronicbillingedc',
 '{"require_npi": true, "max_claim_amount": 10000, "require_taxonomy": true}',
 'FTP', true, 'certified'),

('Cigna Dental', 'CIGNA001', '900 Cottage Grove Rd, Bloomfield, CT 06002',
 '{"phone": "800-244-6224", "contact_email": "provider@cigna.com"}',
 'https://www.cigna.com/providers/dental-claims',
 '{"network_validation": true, "require_tooth_number": ["D2140", "D2150"], "predetermination_threshold": 500}',
 'SFTP', true, 'pending'),

('MetLife Dental', 'METLIFE001', '200 Park Ave, New York, NY 10166',
 '{"phone": "800-275-4638", "contact_email": "provider@metlife.com"}',
 'https://www.metlife.com/providers/dental-claims-guide',
 '{"documentation_required": ["D4210", "D4211"], "frequency_tracking": true, "max_age_restrictions": {"D1206": 18}}',
 'API', true, 'certified');

-- Insert sample claims with different types and statuses
INSERT INTO claims (
    claim_number, claim_type, status, patient_first_name, patient_last_name, 
    patient_dob, patient_id, provider_name, provider_npi, provider_taxonomy,
    payer_id, total_charge, allowed_amount, paid_amount, patient_responsibility,
    raw_edi_data, parsed_data, validation_errors, created_at, submitted_at, processed_at
) VALUES 
-- Dental claim (validated)
('CLM20240115001', '837D', 'validated', 'John', 'Doe', '1985-03-15 00:00:00', 'PAT001',
 'Smile Dental Care', '1234567890', '122300000X', 1, 450.00, NULL, NULL, NULL,
 'ISA*00*          *00*          *ZZ*SUBMITTER      *ZZ*RECEIVER       *240115*1030*^*00501*000000001*0*P*:~GS*HC*SENDER*RECEIVER*20240115*1030*1*X*005010X222A1~ST*837*0001~BHT*0019*00*000000001*20240115*1030*CH~',
 '{"claim_type": "837D", "total_charge": 450.00, "service_lines": [{"procedure": "D1110", "charge": 150.00}, {"procedure": "D2140", "charge": 300.00, "tooth": "14"}]}',
 NULL, '2024-01-15 10:30:00', NULL, NULL),

-- Professional claim (sent)
('CLM20240114001', '837P', 'sent', 'Jane', 'Smith', '1992-07-22 00:00:00', 'PAT002',
 'Family Health Center', '0987654321', '207Q00000X', 2, 250.00, NULL, NULL, NULL,
 'ISA*00*          *00*          *ZZ*SUBMITTER      *ZZ*RECEIVER       *240114*1420*^*00501*000000002*0*P*:~GS*HC*SENDER*RECEIVER*20240114*1420*2*X*005010X222A1~ST*837*0002~BHT*0019*00*000000002*20240114*1420*CH~',
 '{"claim_type": "837P", "total_charge": 250.00, "service_lines": [{"procedure": "99213", "charge": 150.00, "diagnosis": "Z00.00"}, {"procedure": "85025", "charge": 100.00}]}',
 NULL, '2024-01-14 14:20:00', '2024-01-14 16:30:00', NULL),

-- Institutional claim (rejected)
('CLM20240113001', '837I', 'rejected', 'Robert', 'Johnson', '1955-11-08 00:00:00', 'PAT003',
 'City Hospital', '1122334455', '282N00000X', 3, 1250.00, NULL, NULL, NULL,
 'ISA*00*          *00*          *ZZ*SUBMITTER      *ZZ*RECEIVER       *240113*0915*^*00501*000000003*0*P*:~GS*HC*SENDER*RECEIVER*20240113*0915*3*X*005010X223A2~ST*837*0003~BHT*0019*00*000000003*20240113*0915*CH~',
 '{"claim_type": "837I", "total_charge": 1250.00, "service_lines": [{"procedure": "99221", "charge": 800.00}, {"procedure": "71020", "charge": 450.00}]}',
 '{"errors": ["Invalid NPI format", "Missing required diagnosis code", "Service date in future"]}',
 '2024-01-13 09:15:00', NULL, NULL),

-- Dental claim (paid)
('CLM20240112001', '837D', 'paid', 'Mary', 'Wilson', '1978-05-30 00:00:00', 'PAT004',
 'Downtown Dental', '2345678901', '122300000X', 1, 180.00, 150.00, 120.00, 30.00,
 'ISA*00*          *00*          *ZZ*SUBMITTER      *ZZ*RECEIVER       *240112*1100*^*00501*000000004*0*P*:~GS*HC*SENDER*RECEIVER*20240112*1100*4*X*005010X222A1~ST*837*0004~BHT*0019*00*000000004*20240112*1100*CH~',
 '{"claim_type": "837D", "total_charge": 180.00, "service_lines": [{"procedure": "D1110", "charge": 180.00}]}',
 NULL, '2024-01-12 11:00:00', '2024-01-12 15:20:00', '2024-01-20 10:45:00'),

-- Professional claim (paid)
('CLM20240111001', '837P', 'paid', 'David', 'Brown', '1968-12-03 00:00:00', 'PAT005',
 'Metro Medical Group', '3456789012', '207Q00000X', 2, 320.00, 280.00, 224.00, 56.00,
 'ISA*00*          *00*          *ZZ*SUBMITTER      *ZZ*RECEIVER       *240111*0830*^*00501*000000005*0*P*:~GS*HC*SENDER*RECEIVER*20240111*0830*5*X*005010X222A1~ST*837*0005~BHT*0019*00*000000005*20240111*0830*CH~',
 '{"claim_type": "837P", "total_charge": 320.00, "service_lines": [{"procedure": "99214", "charge": 200.00, "diagnosis": "E11.9"}, {"procedure": "80053", "charge": 120.00}]}',
 NULL, '2024-01-11 08:30:00', '2024-01-11 12:15:00', '2024-01-18 14:22:00');

-- Insert service lines for the claims
INSERT INTO service_lines (
    claim_id, line_number, procedure_code, procedure_description, 
    service_date_from, units, charge_amount, allowed_amount, paid_amount, diagnosis_code_1, modifier_1
) VALUES
-- Service lines for claim 1 (Dental)
(1, 1, 'D1110', 'Adult prophylaxis', '2024-01-15 10:30:00', 1, 150.00, NULL, NULL, NULL, NULL),
(1, 2, 'D2140', 'Amalgam restoration - one surface', '2024-01-15 10:30:00', 1, 300.00, NULL, NULL, NULL, NULL),

-- Service lines for claim 2 (Professional)
(2, 1, '99213', 'Office/outpatient visit, established patient', '2024-01-14 14:20:00', 1, 150.00, NULL, NULL, 'Z00.00', NULL),
(2, 2, '85025', 'Blood count; complete', '2024-01-14 14:20:00', 1, 100.00, NULL, NULL, 'Z00.00', NULL),

-- Service lines for claim 3 (Institutional)
(3, 1, '99221', 'Initial hospital care', '2024-01-13 09:15:00', 1, 800.00, NULL, NULL, 'I50.9', NULL),
(3, 2, '71020', 'Chest X-ray', '2024-01-13 09:15:00', 1, 450.00, NULL, NULL, 'I50.9', NULL),

-- Service lines for claim 4 (Dental - paid)
(4, 1, 'D1110', 'Adult prophylaxis', '2024-01-12 11:00:00', 1, 180.00, 150.00, 120.00, NULL, NULL),

-- Service lines for claim 5 (Professional - paid)
(5, 1, '99214', 'Office/outpatient visit, established patient', '2024-01-11 08:30:00', 1, 200.00, 180.00, 144.00, 'E11.9', NULL),
(5, 2, '80053', 'Comprehensive metabolic panel', '2024-01-11 08:30:00', 1, 120.00, 100.00, 80.00, 'E11.9', NULL);

-- Insert dental details for dental claims
INSERT INTO dental_details (
    claim_id, tooth_number, tooth_surface, oral_cavity_area, 
    treatment_plan_sequence, prosthetic_replacement
) VALUES
(1, '14', 'O', NULL, 1, false),  -- Upper right first molar, occlusal surface
(4, NULL, NULL, '01', 1, false); -- Full mouth (prophylaxis doesn't need specific tooth)

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status);
CREATE INDEX IF NOT EXISTS idx_claims_type ON claims(claim_type);
CREATE INDEX IF NOT EXISTS idx_claims_created_at ON claims(created_at);
CREATE INDEX IF NOT EXISTS idx_claims_claim_number ON claims(claim_number);
CREATE INDEX IF NOT EXISTS idx_claims_payer_id ON claims(payer_id);
CREATE INDEX IF NOT EXISTS idx_service_lines_claim_id ON service_lines(claim_id);
CREATE INDEX IF NOT EXISTS idx_service_lines_procedure_code ON service_lines(procedure_code);

-- Sample CDT codes reference table (subset)
CREATE TABLE IF NOT EXISTS cdt_codes (
    code VARCHAR(10) PRIMARY KEY,
    description TEXT NOT NULL,
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    effective_date DATE,
    fee_schedule_amount DECIMAL(10,2)
);

INSERT INTO cdt_codes (code, description, category, is_active, effective_date, fee_schedule_amount) VALUES
('D0120', 'Periodic oral evaluation', 'Diagnostic', true, '2024-01-01', 75.00),
('D0140', 'Limited oral evaluation', 'Diagnostic', true, '2024-01-01', 65.00),
('D0274', 'Bitewing radiographs - four films', 'Diagnostic', true, '2024-01-01', 85.00),
('D1110', 'Adult prophylaxis', 'Preventive', true, '2024-01-01', 120.00),
('D1120', 'Child prophylaxis', 'Preventive', true, '2024-01-01', 95.00),
('D1206', 'Fluoride varnish application', 'Preventive', true, '2024-01-01', 45.00),
('D2140', 'Amalgam restoration - one surface', 'Restorative', true, '2024-01-01', 185.00),
('D2150', 'Amalgam restoration - two surfaces', 'Restorative', true, '2024-01-01', 220.00),
('D2330', 'Resin-based composite - one surface', 'Restorative', true, '2024-01-01', 210.00),
('D2740', 'Crown - porcelain/ceramic substrate', 'Restorative', true, '2024-01-01', 1250.00),
('D3220', 'Therapeutic pulpotomy', 'Endodontics', true, '2024-01-01', 425.00),
('D4210', 'Gingivectomy or gingivoplasty - four or more teeth', 'Periodontics', true, '2024-01-01', 650.00),
('D7140', 'Extraction, erupted tooth or exposed root', 'Oral Surgery', true, '2024-01-01', 285.00),
('D8210', 'Removable appliance therapy', 'Orthodontics', true, '2024-01-01', 1850.00);

-- Sample CPT codes reference table (subset)
CREATE TABLE IF NOT EXISTS cpt_codes (
    code VARCHAR(10) PRIMARY KEY,
    description TEXT NOT NULL,
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    relative_value_units DECIMAL(6,2),
    fee_schedule_amount DECIMAL(10,2)
);

INSERT INTO cpt_codes (code, description, category, is_active, relative_value_units, fee_schedule_amount) VALUES
('99201', 'Office/outpatient visit, new patient, straightforward', 'E&M', true, 0.93, 76.00),
('99202', 'Office/outpatient visit, new patient, low complexity', 'E&M', true, 1.60, 128.00),
('99213', 'Office/outpatient visit, established patient, low complexity', 'E&M', true, 1.30, 109.00),
('99214', 'Office/outpatient visit, established patient, moderate complexity', 'E&M', true, 1.92, 167.00),
('99221', 'Initial hospital care, per day, straightforward', 'E&M', true, 1.94, 170.00),
('36415', 'Collection of venous blood by venipuncture', 'Laboratory', true, 0.17, 8.00),
('80053', 'Comprehensive metabolic panel', 'Laboratory', true, 0.27, 35.00),
('85025', 'Blood count; complete (CBC), automated', 'Laboratory', true, 0.28, 18.00),
('71020', 'Radiologic examination, chest, 2 views', 'Radiology', true, 0.22, 42.00),
('73030', 'Radiologic examination, shoulder; complete', 'Radiology', true, 0.26, 67.00);

-- Create procedure frequency rules table
CREATE TABLE IF NOT EXISTS procedure_frequency_rules (
    id SERIAL PRIMARY KEY,
    procedure_code VARCHAR(10) NOT NULL,
    claim_type VARCHAR(10) NOT NULL,
    frequency_limit VARCHAR(50) NOT NULL,
    time_period_days INTEGER NOT NULL,
    age_restriction_min INTEGER,
    age_restriction_max INTEGER,
    description TEXT,
    is_active BOOLEAN DEFAULT true
);

INSERT INTO procedure_frequency_rules (
    procedure_code, claim_type, frequency_limit, time_period_days, 
    age_restriction_min, age_restriction_max, description, is_active
) VALUES
('D1110', '837D', '2 per year', 183, NULL, NULL, 'Adult prophylaxis - twice per year', true),
('D1120', '837D', '2 per year', 183, NULL, 18, 'Child prophylaxis - twice per year for minors', true),
('D0274', '837D', '1 per year', 365, NULL, NULL, 'Bitewing X-rays - once per year', true),
('D0210', '837D', '1 per 3 years', 1095, NULL, NULL, 'Full mouth X-rays - every 3 years', true),
('D1206', '837D', '2 per year', 183, NULL, 18, 'Fluoride treatment - twice per year for children', true),
('99213', '837P', 'No limit', 0, NULL, NULL, 'Office visits have no frequency restriction', true),
('99214', '837P', 'No limit', 0, NULL, NULL, 'Office visits have no frequency restriction', true);

-- Create audit log table for tracking changes
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

-- Create trigger function for audit logging
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, new_values)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values, new_values)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', row_to_json(OLD)::jsonb);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create audit triggers for key tables
CREATE TRIGGER claims_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON claims
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER payers_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON payers
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Create views for reporting
CREATE OR REPLACE VIEW claim_summary_view AS
SELECT 
    c.id,
    c.claim_number,
    c.claim_type,
    c.status,
    c.patient_first_name || ' ' || c.patient_last_name AS patient_name,
    c.provider_name,
    c.provider_npi,
    p.name AS payer_name,
    c.total_charge,
    c.allowed_amount,
    c.paid_amount,
    c.patient_responsibility,
    c.created_at,
    c.submitted_at,
    c.processed_at,
    COUNT(sl.id) AS service_line_count,
    CASE 
        WHEN c.validation_errors IS NOT NULL THEN 
            jsonb_array_length(c.validation_errors->'errors')
        ELSE 0 
    END AS error_count
FROM claims c
LEFT JOIN payers p ON c.payer_id = p.id
LEFT JOIN service_lines sl ON c.id = sl.claim_id
GROUP BY c.id, p.name;

-- Create materialized view for dashboard statistics (refresh periodically)
CREATE MATERIALIZED VIEW IF NOT EXISTS dashboard_stats AS
SELECT 
    COUNT(*) FILTER (WHERE created_at >= CURRENT_DATE - INTERVAL '30 days') AS claims_last_30_days,
    COUNT(*) FILTER (WHERE status = 'validated') AS validated_claims,
    COUNT(*) FILTER (WHERE status = 'sent') AS sent_claims,
    COUNT(*) FILTER (WHERE status = 'paid') AS paid_claims,
    COUNT(*) FILTER (WHERE status = 'rejected') AS rejected_claims,
    COUNT(*) FILTER (WHERE claim_type = '837D') AS dental_claims,
    COUNT(*) FILTER (WHERE claim_type = '837P') AS professional_claims,
    COUNT(*) FILTER (WHERE claim_type = '837I') AS institutional_claims,
    COALESCE(SUM(total_charge), 0) AS total_charged,
    COALESCE(SUM(allowed_amount), 0) AS total_allowed,
    COALESCE(SUM(paid_amount), 0) AS total_paid,
    COALESCE(AVG(total_charge), 0) AS avg_claim_amount,
    COALESCE(
        SUM(paid_amount) / NULLIF(SUM(total_charge), 0) * 100, 
        0
    ) AS collection_rate_percent
FROM claims;

-- Create unique index on materialized view
CREATE UNIQUE INDEX IF NOT EXISTS dashboard_stats_single_row ON dashboard_stats ((1));

-- Initial refresh of materialized view
REFRESH MATERIALIZED VIEW dashboard_stats;

-- Create function to refresh dashboard stats (call this periodically)
CREATE OR REPLACE FUNCTION refresh_dashboard_stats()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard_stats;
END;
$$ LANGUAGE plpgsql;

-- Sample validation errors for testing
UPDATE claims 
SET validation_errors = '{"errors": ["Invalid NPI check digit", "Missing required diagnosis code", "Service date cannot be in the future"], "warnings": ["Unusual procedure combination"]}'
WHERE claim_number = 'CLM20240113001';

-- Add some additional test data for better demo
INSERT INTO claims (
    claim_number, claim_type, status, patient_first_name, patient_last_name,
    patient_dob, patient_id, provider_name, provider_npi, provider_taxonomy,
    payer_id, total_charge, created_at
) VALUES
('CLM20240122001', '837D', 'queued', 'Emily', 'Davis', '1990-09-12 00:00:00', 'PAT006',
 'Bright Smiles Dental', '4567890123', '122300000X', 4, 375.00, '2024-01-22 14:30:00'),
 
('CLM20240122002', '837P', 'validating', 'Michael', 'Garcia', '1975-04-18 00:00:00', 'PAT007',
 'Westside Clinic', '5678901234', '207Q00000X', 2, 450.00, '2024-01-22 15:45:00'),
 
('CLM20240122003', '837I', 'validated', 'Sarah', 'Martinez', '1982-11-25 00:00:00', 'PAT008',
 'Regional Medical Center', '6789012345', '282N00000X', 3, 2100.00, '2024-01-22 16:20:00');

COMMIT;

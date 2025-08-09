-- Scheduling2.0 - Unified Database Schema
-- Merged schema combining Medical and Mental Health scheduling features
-- PostgreSQL compatible SQL schema

-- Database is already created by Docker container
-- Create extension for UUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing objects if they exist (for clean recreation)
DROP TABLE IF EXISTS waitlist_entries CASCADE;
DROP TABLE IF EXISTS appointments CASCADE;
DROP TABLE IF EXISTS practitioner_availability CASCADE;
DROP TABLE IF EXISTS practitioner_specialties CASCADE;
DROP TABLE IF EXISTS patients CASCADE;
DROP TABLE IF EXISTS clients CASCADE;
DROP TABLE IF EXISTS practitioners CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS organizations CASCADE;
DROP TABLE IF EXISTS service_codes CASCADE;
DROP TABLE IF EXISTS appointment_types CASCADE;
DROP TABLE IF EXISTS specialties CASCADE;
DROP TABLE IF EXISTS locations CASCADE;

-- Drop existing types if they exist
DROP TYPE IF EXISTS waitlist_status CASCADE;
DROP TYPE IF EXISTS waitlist_priority CASCADE;
DROP TYPE IF EXISTS billing_type CASCADE;
DROP TYPE IF EXISTS session_type CASCADE;
DROP TYPE IF EXISTS appointment_type CASCADE;
DROP TYPE IF EXISTS appointment_status CASCADE;
DROP TYPE IF EXISTS service_type CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;

-- Create enums
CREATE TYPE service_type AS ENUM ('THERAPY', 'CONSULTATION', 'ASSESSMENT', 'MEDICAL', 'MENTAL_HEALTH', 'FOLLOW_UP', 'EMERGENCY');
CREATE TYPE appointment_status AS ENUM ('SCHEDULED', 'CONFIRMED', 'PENDING', 'CANCELLED', 'NO_SHOW', 'COMPLETED');
CREATE TYPE appointment_type AS ENUM ('APPOINTMENT', 'CONSULTATION', 'FOLLOW_UP', 'INITIAL', 'EMERGENCY');
CREATE TYPE session_type AS ENUM ('INDIVIDUAL', 'COUPLE', 'FAMILY', 'GROUP', 'TELEHEALTH', 'IN_PERSON');
CREATE TYPE billing_type AS ENUM ('SELF_PAY', 'INSURANCE', 'SLIDING_SCALE', 'MEDICARE', 'MEDICAID');
CREATE TYPE waitlist_priority AS ENUM ('LOW', 'NORMAL', 'HIGH', 'URGENT');
CREATE TYPE waitlist_status AS ENUM ('ACTIVE', 'CONTACTED', 'SCHEDULED', 'REMOVED');
CREATE TYPE user_role AS ENUM ('admin', 'practitioner', 'nurse', 'receptionist', 'therapist', 'psychiatrist');

-- ============================================================================
-- Organizations (from Scheduling project)
-- ============================================================================
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(500) NOT NULL,
    alias TEXT[], -- Alternative names
    description TEXT,
    identifiers JSONB, -- NPI, Tax ID
    type JSONB, -- CodeableConcept
    telecom JSONB, -- Contact information
    addresses JSONB, -- Addresses
    part_of UUID, -- Parent organization
    contact JSONB, -- Contact persons
    endpoints JSONB, -- Technical connections
    active BOOLEAN DEFAULT TRUE,
    fhir_resource JSONB, -- FHIR Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Users (practitioners, staff, admins)
-- ============================================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role user_role NOT NULL,
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Locations (from MBH-Scheduling)
-- ============================================================================
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    is_telehealth BOOLEAN DEFAULT FALSE,
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Service Codes (from MBH-Scheduling)
-- ============================================================================
CREATE TABLE service_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    default_fee INTEGER NOT NULL, -- Amount in cents
    duration_minutes INTEGER NOT NULL,
    service_type service_type NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Specialties (from Scheduling project)
-- ============================================================================
CREATE TABLE specialties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Appointment Types (from Scheduling project)
-- ============================================================================
CREATE TABLE appointment_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30,
    color VARCHAR(7) DEFAULT '#3498db',
    description TEXT,
    service_type service_type,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Practitioners (merged from both projects)
-- ============================================================================
CREATE TABLE practitioners (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    fhir_id VARCHAR(255) UNIQUE,
    
    -- Basic Identity
    family_name VARCHAR(255) NOT NULL,
    given_names TEXT[], -- Array of given names
    prefix VARCHAR(50),
    suffix VARCHAR(50),
    
    -- Credentials and Role
    qualifications JSONB,
    specialties JSONB,
    roles JSONB,
    
    -- Identifiers
    identifiers JSONB,
    
    -- Contact Info
    telecom JSONB,
    addresses JSONB,
    
    -- Associated Organization
    organization_id UUID REFERENCES organizations(id),
    
    -- Availability
    availability JSONB,
    
    -- FHIR resource
    fhir_resource JSONB,
    
    -- Audit Fields
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Practitioner Specialties (junction table)
-- ============================================================================
CREATE TABLE practitioner_specialties (
    practitioner_id INTEGER REFERENCES practitioners(id) ON DELETE CASCADE,
    specialty_id INTEGER REFERENCES specialties(id) ON DELETE CASCADE,
    PRIMARY KEY (practitioner_id, specialty_id)
);

-- ============================================================================
-- Patients (from Scheduling project)
-- ============================================================================
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20) NOT NULL,
    date_of_birth DATE,
    address TEXT,
    insurance_info TEXT,
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    medical_notes TEXT,
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Clients (from MBH-Scheduling - for mental health specific data)
-- ============================================================================
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    date_of_birth DATE,
    emergency_contact TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Practitioner Availability (from Scheduling project)
-- ============================================================================
CREATE TABLE practitioner_availability (
    id SERIAL PRIMARY KEY,
    practitioner_id INTEGER REFERENCES practitioners(id) ON DELETE CASCADE,
    availability_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Appointments (merged from both projects)
-- ============================================================================
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    
    -- Patient/Client references (support both)
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    
    -- Practitioner and appointment details
    practitioner_id INTEGER REFERENCES practitioners(id) ON DELETE CASCADE,
    appointment_type_id INTEGER REFERENCES appointment_types(id),
    service_code_id INTEGER REFERENCES service_codes(id),
    location_id INTEGER REFERENCES locations(id),
    
    -- Appointment details
    appointment_type appointment_type NOT NULL,
    session_type session_type NOT NULL,
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL,
    service_type service_type NOT NULL,
    status appointment_status NOT NULL DEFAULT 'SCHEDULED',
    billing_type billing_type NOT NULL,
    fee_amount INTEGER, -- Amount in cents
    notes TEXT,
    reason_for_visit TEXT,
    is_telehealth BOOLEAN DEFAULT FALSE,
    
    -- Audit fields
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT check_patient_or_client CHECK (
        (patient_id IS NOT NULL AND client_id IS NULL) OR 
        (patient_id IS NULL AND client_id IS NOT NULL)
    )
);

-- ============================================================================
-- Waitlist Entries (from MBH-Scheduling)
-- ============================================================================
CREATE TABLE waitlist_entries (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    practitioner_id INTEGER REFERENCES practitioners(id),
    
    -- Preferences
    preferred_dates JSONB, -- JSON array of preferred dates
    preferred_times JSONB, -- JSON array of preferred times
    service_type service_type NOT NULL,
    
    -- Priority and status
    priority waitlist_priority DEFAULT 'NORMAL',
    status waitlist_status DEFAULT 'ACTIVE',
    notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT check_waitlist_patient_or_client CHECK (
        (patient_id IS NOT NULL AND client_id IS NULL) OR 
        (patient_id IS NULL AND client_id IS NOT NULL)
    )
);

-- ============================================================================
-- Indexes for Performance
-- ============================================================================
CREATE INDEX idx_appointments_practitioner_date ON appointments(practitioner_id, appointment_date);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_client ON appointments(client_id);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_patients_phone ON patients(phone);
CREATE INDEX idx_patients_email ON patients(email);
CREATE INDEX idx_clients_email ON clients(email);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_practitioner_availability_practitioner_day ON practitioner_availability(practitioner_id, availability_date);
CREATE INDEX idx_waitlist_client_id ON waitlist_entries(client_id);
CREATE INDEX idx_waitlist_patient_id ON waitlist_entries(patient_id);
CREATE INDEX idx_waitlist_practitioner_id ON waitlist_entries(practitioner_id);
CREATE INDEX idx_waitlist_status ON waitlist_entries(status);
CREATE INDEX idx_providers_email ON practitioners(family_name);
CREATE INDEX idx_organizations_fhir_id ON organizations(fhir_id);

-- ============================================================================
-- Triggers for updated_at timestamps
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_locations_updated_at BEFORE UPDATE ON locations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_service_codes_updated_at BEFORE UPDATE ON service_codes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_practitioners_updated_at BEFORE UPDATE ON practitioners FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_waitlist_entries_updated_at BEFORE UPDATE ON waitlist_entries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Sample Data Insertion
-- ============================================================================

-- Insert sample organizations
INSERT INTO organizations (fhir_id, name, description, active) VALUES
('org-001', 'Mental Health Clinic', 'Specialized mental health services', true),
('org-002', 'General Medical Practice', 'Comprehensive medical care', true);

-- Insert sample users
INSERT INTO users (email, password_hash, first_name, last_name, role, phone) VALUES
('admin@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.Gi', 'Admin', 'User', 'admin', '555-0100'),
('dr.smith@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.Gi', 'John', 'Smith', 'practitioner', '555-0101'),
('therapist.jones@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.Gi', 'Sarah', 'Jones', 'therapist', '555-0102');

-- Insert sample specialties
INSERT INTO specialties (name, description) VALUES
('Psychiatry', 'Mental health diagnosis and treatment'),
('Psychology', 'Therapy and counseling services'),
('General Medicine', 'Primary care and general health'),
('Pediatrics', 'Child and adolescent care');

-- Insert sample appointment types
INSERT INTO appointment_types (name, duration_minutes, color, description, service_type) VALUES
('Initial Consultation', 60, '#3498db', 'First appointment with new patient', 'CONSULTATION'),
('Therapy Session', 50, '#e74c3c', 'Regular therapy session', 'THERAPY'),
('Follow-up', 30, '#2ecc71', 'Follow-up appointment', 'FOLLOW_UP'),
('Emergency', 45, '#f39c12', 'Emergency appointment', 'EMERGENCY');

-- Insert sample service codes
INSERT INTO service_codes (code, name, description, default_fee, duration_minutes, service_type) VALUES
('TH001', 'Individual Therapy', 'One-on-one therapy session', 15000, 50, 'THERAPY'),
('CON001', 'Initial Consultation', 'First consultation appointment', 20000, 60, 'CONSULTATION'),
('FU001', 'Follow-up', 'Follow-up appointment', 10000, 30, 'FOLLOW_UP'),
('EM001', 'Emergency Visit', 'Emergency medical visit', 25000, 45, 'EMERGENCY');

-- Insert sample locations
INSERT INTO locations (name, address, is_telehealth, organization_id) VALUES
('Main Clinic', '123 Main St, City, State', false, (SELECT id FROM organizations WHERE fhir_id = 'org-001')),
('Telehealth Office', 'Virtual', true, (SELECT id FROM organizations WHERE fhir_id = 'org-001')),
('Medical Center', '456 Health Ave, City, State', false, (SELECT id FROM organizations WHERE fhir_id = 'org-002'));

-- Insert sample practitioners
INSERT INTO practitioners (user_id, fhir_id, family_name, given_names, organization_id, active) VALUES
((SELECT id FROM users WHERE email = 'dr.smith@clinic.com'), 'pract-001', 'Smith', ARRAY['John'], (SELECT id FROM organizations WHERE fhir_id = 'org-001'), true),
((SELECT id FROM users WHERE email = 'therapist.jones@clinic.com'), 'pract-002', 'Jones', ARRAY['Sarah'], (SELECT id FROM organizations WHERE fhir_id = 'org-001'), true);

-- Link practitioners to specialties
INSERT INTO practitioner_specialties (practitioner_id, specialty_id) VALUES
((SELECT id FROM practitioners WHERE fhir_id = 'pract-001'), (SELECT id FROM specialties WHERE name = 'Psychiatry')),
((SELECT id FROM practitioners WHERE fhir_id = 'pract-002'), (SELECT id FROM specialties WHERE name = 'Psychology')); 
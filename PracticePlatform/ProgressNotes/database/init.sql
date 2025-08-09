-- Mental Health EHR Progress Notes Database Schema
-- PostgreSQL Database Setup

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table for authentication and roles
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('clinician', 'supervisor', 'admin', 'billing_staff')),
    license_number VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    medical_record_number VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Note templates table
CREATE TABLE note_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    template_type VARCHAR(50) NOT NULL CHECK (template_type IN ('SOAP', 'DAP', 'BIRP', 'PAIP', 'Custom')),
    structure JSONB NOT NULL, -- JSON structure for form fields
    is_system_template BOOLEAN DEFAULT false,
    created_by UUID REFERENCES users(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Progress notes table
CREATE TABLE progress_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    clinician_id UUID NOT NULL REFERENCES users(id),
    template_id UUID REFERENCES note_templates(id),
    note_type VARCHAR(50) NOT NULL CHECK (note_type IN ('SOAP', 'DAP', 'BIRP', 'PAIP', 'Custom')),
    session_date TIMESTAMP WITH TIME ZONE NOT NULL,
    content JSONB NOT NULL, -- JSON structure containing note sections
    is_draft BOOLEAN DEFAULT true,
    is_signed BOOLEAN DEFAULT false,
    signed_at TIMESTAMP WITH TIME ZONE,
    signed_by UUID REFERENCES users(id),
    digital_signature TEXT,
    is_locked BOOLEAN DEFAULT false,
    locked_by UUID REFERENCES users(id),
    locked_at TIMESTAMP WITH TIME ZONE,
    unlock_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1
);

-- Note attachments table
CREATE TABLE note_attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    note_id UUID NOT NULL REFERENCES progress_notes(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    uploaded_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit log table for compliance
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    action VARCHAR(100) NOT NULL, -- 'create', 'read', 'update', 'delete', 'sign', 'unlock'
    resource_type VARCHAR(50) NOT NULL, -- 'progress_note', 'template', 'user'
    resource_id UUID NOT NULL,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Patient-clinician relationships
CREATE TABLE patient_clinicians (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    clinician_id UUID NOT NULL REFERENCES users(id),
    is_primary BOOLEAN DEFAULT false,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(patient_id, clinician_id)
);

-- Indexes for performance
CREATE INDEX idx_progress_notes_patient_id ON progress_notes(patient_id);
CREATE INDEX idx_progress_notes_clinician_id ON progress_notes(clinician_id);
CREATE INDEX idx_progress_notes_session_date ON progress_notes(session_date);
CREATE INDEX idx_progress_notes_created_at ON progress_notes(created_at);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_resource_type_id ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_note_templates_updated_at BEFORE UPDATE ON note_templates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_progress_notes_updated_at BEFORE UPDATE ON progress_notes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default note templates
INSERT INTO note_templates (name, template_type, structure, is_system_template) VALUES 
('Standard SOAP Note', 'SOAP', '{"subjective": "", "objective": "", "assessment": "", "plan": ""}', true),
('Standard DAP Note', 'DAP', '{"data": "", "assessment": "", "plan": ""}', true),
('Standard BIRP Note', 'BIRP', '{"behavior": "", "intervention": "", "response": "", "plan": ""}', true),
('Standard PAIP Note', 'PAIP', '{"problem": "", "assessment": "", "intervention": "", "plan": ""}', true);

-- Sample admin user (password: admin123 - hash this properly in production)
INSERT INTO users (email, password_hash, first_name, last_name, role) VALUES 
('admin@clinic.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewsHO3zJBpj2O5ku', 'Admin', 'User', 'admin');

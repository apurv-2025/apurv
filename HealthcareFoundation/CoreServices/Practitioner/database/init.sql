-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- FHIR Practitioner Resource
-- ============================================================================
CREATE TABLE practitioners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,

    -- Demographics
    family_name VARCHAR(255),
    given_names TEXT[],
    prefix VARCHAR(50),
    suffix VARCHAR(50),

    -- Identifiers (NPI, License numbers)
    identifiers JSONB,

    -- Contact Information
    telecom JSONB,
    addresses JSONB,

    -- Basic Info
    gender VARCHAR(20) CHECK (gender IN ('male', 'female', 'other', 'unknown')),
    birth_date DATE,

    -- Professional Info
    qualifications JSONB, -- Education, certifications
    communication JSONB, -- Languages

    -- Photo
    photo JSONB,

    -- Active status
    active BOOLEAN DEFAULT TRUE,

    -- FHIR Metadata
    fhir_resource JSONB,

    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_practitioners_fhir_id ON practitioners(fhir_id);
CREATE INDEX idx_practitioners_family_name ON practitioners(family_name);
CREATE INDEX idx_practitioners_given_names ON practitioners USING GIN(given_names);
CREATE INDEX idx_practitioners_active ON practitioners(active);
CREATE INDEX idx_practitioners_gender ON practitioners(gender);
CREATE INDEX idx_practitioners_birth_date ON practitioners(birth_date);
CREATE INDEX idx_practitioners_created_at ON practitioners(created_at);
CREATE INDEX idx_practitioners_identifiers ON practitioners USING GIN(identifiers);
CREATE INDEX idx_practitioners_qualifications ON practitioners USING GIN(qualifications);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$ language 'plpgsql';

CREATE TRIGGER update_practitioners_updated_at 
    BEFORE UPDATE ON practitioners 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample practitioners
INSERT INTO practitioners (
    fhir_id, family_name, given_names, prefix, suffix, gender, birth_date, 
    identifiers, telecom, addresses, qualifications, communication, active
) VALUES 
(
    'pract-001', 
    'Smith', 
    ARRAY['John', 'Robert'], 
    'Dr.',
    'MD',
    'male', 
    '1975-03-15',
    '[
        {"system": "NPI", "value": "1234567890", "use": "official"},
        {"system": "DEA", "value": "BS1234567", "use": "official"}
    ]'::jsonb,
    '[
        {"system": "phone", "value": "+1-555-0123", "use": "work"},
        {"system": "email", "value": "dr.smith@hospital.com", "use": "work"}
    ]'::jsonb,
    '[
        {
            "use": "work", 
            "line": ["123 Medical Center Dr"], 
            "city": "Boston", 
            "state": "MA", 
            "postal_code": "02101", 
            "country": "USA"
        }
    ]'::jsonb,
    '[
        {
            "code": {"text": "Doctor of Medicine"},
            "issuer": {"display": "Harvard Medical School"},
            "period": {"start": "1997-05-15", "end": "2001-05-15"}
        },
        {
            "code": {"text": "Board Certification in Cardiology"},
            "issuer": {"display": "American Board of Internal Medicine"},
            "period": {"start": "2005-01-01"}
        }
    ]'::jsonb,
    '[
        {"language": {"text": "English"}, "preferred": true},
        {"language": {"text": "Spanish"}, "preferred": false}
    ]'::jsonb,
    true
),
(
    'pract-002', 
    'Johnson', 
    ARRAY['Sarah', 'Marie'], 
    'Dr.',
    'RN, MSN',
    'female', 
    '1982-07-22',
    '[
        {"system": "NPI", "value": "9876543210", "use": "official"},
        {"system": "LICENSE", "value": "RN123456", "use": "official"}
    ]'::jsonb,
    '[
        {"system": "phone", "value": "+1-555-0456", "use": "work"},
        {"system": "email", "value": "s.johnson@clinic.com", "use": "work"}
    ]'::jsonb,
    '[
        {
            "use": "work", 
            "line": ["456 Healthcare Blvd", "Suite 200"], 
            "city": "Cambridge", 
            "state": "MA", 
            "postal_code": "02139", 
            "country": "USA"
        }
    ]'::jsonb,
    '[
        {
            "code": {"text": "Bachelor of Science in Nursing"},
            "issuer": {"display": "Boston University"},
            "period": {"start": "2000-09-01", "end": "2004-05-15"}
        },
        {
            "code": {"text": "Master of Science in Nursing"},
            "issuer": {"display": "Northeastern University"},
            "period": {"start": "2010-09-01", "end": "2012-12-15"}
        }
    ]'::jsonb,
    '[
        {"language": {"text": "English"}, "preferred": true},
        {"language": {"text": "French"}, "preferred": false}
    ]'::jsonb,
    true
),
(
    'pract-003', 
    'Williams', 
    ARRAY['Robert', 'James'], 
    'Dr.',
    'PhD, LCSW',
    'male', 
    '1978-12-03',
    '[
        {"system": "NPI", "value": "5555666677", "use": "official"},
        {"system": "LICENSE", "value": "LCSW98765", "use": "official"}
    ]'::jsonb,
    '[
        {"system": "phone", "value": "+1-555-0789", "use": "work"},
        {"system": "email", "value": "r.williams@mentalhealth.com", "use": "work"}
    ]'::jsonb,
    '[
        {
            "use": "work", 
            "line": ["789 Wellness Center"], 
            "city": "Somerville", 
            "state": "MA", 
            "postal_code": "02143", 
            "country": "USA"
        }
    ]'::jsonb,
    '[
        {
            "code": {"text": "Doctor of Philosophy in Psychology"},
            "issuer": {"display": "MIT"},
            "period": {"start": "1996-09-01", "end": "2002-05-15"}
        },
        {
            "code": {"text": "Licensed Clinical Social Worker"},
            "issuer": {"display": "Massachusetts Board of Health"},
            "period": {"start": "2003-01-01"}
        }
    ]'::jsonb,
    '[
        {"language": {"text": "English"}, "preferred": true},
        {"language": {"text": "Portuguese"}, "preferred": false}
    ]'::jsonb,
    true
),
(
    'pract-004', 
    'Davis', 
    ARRAY['Emily', 'Claire'], 
    'Dr.',
    'PharmD',
    'female', 
    '1985-04-18',
    '[
        {"system": "NPI", "value": "1122334455", "use": "official"},
        {"system": "LICENSE", "value": "RPH54321", "use": "official"}
    ]'::jsonb,
    '[
        {"system": "phone", "value": "+1-555-0321", "use": "work"},
        {"system": "email", "value": "e.davis@pharmacy.com", "use": "work"}
    ]'::jsonb,
    '[
        {
            "use": "work", 
            "line": ["321 Pharmacy Lane"], 
            "city": "Brookline", 
            "state": "MA", 
            "postal_code": "02446", 
            "country": "USA"
        }
    ]'::jsonb,
    '[
        {
            "code": {"text": "Doctor of Pharmacy"},
            "issuer": {"display": "Massachusetts College of Pharmacy"},
            "period": {"start": "2003-09-01", "end": "2007-05-15"}
        },
        {
            "code": {"text": "Board Certification in Pharmacotherapy"},
            "issuer": {"display": "Board of Pharmacy Specialties"},
            "period": {"start": "2009-01-01"}
        }
    ]'::jsonb,
    '[
        {"language": {"text": "English"}, "preferred": true},
        {"language": {"text": "Mandarin"}, "preferred": false}
    ]'::jsonb,
    true
);

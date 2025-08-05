-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create required tables for foreign key references
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS practitioners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS encounters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID,
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FHIR DocumentReference Resource (for intake forms, scanned documents)
-- ============================================================================
CREATE TABLE document_references (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Master Identifier
    master_identifier JSONB, -- Identifier object
    
    -- Identifiers
    identifiers JSONB, -- Array of identifier objects
    
    -- Status
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'current', 'superseded', 'entered-in-error'
    )),
    
    -- Doc Status
    doc_status VARCHAR(50) CHECK (doc_status IN (
        'preliminary', 'final', 'amended', 'entered-in-error'
    )),
    
    -- Type
    type JSONB, -- CodeableConcept
    
    -- Category
    categories JSONB, -- Array of CodeableConcept
    
    -- Subject (patient)
    subject_patient_id UUID NOT NULL,
    
    -- Date
    date_time TIMESTAMP WITH TIME ZONE,
    
    -- Authors
    authors JSONB, -- Array of references
    
    -- Authenticator
    authenticator UUID,
    
    -- Custodian
    custodian UUID,
    
    -- Related Identifiers
    relates_to JSONB, -- Array of related document objects
    
    -- Description
    description TEXT,
    
    -- Security Label
    security_labels JSONB, -- Array of CodeableConcept
    
    -- Content
    content JSONB NOT NULL, -- Array of content attachments
    
    -- Context
    context JSONB, -- Document context
    
    -- FHIR Metadata
    fhir_resource JSONB,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (subject_patient_id) REFERENCES patients(id),
    FOREIGN KEY (authenticator) REFERENCES practitioners(id),
    FOREIGN KEY (custodian) REFERENCES organizations(id)
);

-- Indexes for document_references
CREATE INDEX idx_document_references_fhir_id ON document_references(fhir_id);
CREATE INDEX idx_document_references_patient ON document_references(subject_patient_id);
CREATE INDEX idx_document_references_type ON document_references USING GIN(type);
CREATE INDEX idx_document_references_date ON document_references(date_time);

-- ============================================================================
-- FHIR Questionnaire Resource (for intake forms)
-- ============================================================================
CREATE TABLE questionnaires (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- URL (canonical identifier)
    url VARCHAR(500),
    
    -- Identifiers
    identifiers JSONB, -- Array of identifier objects
    
    -- Version
    version VARCHAR(100),
    
    -- Name
    name VARCHAR(255),
    
    -- Title
    title VARCHAR(500),
    
    -- Derived From
    derived_from TEXT[],
    
    -- Status
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'draft', 'active', 'retired', 'unknown'
    )),
    
    -- Experimental
    experimental BOOLEAN DEFAULT FALSE,
    
    -- Subject Types
    subject_types TEXT[] CHECK (subject_types <@ ARRAY[
        'Patient', 'Person', 'Organization', 'Practitioner', 
        'Device', 'Medication', 'Substance'
    ]),
    
    -- Date
    date_time TIMESTAMP WITH TIME ZONE,
    
    -- Publisher
    publisher VARCHAR(500),
    
    -- Contact
    contacts JSONB, -- Array of ContactDetail
    
    -- Description
    description TEXT,
    
    -- Use Context
    use_contexts JSONB, -- Array of UsageContext
    
    -- Jurisdiction
    jurisdictions JSONB, -- Array of CodeableConcept
    
    -- Purpose
    purpose TEXT,
    
    -- Copyright
    copyright TEXT,
    
    -- Approval Date
    approval_date DATE,
    
    -- Last Review Date
    last_review_date DATE,
    
    -- Effective Period
    effective_period JSONB, -- Period object
    
    -- Code (questionnaire classification)
    codes JSONB, -- Array of Coding
    
    -- Items (questionnaire structure)
    items JSONB NOT NULL, -- Array of questionnaire items
    
    -- FHIR Metadata
    fhir_resource JSONB,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for questionnaires
CREATE INDEX idx_questionnaires_fhir_id ON questionnaires(fhir_id);
CREATE INDEX idx_questionnaires_url ON questionnaires(url);
CREATE INDEX idx_questionnaires_status ON questionnaires(status);
CREATE INDEX idx_questionnaires_items ON questionnaires USING GIN(items);

-- ============================================================================
-- FHIR QuestionnaireResponse Resource (patient intake responses)
-- ============================================================================
CREATE TABLE questionnaire_responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Identifier
    identifier JSONB, -- Identifier object
    
    -- Based On
    based_on JSONB, -- Array of references
    
    -- Part Of
    part_of JSONB, -- Array of references
    
    -- Questionnaire
    questionnaire_id UUID,
    questionnaire_canonical VARCHAR(500),
    
    -- Status
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'in-progress', 'completed', 'amended', 'entered-in-error', 'stopped'
    )),
    
    -- Subject (patient)
    subject_patient_id UUID NOT NULL,
    
    -- Encounter
    encounter_id UUID,
    
    -- Authored
    authored TIMESTAMP WITH TIME ZONE,
    
    -- Author
    author_patient_id UUID,
    author_practitioner_id UUID,
    author_device_id UUID,
    author_organization_id UUID,
    
    -- Source
    source_patient_id UUID,
    source_practitioner_id UUID,
    source_related_person_id UUID,
    
    -- Items (responses)
    items JSONB, -- Array of response items
    
    -- FHIR Metadata
    fhir_resource JSONB,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (questionnaire_id) REFERENCES questionnaires(id),
    FOREIGN KEY (subject_patient_id) REFERENCES patients(id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(id),
    FOREIGN KEY (author_patient_id) REFERENCES patients(id),
    FOREIGN KEY (author_practitioner_id) REFERENCES practitioners(id),
    FOREIGN KEY (source_patient_id) REFERENCES patients(id),
    FOREIGN KEY (source_practitioner_id) REFERENCES practitioners(id)
);

-- Indexes for questionnaire_responses
CREATE INDEX idx_questionnaire_responses_fhir_id ON questionnaire_responses(fhir_id);
CREATE INDEX idx_questionnaire_responses_patient ON questionnaire_responses(subject_patient_id);
CREATE INDEX idx_questionnaire_responses_encounter ON questionnaire_responses(encounter_id);
CREATE INDEX idx_questionnaire_responses_questionnaire ON questionnaire_responses(questionnaire_id);
CREATE INDEX idx_questionnaire_responses_status ON questionnaire_responses(status);
CREATE INDEX idx_questionnaire_responses_authored ON questionnaire_responses(authored);

-- Insert sample data
INSERT INTO patients (id, name) VALUES 
    ('00000000-0000-0000-0000-000000000001', 'John Doe'),
    ('00000000-0000-0000-0000-000000000002', 'Jane Smith'),
    ('11111111-1111-1111-1111-111111111111', 'Alice Johnson'),
    ('22222222-2222-2222-2222-222222222222', 'Bob Wilson')
ON CONFLICT (id) DO NOTHING;

INSERT INTO practitioners (id, name) VALUES 
    ('00000000-0000-0000-0000-000000000001', 'Dr. Johnson'),
    ('00000000-0000-0000-0000-000000000002', 'Dr. Williams'),
    ('33333333-3333-3333-3333-333333333333', 'Dr. Sarah Davis'),
    ('44444444-4444-4444-4444-444444444444', 'Dr. Michael Brown')
ON CONFLICT (id) DO NOTHING;

INSERT INTO organizations (id, name) VALUES 
    ('00000000-0000-0000-0000-000000000001', 'General Hospital'),
    ('00000000-0000-0000-0000-000000000002', 'Medical Center'),
    ('55555555-5555-5555-5555-555555555555', 'City Health Clinic'),
    ('66666666-6666-6666-6666-666666666666', 'Regional Medical Group')
ON CONFLICT (id) DO NOTHING;

INSERT INTO encounters (id, patient_id, status) VALUES 
    ('77777777-7777-7777-7777-777777777777', '00000000-0000-0000-0000-000000000001', 'finished'),
    ('88888888-8888-8888-8888-888888888888', '00000000-0000-0000-0000-000000000002', 'in-progress'),
    ('99999999-9999-9999-9999-999999999999', '11111111-1111-1111-1111-111111111111', 'planned')
ON CONFLICT (id) DO NOTHING;

-- Insert sample document references
INSERT INTO document_references (
    fhir_id, 
    status, 
    subject_patient_id, 
    description, 
    content,
    date_time
) VALUES 
    (
        'DOC-001', 
        'current', 
        '00000000-0000-0000-0000-000000000001', 
        'Patient intake form for John Doe',
        '[{"attachment": {"contentType": "application/pdf", "title": "Intake Form", "size": 2048}}]',
        NOW()
    ),
    (
        'DOC-002', 
        'current', 
        '00000000-0000-0000-0000-000000000002', 
        'Lab results for Jane Smith',
        '[{"attachment": {"contentType": "application/pdf", "title": "Lab Results", "size": 1024}}]',
        NOW()
    ),
    (
        'DOC-003', 
        'current', 
        '11111111-1111-1111-1111-111111111111', 
        'Medical history document',
        '[{"attachment": {"contentType": "text/plain", "title": "Medical History", "size": 512}}]',
        NOW()
    )
ON CONFLICT (fhir_id) DO NOTHING;

-- Insert sample questionnaires
INSERT INTO questionnaires (
    fhir_id,
    title,
    status,
    description,
    items
) VALUES 
    (
        'Q-001',
        'Patient Health Assessment',
        'active',
        'Standard patient health assessment questionnaire',
        '[
            {
                "linkId": "1",
                "text": "What is your primary health concern?",
                "type": "text"
            },
            {
                "linkId": "2", 
                "text": "Rate your pain level (1-10)",
                "type": "integer"
            },
            {
                "linkId": "3",
                "text": "Do you have any allergies?",
                "type": "boolean"
            }
        ]'
    ),
    (
        'Q-002',
        'Mental Health Screening',
        'active',
        'Brief mental health screening questionnaire',
        '[
            {
                "linkId": "1",
                "text": "How often do you feel sad or depressed?",
                "type": "choice"
            },
            {
                "linkId": "2",
                "text": "Rate your stress level (1-10)", 
                "type": "integer"
            }
        ]'
    ),
    (
        'Q-003',
        'Medication Review',
        'draft',
        'Review of current medications',
        '[
            {
                "linkId": "1",
                "text": "List all current medications",
                "type": "text"
            },
            {
                "linkId": "2",
                "text": "Any medication side effects?",
                "type": "text"
            }
        ]'
    )
ON CONFLICT (fhir_id) DO NOTHING;

-- Insert sample questionnaire responses
INSERT INTO questionnaire_responses (
    fhir_id,
    questionnaire_id,
    status,
    subject_patient_id,
    authored,
    items
) VALUES 
    (
        'QR-001',
        (SELECT id FROM questionnaires WHERE fhir_id = 'Q-001'),
        'completed',
        '00000000-0000-0000-0000-000000000001',
        NOW(),
        '[
            {
                "linkId": "1",
                "text": "What is your primary health concern?",
                "answer": [{"valueString": "Chronic back pain"}]
            },
            {
                "linkId": "2",
                "text": "Rate your pain level (1-10)",
                "answer": [{"valueInteger": 7}]
            },
            {
                "linkId": "3", 
                "text": "Do you have any allergies?",
                "answer": [{"valueBoolean": true}]
            }
        ]'
    ),
    (
        'QR-002',
        (SELECT id FROM questionnaires WHERE fhir_id = 'Q-002'),
        'completed',
        '00000000-0000-0000-0000-000000000002',
        NOW(),
        '[
            {
                "linkId": "1",
                "text": "How often do you feel sad or depressed?",
                "answer": [{"valueString": "Sometimes"}]
            },
            {
                "linkId": "2",
                "text": "Rate your stress level (1-10)",
                "answer": [{"valueInteger": 5}]
            }
        ]'
    ),
    (
        'QR-003',
        (SELECT id FROM questionnaires WHERE fhir_id = 'Q-001'),
        'in-progress',
        '11111111-1111-1111-1111-111111111111',
        NOW(),
        '[
            {
                "linkId": "1",
                "text": "What is your primary health concern?",
                "answer": [{"valueString": "Regular checkup"}]
            }
        ]'
    )
ON CONFLICT (fhir_id) DO NOTHING;

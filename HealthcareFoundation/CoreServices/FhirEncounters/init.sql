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

-- Create encounters table
CREATE TABLE IF NOT EXISTS encounters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL,
    class JSONB,
    type JSONB,
    service_type JSONB,
    priority JSONB,
    subject_patient_id UUID NOT NULL,
    episode_of_care JSONB,
    incoming_referral JSONB,
    participants JSONB,
    appointment UUID,
    period_start TIMESTAMP WITH TIME ZONE,
    period_end TIMESTAMP WITH TIME ZONE,
    length_value DECIMAL,
    length_unit VARCHAR(50),
    reason_code JSONB,
    reason_reference JSONB,
    diagnosis JSONB,
    account JSONB,
    hospitalization JSONB,
    locations JSONB,
    service_provider UUID,
    part_of UUID,
    fhir_resource JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT encounters_status_check CHECK (status IN ('planned', 'arrived', 'triaged', 'in-progress', 'onleave', 'finished', 'cancelled', 'entered-in-error', 'unknown'))
);

-- Create observations table
CREATE TABLE IF NOT EXISTS observations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL,
    category JSONB,
    code JSONB NOT NULL,
    subject_patient_id UUID NOT NULL,
    encounter_id UUID REFERENCES encounters(id),
    effective_date_time TIMESTAMP WITH TIME ZONE,
    effective_period_start TIMESTAMP WITH TIME ZONE,
    effective_period_end TIMESTAMP WITH TIME ZONE,
    effective_instant TIMESTAMP WITH TIME ZONE,
    issued TIMESTAMP WITH TIME ZONE,
    performers JSONB,
    value_quantity_value DECIMAL,
    value_quantity_unit VARCHAR(100),
    value_quantity_system VARCHAR(500),
    value_quantity_code VARCHAR(100),
    value_codeable_concept JSONB,
    value_string TEXT,
    value_boolean BOOLEAN,
    value_integer INTEGER,
    value_range JSONB,
    value_ratio JSONB,
    value_sampled_data JSONB,
    value_time TIME,
    value_date_time TIMESTAMP WITH TIME ZONE,
    value_period JSONB,
    data_absent_reason JSONB,
    interpretation JSONB,
    notes JSONB,
    body_site JSONB,
    method JSONB,
    specimen UUID,
    device UUID,
    reference_ranges JSONB,
    has_member JSONB,
    derived_from JSONB,
    components JSONB,
    fhir_resource JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT observations_status_check CHECK (status IN ('registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown'))
);

-- Create conditions table
CREATE TABLE IF NOT EXISTS conditions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fhir_id VARCHAR(255) UNIQUE NOT NULL,
    clinical_status VARCHAR(50),
    verification_status VARCHAR(50),
    category JSONB,
    severity JSONB,
    code JSONB,
    body_sites JSONB,
    subject_patient_id UUID NOT NULL,
    encounter_id UUID REFERENCES encounters(id),
    onset_date_time TIMESTAMP WITH TIME ZONE,
    onset_age JSONB,
    onset_period JSONB,
    onset_range JSONB,
    onset_string VARCHAR(500),
    abatement_date_time TIMESTAMP WITH TIME ZONE,
    abatement_age JSONB,
    abatement_period JSONB,
    abatement_range JSONB,
    abatement_string VARCHAR(500),
    abatement_boolean BOOLEAN,
    recorded_date TIMESTAMP,
    recorder UUID,
    asserter UUID,
    stages JSONB,
    evidence JSONB,
    notes JSONB,
    fhir_resource JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT conditions_clinical_status_check CHECK (clinical_status IN ('active', 'recurrence', 'relapse', 'inactive', 'remission', 'resolved', 'unknown')),
    CONSTRAINT conditions_verification_status_check CHECK (verification_status IN ('unconfirmed', 'provisional', 'differential', 'confirmed', 'refuted', 'entered-in-error'))
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

-- Insert sample Observations
INSERT INTO observations (fhir_id, status, category, code, subject_patient_id, effective_date_time, value_quantity_value, value_quantity_unit, value_string, interpretation) VALUES 
-- Blood Pressure Readings
('obs-bp-001', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "85354-9", "display": "Blood pressure panel with all children optional"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 10:30:00+00', 120, 'mmHg', 'Systolic: 120, Diastolic: 80', '[{"coding": [{"code": "normal", "display": "Normal"}]}]'),
('obs-bp-002', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "85354-9", "display": "Blood pressure panel with all children optional"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2024-01-16 14:15:00+00', 135, 'mmHg', 'Systolic: 135, Diastolic: 85', '[{"coding": [{"code": "high", "display": "High"}]}]'),
('obs-bp-003', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "85354-9", "display": "Blood pressure panel with all children optional"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2024-01-17 09:45:00+00', 110, 'mmHg', 'Systolic: 110, Diastolic: 70', '[{"coding": [{"code": "normal", "display": "Normal"}]}]'),

-- Heart Rate
('obs-hr-001', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "8867-4", "display": "Heart rate"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 10:30:00+00', 72, 'beats/min', NULL, '[{"coding": [{"code": "normal", "display": "Normal"}]}]'),
('obs-hr-002', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "8867-4", "display": "Heart rate"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2024-01-16 14:15:00+00', 85, 'beats/min', NULL, '[{"coding": [{"code": "high", "display": "High"}]}]'),

-- Body Temperature
('obs-temp-001', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "8310-5", "display": "Body temperature"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 10:30:00+00', 98.6, 'F', NULL, '[{"coding": [{"code": "normal", "display": "Normal"}]}]'),
('obs-temp-002', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "8310-5", "display": "Body temperature"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2024-01-17 09:45:00+00', 99.2, 'F', NULL, '[{"coding": [{"code": "high", "display": "High"}]}]'),

-- Lab Results - Blood Glucose
('obs-glucose-001', 'final', '[{"coding": [{"code": "laboratory", "display": "Laboratory"}]}]', '{"coding": [{"code": "2339-0", "display": "Glucose [Mass/volume] in Blood"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2024-01-16 08:00:00+00', 95, 'mg/dL', NULL, '[{"coding": [{"code": "normal", "display": "Normal"}]}]'),
('obs-glucose-002', 'final', '[{"coding": [{"code": "laboratory", "display": "Laboratory"}]}]', '{"coding": [{"code": "2339-0", "display": "Glucose [Mass/volume] in Blood"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 07:30:00+00', 140, 'mg/dL', NULL, '[{"coding": [{"code": "high", "display": "High"}]}]'),

-- Lab Results - Cholesterol
('obs-chol-001', 'final', '[{"coding": [{"code": "laboratory", "display": "Laboratory"}]}]', '{"coding": [{"code": "14647-2", "display": "Cholesterol [Mass/volume] in Serum or Plasma"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 07:30:00+00', 220, 'mg/dL', NULL, '[{"coding": [{"code": "high", "display": "High"}]}]'),
('obs-chol-002', 'final', '[{"coding": [{"code": "laboratory", "display": "Laboratory"}]}]', '{"coding": [{"code": "14647-2", "display": "Cholesterol [Mass/volume] in Serum or Plasma"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2024-01-17 08:15:00+00', 180, 'mg/dL', NULL, '[{"coding": [{"code": "normal", "display": "Normal"}]}]'),

-- Height and Weight
('obs-height-001', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "8302-2", "display": "Body height"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 10:30:00+00', 175, 'cm', NULL, '[{"coding": [{"code": "normal", "display": "Normal"}]}]'),
('obs-weight-001', 'final', '[{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}]', '{"coding": [{"code": "29463-7", "display": "Body weight"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 10:30:00+00', 75, 'kg', NULL, '[{"coding": [{"code": "normal", "display": "Normal"}]}]'),

-- String-based observations
('obs-pain-001', 'final', '[{"coding": [{"code": "survey", "display": "Survey"}]}]', '{"coding": [{"code": "72514-3", "display": "Pain severity - 0-10 verbal numeric rating [Score] - Reported"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2024-01-16 14:15:00+00', NULL, NULL, '3', '[{"coding": [{"code": "low", "display": "Low"}]}]'),
('obs-allergy-001', 'final', '[{"coding": [{"code": "allergy", "display": "Allergy"}]}]', '{"coding": [{"code": "716186003", "display": "No known allergy"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 10:30:00+00', NULL, NULL, 'No known allergies', '[{"coding": [{"code": "normal", "display": "Normal"}]}]')
ON CONFLICT (fhir_id) DO NOTHING;

-- Insert sample Conditions
INSERT INTO conditions (fhir_id, clinical_status, verification_status, category, severity, code, subject_patient_id, onset_date_time, recorded_date) VALUES 
-- Chronic Conditions
('condition-diabetes-001', 'active', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "moderate", "display": "Moderate"}]}', '{"coding": [{"code": "E11.9", "display": "Type 2 diabetes mellitus without complications"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2020-03-15 00:00:00+00', '2020-03-15'),
('condition-hypertension-001', 'active', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "mild", "display": "Mild"}]}', '{"coding": [{"code": "I10", "display": "Essential (primary) hypertension"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2019-07-20 00:00:00+00', '2019-07-20'),
('condition-asthma-001', 'active', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "mild", "display": "Mild"}]}', '{"coding": [{"code": "J45.909", "display": "Unspecified asthma with (acute) exacerbation"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2018-11-10 00:00:00+00', '2018-11-10'),

-- Resolved Conditions
('condition-pneumonia-001', 'resolved', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "moderate", "display": "Moderate"}]}', '{"coding": [{"code": "J18.9", "display": "Pneumonia, unspecified organism"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2023-12-01 00:00:00+00', '2023-12-01'),
('condition-fracture-001', 'resolved', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "moderate", "display": "Moderate"}]}', '{"coding": [{"code": "S52.501A", "display": "Unspecified fracture of the lower end of right radius, initial encounter for closed fracture"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2023-08-15 00:00:00+00', '2023-08-15'),

-- Inactive Conditions
('condition-depression-001', 'inactive', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "mild", "display": "Mild"}]}', '{"coding": [{"code": "F32.9", "display": "Major depressive disorder, unspecified"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2022-05-10 00:00:00+00', '2022-05-10'),

-- Provisional Conditions
('condition-allergy-001', 'active', 'provisional', '[{"coding": [{"code": "allergy", "display": "Allergy"}]}]', '{"coding": [{"code": "moderate", "display": "Moderate"}]}', '{"coding": [{"code": "Z91.010", "display": "Allergy to peanuts"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2021-06-20 00:00:00+00', '2021-06-20'),
('condition-allergy-002', 'active', 'confirmed', '[{"coding": [{"code": "allergy", "display": "Allergy"}]}]', '{"coding": [{"code": "severe", "display": "Severe"}]}', '{"coding": [{"code": "Z91.012", "display": "Allergy to bee venom"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2020-09-15 00:00:00+00', '2020-09-15'),

-- Cardiovascular Conditions
('condition-hyperlipidemia-001', 'active', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "mild", "display": "Mild"}]}', '{"coding": [{"code": "E78.5", "display": "Disorder of lipoprotein metabolism, unspecified"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2021-01-10 00:00:00+00', '2021-01-10'),
('condition-heart-disease-001', 'active', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "moderate", "display": "Moderate"}]}', '{"coding": [{"code": "I25.10", "display": "Atherosclerotic heart disease of native coronary artery without angina pectoris"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2022-03-05 00:00:00+00', '2022-03-05'),

-- Musculoskeletal Conditions
('condition-arthritis-001', 'active', 'confirmed', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "moderate", "display": "Moderate"}]}', '{"coding": [{"code": "M15.9", "display": "Polyosteoarthritis, unspecified site"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2020-12-01 00:00:00+00', '2020-12-01'),
('condition-back-pain-001', 'active', 'provisional', '[{"coding": [{"code": "problem-list-item", "display": "Problem List Item"}]}]', '{"coding": [{"code": "mild", "display": "Mild"}]}', '{"coding": [{"code": "M54.5", "display": "Low back pain"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-10 00:00:00+00', '2024-01-10')
ON CONFLICT (fhir_id) DO NOTHING;

-- Insert sample Encounters
INSERT INTO encounters (fhir_id, status, class, type, service_type, priority, subject_patient_id, period_start, period_end, length_value, length_unit, reason_code, diagnosis) VALUES 
-- Routine Check-ups
('encounter-checkup-001', 'finished', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-15 10:00:00+00', '2024-01-15 11:00:00+00', 60, 'min', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '[{"condition": {"reference": "Condition/condition-diabetes-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),
('encounter-checkup-002', 'finished', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2024-01-16 14:00:00+00', '2024-01-16 15:00:00+00', 60, 'min', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '[{"condition": {"reference": "Condition/condition-hypertension-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),
('encounter-checkup-003', 'finished', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2024-01-17 09:00:00+00', '2024-01-17 10:00:00+00', 60, 'min', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '[{"condition": {"reference": "Condition/condition-asthma-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),

-- Emergency Department Visits
('encounter-ed-001', 'finished', '{"coding": [{"code": "EMER", "display": "Emergency"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "2", "display": "Surgical Care"}]}', '{"coding": [{"code": "urgent", "display": "Urgent"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2023-12-01 08:00:00+00', '2023-12-01 12:00:00+00', 240, 'min', '[{"coding": [{"code": "R50.9", "display": "Fever, unspecified"}]}]', '[{"condition": {"reference": "Condition/condition-pneumonia-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),
('encounter-ed-002', 'finished', '{"coding": [{"code": "EMER", "display": "Emergency"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "2", "display": "Surgical Care"}]}', '{"coding": [{"code": "urgent", "display": "Urgent"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2023-08-15 16:00:00+00', '2023-08-15 20:00:00+00', 240, 'min', '[{"coding": [{"code": "S52.501A", "display": "Unspecified fracture of the lower end of right radius"}]}]', '[{"condition": {"reference": "Condition/condition-fracture-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),

-- Specialist Consultations
('encounter-cardio-001', 'finished', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-20 13:00:00+00', '2024-01-20 14:30:00+00', 90, 'min', '[{"coding": [{"code": "I10", "display": "Essential (primary) hypertension"}]}]', '[{"condition": {"reference": "Condition/condition-hyperlipidemia-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),
('encounter-cardio-002', 'finished', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2024-01-22 10:00:00+00', '2024-01-22 11:30:00+00', 90, 'min', '[{"coding": [{"code": "I25.10", "display": "Atherosclerotic heart disease"}]}]', '[{"condition": {"reference": "Condition/condition-heart-disease-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),

-- Inpatient Hospitalizations
('encounter-inpatient-001', 'finished', '{"coding": [{"code": "IMP", "display": "Inpatient encounter"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "urgent", "display": "Urgent"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2023-12-01 12:00:00+00', '2023-12-05 10:00:00+00', 5760, 'min', '[{"coding": [{"code": "J18.9", "display": "Pneumonia, unspecified organism"}]}]', '[{"condition": {"reference": "Condition/condition-pneumonia-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),
('encounter-inpatient-002', 'finished', '{"coding": [{"code": "IMP", "display": "Inpatient encounter"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "2", "display": "Surgical Care"}]}', '{"coding": [{"code": "urgent", "display": "Urgent"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2023-08-15 20:00:00+00', '2023-08-18 14:00:00+00', 4320, 'min', '[{"coding": [{"code": "S52.501A", "display": "Unspecified fracture of the lower end of right radius"}]}]', '[{"condition": {"reference": "Condition/condition-fracture-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),

-- Planned Appointments
('encounter-planned-001', 'planned', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-02-15 10:00:00+00', '2024-02-15 11:00:00+00', 60, 'min', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', NULL),
('encounter-planned-002', 'planned', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2024-02-20 14:00:00+00', '2024-02-20 15:00:00+00', 60, 'min', '[{"coding": [{"code": "I10", "display": "Essential (primary) hypertension"}]}]', NULL),
('encounter-planned-003', 'planned', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2024-02-25 09:00:00+00', '2024-02-25 10:00:00+00', 60, 'min', '[{"coding": [{"code": "J45.909", "display": "Unspecified asthma"}]}]', NULL),

-- Urgent Care Visits
('encounter-urgent-001', 'finished', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "308335008", "display": "Patient encounter procedure"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "urgent", "display": "Urgent"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2024-01-10 18:00:00+00', '2024-01-10 19:30:00+00', 90, 'min', '[{"coding": [{"code": "J45.909", "display": "Unspecified asthma with (acute) exacerbation"}]}]', '[{"condition": {"reference": "Condition/condition-asthma-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),

-- Follow-up Visits
('encounter-followup-001', 'finished', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-001'), '2024-01-25 11:00:00+00', '2024-01-25 11:30:00+00', 30, 'min', '[{"coding": [{"code": "Z51.11", "display": "Encounter for antineoplastic chemotherapy"}]}]', '[{"condition": {"reference": "Condition/condition-diabetes-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),
('encounter-followup-002', 'finished', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-002'), '2024-01-28 15:00:00+00', '2024-01-28 15:30:00+00', 30, 'min', '[{"coding": [{"code": "Z51.11", "display": "Encounter for antineoplastic chemotherapy"}]}]', '[{"condition": {"reference": "Condition/condition-hypertension-001"}, "rank": 1, "use": {"coding": [{"code": "AD", "display": "Admission diagnosis"}]}}]'),

-- Cancelled Appointments
('encounter-cancelled-001', 'cancelled', '{"coding": [{"code": "AMB", "display": "Ambulatory"}]}', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', '{"coding": [{"code": "1", "display": "Medical Care"}]}', '{"coding": [{"code": "routine", "display": "Routine"}]}', (SELECT id FROM patients WHERE fhir_id = 'patient-003'), '2024-01-30 10:00:00+00', '2024-01-30 11:00:00+00', 60, 'min', '[{"coding": [{"code": "185389000", "display": "Routine medical examination"}]}]', NULL)
ON CONFLICT (fhir_id) DO NOTHING;

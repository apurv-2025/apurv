-- Healthcare Patient Portal Database Initialization
-- This script creates the database schema and inserts sample data

-- Create database if it doesn't exist
-- CREATE DATABASE healthcare_portal;

-- Connect to the database
-- \c healthcare_portal;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    date_of_birth DATE,
    insurance_provider VARCHAR(100),
    insurance_id VARCHAR(50),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    appointment_date TIMESTAMP NOT NULL,
    appointment_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create medications table
CREATE TABLE IF NOT EXISTS medications (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    prescriber_id INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    refills_remaining INTEGER DEFAULT 0,
    instructions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create lab_results table
CREATE TABLE IF NOT EXISTS lab_results (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ordering_doctor_id INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    test_name VARCHAR(255) NOT NULL,
    test_date DATE NOT NULL,
    result_value VARCHAR(255),
    reference_range VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    notes TEXT,
    file_path VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    recipient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create surveys table
CREATE TABLE IF NOT EXISTS surveys (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    survey_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create survey_questions table
CREATE TABLE IF NOT EXISTS survey_questions (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER NOT NULL REFERENCES surveys(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    options JSONB,
    required BOOLEAN DEFAULT TRUE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create survey_responses table
CREATE TABLE IF NOT EXISTS survey_responses (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER NOT NULL REFERENCES surveys(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    appointment_id INTEGER REFERENCES appointments(id) ON DELETE SET NULL,
    conversation_id VARCHAR(255),
    response_data JSONB NOT NULL,
    overall_rating FLOAT CHECK (overall_rating >= 1 AND overall_rating <= 5),
    feedback_text TEXT,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_doctors_email ON doctors(email);
CREATE INDEX IF NOT EXISTS idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor_id ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_medications_patient_id ON medications(patient_id);
CREATE INDEX IF NOT EXISTS idx_medications_prescriber_id ON medications(prescriber_id);
CREATE INDEX IF NOT EXISTS idx_lab_results_patient_id ON lab_results(patient_id);
CREATE INDEX IF NOT EXISTS idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_surveys_type ON surveys(survey_type);
CREATE INDEX IF NOT EXISTS idx_surveys_active ON surveys(is_active);
CREATE INDEX IF NOT EXISTS idx_survey_questions_survey_id ON survey_questions(survey_id);
CREATE INDEX IF NOT EXISTS idx_survey_questions_order ON survey_questions(survey_id, order_index);
CREATE INDEX IF NOT EXISTS idx_survey_responses_survey_id ON survey_responses(survey_id);
CREATE INDEX IF NOT EXISTS idx_survey_responses_user_id ON survey_responses(user_id);
CREATE INDEX IF NOT EXISTS idx_survey_responses_appointment_id ON survey_responses(appointment_id);
CREATE INDEX IF NOT EXISTS idx_survey_responses_conversation_id ON survey_responses(conversation_id);

-- Insert sample doctors
INSERT INTO doctors (first_name, last_name, specialty, email, phone) VALUES
('Dr. Sarah', 'Johnson', 'Cardiology', 'sarah.johnson@healthcare.com', '555-0101'),
('Dr. Michael', 'Chen', 'Internal Medicine', 'michael.chen@healthcare.com', '555-0102'),
('Dr. Emily', 'Davis', 'Pediatrics', 'emily.davis@healthcare.com', '555-0103'),
('Dr. Robert', 'Wilson', 'Orthopedics', 'robert.wilson@healthcare.com', '555-0104'),
('Dr. Lisa', 'Brown', 'Dermatology', 'lisa.brown@healthcare.com', '555-0105')
ON CONFLICT (email) DO NOTHING;

-- Insert sample users (passwords are hashed versions of 'password123' and 'testpassword123')
INSERT INTO users (email, hashed_password, first_name, last_name, phone, address, date_of_birth, insurance_provider, insurance_id, emergency_contact_name, emergency_contact_phone) VALUES
('john.doe@example.com', '$2b$12$DdOiqvLumbzkhVcsVthSLO.hE5NKEu9WrJpGEZtsLLko8GpEkIu4K', 'John', 'Doe', '555-0201', '123 Main St, City, State', '1990-05-15', 'Blue Cross', 'BC123456', 'Jane Doe', '555-0202'),
('jane.smith@example.com', '$2b$12$DdOiqvLumbzkhVcsVthSLO.hE5NKEu9WrJpGEZtsLLko8GpEkIu4K', 'Jane', 'Smith', '555-0203', '456 Oak Ave, City, State', '1985-08-22', 'Aetna', 'AE789012', 'Bob Smith', '555-0204'),
('john.smith@email.com', '$2b$12$eYwk0/6aqzaQ74oduA/ekOx1H00vOeaFV.yfXNXNq5J4/PJ1wLREu', 'John', 'Smith', '555-0205', '789 Pine Rd, City, State', '1978-12-10', 'Cigna', 'CI345678', 'Sue Wilson', '555-0206'),
('mike.wilson@example.com', '$2b$12$DdOiqvLumbzkhVcsVthSLO.hE5NKEu9WrJpGEZtsLLko8GpEkIu4K', 'Mike', 'Wilson', '555-0207', '321 Elm St, City, State', '1982-03-18', 'UnitedHealth', 'UH567890', 'Lisa Wilson', '555-0208')
ON CONFLICT (email) DO NOTHING;

-- Insert sample appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_type, status, notes) VALUES
(1, 1, '2024-02-15 10:00:00', 'Check-up', 'scheduled', 'Annual physical examination'),
(1, 2, '2024-02-20 14:30:00', 'Consultation', 'scheduled', 'Follow-up on blood pressure'),
(2, 3, '2024-02-18 09:00:00', 'Vaccination', 'scheduled', 'Flu shot and routine vaccines'),
(3, 4, '2024-02-22 11:00:00', 'Surgery', 'scheduled', 'Knee replacement consultation')
ON CONFLICT DO NOTHING;

-- Insert sample medications
INSERT INTO medications (patient_id, prescriber_id, name, dosage, frequency, start_date, end_date, refills_remaining, instructions) VALUES
(1, 1, 'Lisinopril', '10mg', 'Once daily', '2024-01-01', NULL, 2, 'Take in the morning with food'),
(1, 2, 'Metformin', '500mg', 'Twice daily', '2024-01-15', NULL, 1, 'Take with meals'),
(2, 3, 'Ibuprofen', '400mg', 'As needed', '2024-02-01', '2024-02-15', 0, 'Take for pain relief'),
(3, 4, 'Tramadol', '50mg', 'Every 6 hours', '2024-01-20', NULL, 3, 'Take as prescribed for pain')
ON CONFLICT DO NOTHING;

-- Insert sample lab results
INSERT INTO lab_results (patient_id, ordering_doctor_id, test_name, test_date, result_value, reference_range, status, notes) VALUES
(1, 1, 'Blood Pressure', '2024-02-01', '120/80', '90-140/60-90', 'normal', 'Good blood pressure reading'),
(1, 2, 'Blood Glucose', '2024-02-01', '95', '70-100', 'normal', 'Fasting glucose level'),
(2, 3, 'Cholesterol Panel', '2024-02-05', 'Total: 180', 'Total: <200', 'normal', 'All values within normal range'),
(3, 4, 'X-Ray - Knee', '2024-02-10', 'Moderate arthritis', 'N/A', 'abnormal', 'Shows signs of osteoarthritis')
ON CONFLICT DO NOTHING;

-- Insert sample messages
INSERT INTO messages (sender_id, recipient_id, subject, content, is_read) VALUES
(1, 1, 'Appointment Reminder', 'This is a reminder for your appointment on February 15th at 10:00 AM. Please arrive 15 minutes early.', false),
(2, 1, 'Test Results Available', 'Your recent blood work results are now available in your patient portal. Please review them.', false),
(3, 2, 'Vaccination Schedule', 'Your child is due for their next round of vaccinations. Please schedule an appointment.', false),
(4, 3, 'Surgery Preparation', 'Please review the pre-surgery instructions I sent you. Call if you have any questions.', false)
ON CONFLICT DO NOTHING;

-- Insert sample surveys
INSERT INTO surveys (title, description, survey_type, is_active) VALUES
('Visit Experience Survey', 'Please share your experience with your recent visit', 'visit', true),
('AI Assistant Experience Survey', 'Please share your experience with our AI health assistant', 'ai_chat', true),
('General Patient Satisfaction Survey', 'Help us improve our services by providing feedback', 'general', true)
ON CONFLICT DO NOTHING;

-- Insert sample survey questions for visit survey
INSERT INTO survey_questions (survey_id, question_text, question_type, options, required, order_index) VALUES
(1, 'How would you rate your overall experience?', 'rating', NULL, true, 1),
(1, 'How satisfied were you with the doctor''s care?', 'rating', NULL, true, 2),
(1, 'How satisfied were you with the wait time?', 'rating', NULL, true, 3),
(1, 'How satisfied were you with the staff?', 'rating', NULL, true, 4),
(1, 'Would you recommend this doctor to others?', 'yes_no', NULL, true, 5),
(1, 'Please share any additional comments or suggestions:', 'text', NULL, false, 6)
ON CONFLICT DO NOTHING;

-- Insert sample survey questions for AI chat survey
INSERT INTO survey_questions (survey_id, question_text, question_type, options, required, order_index) VALUES
(2, 'How helpful was the AI assistant?', 'rating', NULL, true, 1),
(2, 'How satisfied were you with the response time?', 'rating', NULL, true, 2),
(2, 'How accurate were the AI assistant''s responses?', 'rating', NULL, true, 3),
(2, 'How easy was it to understand the AI assistant''s responses?', 'rating', NULL, true, 4),
(2, 'Did the AI assistant solve your problem?', 'yes_no', NULL, true, 5),
(2, 'Would you use the AI assistant again?', 'yes_no', NULL, true, 6),
(2, 'Please share any additional feedback:', 'text', NULL, false, 7)
ON CONFLICT DO NOTHING;

-- Insert sample survey questions for general survey
INSERT INTO survey_questions (survey_id, question_text, question_type, options, required, order_index) VALUES
(3, 'How satisfied are you with our patient portal?', 'rating', NULL, true, 1),
(3, 'How likely are you to recommend our services?', 'rating', NULL, true, 2),
(3, 'What is your preferred method of communication?', 'multiple_choice', '["Email", "Phone", "Text", "Portal"]', true, 3),
(3, 'How would you rate our appointment scheduling process?', 'rating', NULL, true, 4),
(3, 'Please share any suggestions for improvement:', 'text', NULL, false, 5)
ON CONFLICT DO NOTHING;

-- Insert sample survey responses
INSERT INTO survey_responses (survey_id, user_id, appointment_id, response_data, overall_rating, feedback_text) VALUES
(1, 1, 1, '{"1": 4, "2": 5, "3": 3, "4": 4, "5": true, "6": "Great experience overall!"}', 4.0, 'Great experience overall!'),
(2, 1, NULL, '{"1": 5, "2": 4, "3": 5, "4": 4, "5": true, "6": true, "7": "Very helpful AI assistant"}', 4.5, 'Very helpful AI assistant'),
(3, 2, NULL, '{"1": 4, "2": 4, "3": "Email", "4": 4, "5": "Keep up the good work!"}', 4.0, 'Keep up the good work!')
ON CONFLICT DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update the updated_at column
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_medications_updated_at BEFORE UPDATE ON medications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_surveys_updated_at BEFORE UPDATE ON surveys FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO healthcare_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO healthcare_user;

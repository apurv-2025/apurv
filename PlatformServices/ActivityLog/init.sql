-- init.sql
-- Create database if it doesn't exist
-- This file runs when PostgreSQL container starts for the first time

-- Create sample data
INSERT INTO users (id, email, hashed_password, full_name, is_active, created_at) 
VALUES 
    ('mock-user-id', 'user@example.com', 'hashed_password123', 'John Doe', true, NOW())
ON CONFLICT (id) DO NOTHING;

INSERT INTO clients (id, first_name, last_name, email, created_by, created_at)
VALUES 
    ('client-1', 'Jamie', 'D. Appleseed', 'jamie@example.com', 'mock-user-id', NOW())
ON CONFLICT (id) DO NOTHING;

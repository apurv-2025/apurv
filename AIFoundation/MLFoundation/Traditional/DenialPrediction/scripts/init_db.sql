-- Initialize healthcare denials database
-- This file is executed when the PostgreSQL container starts

-- Create the database if it doesn't exist
SELECT 'CREATE DATABASE healthcare_denials'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'healthcare_denials')\gexec

-- Connect to the database
\c healthcare_denials;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE healthcare_denials TO user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO user; 
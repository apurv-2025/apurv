# database/init.sql
-- Initialize database with proper settings
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for better performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_status_created_at 
ON tasks(status, created_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_due_date_status 
ON tasks(due_date, status) 
WHERE due_date IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_client_status 
ON tasks(client_id, status) 
WHERE client_id IS NOT NULL;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to auto-update updated_at columns
CREATE TRIGGER update_clients_updated_at 
    BEFORE UPDATE ON clients 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at 
    BEFORE UPDATE ON tasks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

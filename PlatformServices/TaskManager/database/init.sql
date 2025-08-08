# init.sql
-- Initialize the TaskManager database with proper schema and indexes

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    task_type VARCHAR(50) NOT NULL CHECK (task_type IN ('email', 'sms', 'webhook', 'reminder')),
    payload JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    callback_url VARCHAR(500),
    max_retries INTEGER DEFAULT 3 CHECK (max_retries >= 0),
    retry_count INTEGER DEFAULT 0 CHECK (retry_count >= 0),
    
    -- Constraints
    CONSTRAINT tasks_retry_count_valid CHECK (retry_count <= max_retries),
    CONSTRAINT tasks_name_not_empty CHECK (LENGTH(TRIM(name)) > 0)
);

-- Create task_executions table
CREATE TABLE IF NOT EXISTS task_executions (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('running', 'success', 'failed')),
    result JSONB,
    error_message TEXT,
    
    -- Constraints
    CONSTRAINT executions_completion_logic CHECK (
        (status = 'running' AND completed_at IS NULL) OR
        (status IN ('success', 'failed') AND completed_at IS NOT NULL)
    )
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_scheduled_time ON tasks(scheduled_time);
CREATE INDEX IF NOT EXISTS idx_tasks_task_type ON tasks(task_type);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_status_scheduled ON tasks(status, scheduled_time) WHERE status = 'pending';

CREATE INDEX IF NOT EXISTS idx_task_executions_task_id ON task_executions(task_id);
CREATE INDEX IF NOT EXISTS idx_task_executions_status ON task_executions(status);
CREATE INDEX IF NOT EXISTS idx_task_executions_started_at ON task_executions(started_at);

-- Create partial indexes for active tasks
CREATE INDEX IF NOT EXISTS idx_tasks_pending_scheduled ON tasks(scheduled_time) 
    WHERE status = 'pending';
CREATE INDEX IF NOT EXISTS idx_tasks_running ON tasks(id) 
    WHERE status = 'running';

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_tasks_type_status ON tasks(task_type, status);
CREATE INDEX IF NOT EXISTS idx_executions_task_status ON task_executions(task_id, status);

-- Create GIN index for JSONB payload searches
CREATE INDEX IF NOT EXISTS idx_tasks_payload_gin ON tasks USING GIN (payload);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to validate task payload based on type
CREATE OR REPLACE FUNCTION validate_task_payload()
RETURNS TRIGGER AS $$
BEGIN
    -- Validate email task payload
    IF NEW.task_type = 'email' THEN
        IF NOT (NEW.payload ? 'to_email' AND NEW.payload ? 'subject' AND NEW.payload ? 'body') THEN
            RAISE EXCEPTION 'Email task requires to_email, subject, and body fields in payload';
        END IF;
        IF NOT (NEW.payload->>'to_email' ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$') THEN
            RAISE EXCEPTION 'Invalid email address format';
        END IF;
    END IF;
    
    -- Validate SMS task payload
    IF NEW.task_type = 'sms' THEN
        IF NOT (NEW.payload ? 'phone_number' AND NEW.payload ? 'message') THEN
            RAISE EXCEPTION 'SMS task requires phone_number and message fields in payload';
        END IF;
        IF NOT (NEW.payload->>'phone_number' ~ '^\+?[1-9]\d{1,14}$') THEN
            RAISE EXCEPTION 'Invalid phone number format';
        END IF;
    END IF;
    
    -- Validate webhook task payload
    IF NEW.task_type = 'webhook' THEN
        IF NOT (NEW.payload ? 'url') THEN
            RAISE EXCEPTION 'Webhook task requires url field in payload';
        END IF;
        IF NOT (NEW.payload->>'url' ~ '^https?://') THEN
            RAISE EXCEPTION 'Webhook URL must start with http:// or https://';
        END IF;
    END IF;
    
    -- Validate reminder task payload
    IF NEW.task_type = 'reminder' THEN
        IF NOT (NEW.payload ? 'type' AND NEW.payload ? 'recipient' AND NEW.payload ? 'message') THEN
            RAISE EXCEPTION 'Reminder task requires type, recipient, and message fields in payload';
        END IF;
        IF NEW.payload->>'type' NOT IN ('email', 'sms') THEN
            RAISE EXCEPTION 'Reminder type must be either email or sms';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for payload validation
DROP TRIGGER IF EXISTS validate_task_payload_trigger ON tasks;
CREATE TRIGGER validate_task_payload_trigger
    BEFORE INSERT OR UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION validate_task_payload();

-- Function to get task statistics
CREATE OR REPLACE FUNCTION get_task_stats()
RETURNS TABLE (
    total_tasks INTEGER,
    pending_tasks INTEGER,
    running_tasks INTEGER,
    completed_tasks INTEGER,
    failed_tasks INTEGER,
    success_rate DECIMAL(5,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::INTEGER as total_tasks,
        COUNT(*) FILTER (WHERE status = 'pending')::INTEGER as pending_tasks,
        COUNT(*) FILTER (WHERE status = 'running')::INTEGER as running_tasks,
        COUNT(*) FILTER (WHERE status = 'completed')::INTEGER as completed_tasks,
        COUNT(*) FILTER (WHERE status = 'failed')::INTEGER as failed_tasks,
        CASE 
            WHEN COUNT(*) FILTER (WHERE status IN ('completed', 'failed')) > 0 
            THEN ROUND(
                (COUNT(*) FILTER (WHERE status = 'completed')::DECIMAL / 
                 COUNT(*) FILTER (WHERE status IN ('completed', 'failed'))::DECIMAL) * 100, 2
            )
            ELSE 0.00
        END as success_rate
    FROM tasks;
END;
$$ language 'plpgsql';

-- Function to clean up old completed tasks (optional)
CREATE OR REPLACE FUNCTION cleanup_old_tasks(days_old INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM tasks 
    WHERE status = 'completed' 
    AND created_at < CURRENT_TIMESTAMP - (days_old || ' days')::INTERVAL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ language 'plpgsql';

-- Create a view for task summary with execution info
CREATE OR REPLACE VIEW task_summary AS
SELECT 
    t.id,
    t.name,
    t.description,
    t.task_type,
    t.status,
    t.scheduled_time,
    t.created_at,
    t.updated_at,
    t.retry_count,
    t.max_retries,
    COUNT(te.id) as execution_count,
    MAX(te.started_at) as last_execution_time,
    CASE 
        WHEN t.status = 'completed' THEN te_last.result
        ELSE NULL 
    END as last_result,
    CASE 
        WHEN t.status = 'failed' THEN te_last.error_message
        ELSE NULL 
    END as last_error
FROM tasks t
LEFT JOIN task_executions te ON t.id = te.task_id
LEFT JOIN task_executions te_last ON t.id = te_last.task_id 
    AND te_last.started_at = (
        SELECT MAX(started_at) 
        FROM task_executions 
        WHERE task_id = t.id
    )
GROUP BY t.id, t.name, t.description, t.task_type, t.status, 
         t.scheduled_time, t.created_at, t.updated_at, 
         t.retry_count, t.max_retries, te_last.result, te_last.error_message;

-- Insert sample data for testing (optional)
INSERT INTO tasks (name, description, task_type, payload, scheduled_time) VALUES
(
    'Welcome Email',
    'Send welcome email to new patients',
    'email',
    '{"to_email": "patient@example.com", "subject": "Welcome to Our Practice", "body": "Thank you for choosing our medical practice."}',
    CURRENT_TIMESTAMP + INTERVAL '1 hour'
),
(
    'Appointment Reminder SMS',
    'Send SMS reminder for upcoming appointment',
    'sms',
    '{"phone_number": "+1234567890", "message": "Reminder: You have an appointment tomorrow at 2:00 PM."}',
    CURRENT_TIMESTAMP + INTERVAL '24 hours'
),
(
    'Lab Results Notification',
    'Notify external system about lab results',
    'webhook',
    '{"url": "https://api.example.com/lab-results", "method": "POST", "data": {"patient_id": "12345", "results": "available"}}',
    CURRENT_TIMESTAMP + INTERVAL '2 hours'
);

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO taskuser;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO taskuser;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO taskuser;

-- Create health check function
CREATE OR REPLACE FUNCTION health_check()
RETURNS TABLE (
    status TEXT,
    timestamp TIMESTAMP WITH TIME ZONE,
    tasks_count INTEGER,
    pending_count INTEGER,
    database_size TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'healthy'::TEXT as status,
        CURRENT_TIMESTAMP as timestamp,
        COUNT(*)::INTEGER as tasks_count,
        COUNT(*) FILTER (WHERE tasks.status = 'pending')::INTEGER as pending_count,
        pg_size_pretty(pg_database_size(current_database())) as database_size
    FROM tasks;
END;
$$ language 'plpgsql';

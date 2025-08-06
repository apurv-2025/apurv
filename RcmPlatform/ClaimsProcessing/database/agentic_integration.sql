-- Agentic Core Integration Tables for ClaimsProcessing Database
-- This file adds the necessary tables for Agentic Core functionality

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Agentic Core Tables

-- Conversations table for storing chat conversations
CREATE TABLE IF NOT EXISTS agentic_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) NOT NULL,
    title VARCHAR(255),
    model VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    conversation_id VARCHAR(100) UNIQUE
);

-- Messages table for storing conversation messages
CREATE TABLE IF NOT EXISTS agentic_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES agentic_conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Tasks table for storing AI agent tasks
CREATE TABLE IF NOT EXISTS agentic_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    data JSONB,
    result JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT
);

-- Tools table for storing available AI tools
CREATE TABLE IF NOT EXISTS agentic_tools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0.0',
    config JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tool executions table for tracking tool usage
CREATE TABLE IF NOT EXISTS agentic_tool_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES agentic_tasks(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES agentic_tools(id) ON DELETE CASCADE,
    input_data JSONB,
    output_data JSONB,
    execution_time_ms INTEGER,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'success', 'failed')),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Users table for Agentic Core (extends existing users if needed)
CREATE TABLE IF NOT EXISTS agentic_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    preferences JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Model configurations table
CREATE TABLE IF NOT EXISTS agentic_model_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    config JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- API keys table for authentication
CREATE TABLE IF NOT EXISTS agentic_api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES agentic_users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    permissions JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table for user sessions
CREATE TABLE IF NOT EXISTS agentic_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES agentic_users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Metrics table for performance tracking
CREATE TABLE IF NOT EXISTS agentic_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10, 4) NOT NULL,
    metric_unit VARCHAR(20),
    tags JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs table for tracking actions
CREATE TABLE IF NOT EXISTS agentic_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES agentic_users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_agentic_conversations_user_id ON agentic_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_agentic_conversations_created_at ON agentic_conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_agentic_messages_conversation_id ON agentic_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_agentic_messages_timestamp ON agentic_messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_agentic_tasks_user_id ON agentic_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_agentic_tasks_status ON agentic_tasks(status);
CREATE INDEX IF NOT EXISTS idx_agentic_tasks_created_at ON agentic_tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_agentic_tool_executions_task_id ON agentic_tool_executions(task_id);
CREATE INDEX IF NOT EXISTS idx_agentic_tool_executions_tool_id ON agentic_tool_executions(tool_id);
CREATE INDEX IF NOT EXISTS idx_agentic_metrics_timestamp ON agentic_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_agentic_metrics_name ON agentic_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_agentic_audit_logs_user_id ON agentic_audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_agentic_audit_logs_created_at ON agentic_audit_logs(created_at);

-- Functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_agentic_conversations_updated_at 
    BEFORE UPDATE ON agentic_conversations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agentic_tools_updated_at 
    BEFORE UPDATE ON agentic_tools 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agentic_users_updated_at 
    BEFORE UPDATE ON agentic_users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agentic_model_configs_updated_at 
    BEFORE UPDATE ON agentic_model_configs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default data
INSERT INTO agentic_tools (name, description, version, config) VALUES
('search', 'Search for information on the web', '1.0.0', '{"enabled": true}'),
('calculator', 'Perform mathematical calculations', '1.0.0', '{"enabled": true}'),
('datetime', 'Get current date and time information', '1.0.0', '{"enabled": true}'),
('weather', 'Get weather information for a location', '1.0.0', '{"enabled": true}'),
('file_read', 'Read content from files', '1.0.0', '{"enabled": false}'),
('analyze_claim', 'Analyze a claim for issues and provide recommendations', '1.0.0', '{"enabled": true}'),
('analyze_rejection', 'Analyze a claim rejection and suggest fixes', '1.0.0', '{"enabled": true}'),
('generate_report', 'Generate various types of claims reports', '1.0.0', '{"enabled": true}'),
('search_claims', 'Search claims with various criteria', '1.0.0', '{"enabled": true}')
ON CONFLICT (name) DO NOTHING;

INSERT INTO agentic_model_configs (name, provider, model_id, config) VALUES
('GPT-4', 'openai', 'gpt-4', '{"max_tokens": 8192, "temperature": 0.7}'),
('GPT-3.5 Turbo', 'openai', 'gpt-3.5-turbo', '{"max_tokens": 4096, "temperature": 0.7}'),
('Claude 3 Sonnet', 'anthropic', 'claude-3-sonnet', '{"max_tokens": 200000, "temperature": 0.7}'),
('Claude 3 Haiku', 'anthropic', 'claude-3-haiku', '{"max_tokens": 200000, "temperature": 0.7}')
ON CONFLICT DO NOTHING;

-- Views for easier querying
CREATE OR REPLACE VIEW agentic_conversation_summary AS
SELECT 
    c.id,
    c.user_id,
    c.title,
    c.model,
    c.created_at,
    c.updated_at,
    COUNT(m.id) as message_count,
    MAX(m.timestamp) as last_message_at
FROM agentic_conversations c
LEFT JOIN agentic_messages m ON c.id = m.conversation_id
GROUP BY c.id, c.user_id, c.title, c.model, c.created_at, c.updated_at;

CREATE OR REPLACE VIEW agentic_task_summary AS
SELECT 
    t.id,
    t.user_id,
    t.task_type,
    t.status,
    t.created_at,
    t.completed_at,
    COUNT(te.id) as tool_executions,
    AVG(te.execution_time_ms) as avg_execution_time
FROM agentic_tasks t
LEFT JOIN agentic_tool_executions te ON t.id = te.task_id
GROUP BY t.id, t.user_id, t.task_type, t.status, t.created_at, t.completed_at;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user; 
-- schema.sql
-- PostgreSQL schema for notification system

-- Enable UUID extension if you want to use UUIDs (optional)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (you might already have this)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes on users table
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Notifications table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL DEFAULT 'info' CHECK (type IN ('success', 'warning', 'error', 'info')),
    category VARCHAR(50) NOT NULL DEFAULT 'system' CHECK (category IN ('billing', 'team', 'system', 'security')),
    read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_notifications_user_read ON notifications(user_id, read);
CREATE INDEX idx_notifications_user_category ON notifications(user_id, category);
CREATE INDEX idx_notifications_user_created ON notifications(user_id, created_at DESC);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_category ON notifications(category);
CREATE INDEX idx_notifications_read ON notifications(read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);

-- Full-text search index for title and message
CREATE INDEX idx_notifications_search ON notifications USING gin(to_tsvector('english', title || ' ' || message));

-- Notification preferences table
CREATE TABLE notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    email BOOLEAN NOT NULL DEFAULT TRUE,
    push BOOLEAN NOT NULL DEFAULT TRUE,
    sms BOOLEAN NOT NULL DEFAULT FALSE,
    weekly_digest BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on user_id for preferences
CREATE INDEX idx_notification_preferences_user_id ON notification_preferences(user_id);

-- Notification templates table (optional, for system templates)
CREATE TABLE notification_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    title_template VARCHAR(255) NOT NULL,
    message_template TEXT NOT NULL,
    type VARCHAR(50) NOT NULL DEFAULT 'info' CHECK (type IN ('success', 'warning', 'error', 'info')),
    category VARCHAR(50) NOT NULL DEFAULT 'system' CHECK (category IN ('billing', 'team', 'system', 'security')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes on templates
CREATE INDEX idx_notification_templates_name ON notification_templates(name);
CREATE INDEX idx_notification_templates_active ON notification_templates(is_active);
CREATE INDEX idx_notification_templates_type ON notification_templates(type);
CREATE INDEX idx_notification_templates_category ON notification_templates(category);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to automatically update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notifications_updated_at BEFORE UPDATE ON notifications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notification_preferences_updated_at BEFORE UPDATE ON notification_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notification_templates_updated_at BEFORE UPDATE ON notification_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert some sample data (optional)
-- Insert a test user
INSERT INTO users (email, username) VALUES 
('test@example.com', 'testuser')
ON CONFLICT (email) DO NOTHING;

-- Insert default preferences for the test user
INSERT INTO notification_preferences (user_id, email, push, sms, weekly_digest)
SELECT id, TRUE, TRUE, FALSE, TRUE 
FROM users 
WHERE email = 'test@example.com'
ON CONFLICT (user_id) DO NOTHING;

-- Insert some sample notifications
INSERT INTO notifications (user_id, title, message, type, category, read) 
SELECT 
    u.id,
    'Payment Successful',
    'Your subscription has been renewed for $29.99',
    'success',
    'billing',
    FALSE
FROM users u 
WHERE u.email = 'test@example.com'
ON CONFLICT DO NOTHING;

INSERT INTO notifications (user_id, title, message, type, category, read) 
SELECT 
    u.id,
    'New Team Member',
    'John Doe has joined your workspace',
    'info',
    'team',
    FALSE
FROM users u 
WHERE u.email = 'test@example.com';

INSERT INTO notifications (user_id, title, message, type, category, read) 
SELECT 
    u.id,
    'Storage Limit Warning',
    'You''re using 85% of your storage space',
    'warning',
    'system',
    TRUE
FROM users u 
WHERE u.email = 'test@example.com';

INSERT INTO notifications (user_id, title, message, type, category, read) 
SELECT 
    u.id,
    'Security Alert',
    'New login from unknown device detected',
    'error',
    'security',
    FALSE
FROM users u 
WHERE u.email = 'test@example.com';

-- Insert some notification templates
INSERT INTO notification_templates (name, title_template, message_template, type, category) VALUES
('welcome', 'Welcome to {app_name}!', 'Thank you for joining {app_name}. We''re excited to have you on board!', 'info', 'system'),
('payment_success', 'Payment Successful', 'Your payment of ${amount} has been processed successfully.', 'success', 'billing'),
('payment_failed', 'Payment Failed', 'We couldn''t process your payment of ${amount}. Please update your payment method.', 'error', 'billing'),
('storage_warning', 'Storage Limit Warning', 'You''re using {percentage}% of your storage space. Consider upgrading your plan.', 'warning', 'system'),
('new_team_member', 'New Team Member', '{member_name} has joined your workspace.', 'info', 'team'),
('security_login', 'New Login Detected', 'A new login was detected from {location} on {device}.', 'warning', 'security')
ON CONFLICT (name) DO NOTHING;

-- Performance optimization: Analyze tables
ANALYZE users;
ANALYZE notifications;
ANALYZE notification_preferences;
ANALYZE notification_templates;

-- Optional: Create a view for notification statistics
CREATE OR REPLACE VIEW notification_stats AS
SELECT 
    u.id as user_id,
    u.email,
    COUNT(n.id) as total_notifications,
    COUNT(CASE WHEN n.read = FALSE THEN 1 END) as unread_count,
    COUNT(CASE WHEN n.type = 'success' THEN 1 END) as success_count,
    COUNT(CASE WHEN n.type = 'warning' THEN 1 END) as warning_count,
    COUNT(CASE WHEN n.type = 'error' THEN 1 END) as error_count,
    COUNT(CASE WHEN n.type = 'info' THEN 1 END) as info_count,
    COUNT(CASE WHEN n.category = 'billing' THEN 1 END) as billing_count,
    COUNT(CASE WHEN n.category = 'team' THEN 1 END) as team_count,
    COUNT(CASE WHEN n.category = 'system' THEN 1 END) as system_count,
    COUNT(CASE WHEN n.category = 'security' THEN 1 END) as security_count,
    MAX(n.created_at) as last_notification_at
FROM users u
LEFT JOIN notifications n ON u.id = n.user_id
GROUP BY u.id, u.email;
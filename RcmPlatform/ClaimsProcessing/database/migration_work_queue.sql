-- Migration script to add work queue functionality
-- Run this script to update existing database schema

-- Add work queue columns to claims table
ALTER TABLE claims 
ADD COLUMN IF NOT EXISTS work_queue_status VARCHAR(20) DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS work_queue_priority VARCHAR(20) DEFAULT 'medium',
ADD COLUMN IF NOT EXISTS assigned_to VARCHAR(100),
ADD COLUMN IF NOT EXISTS assigned_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS estimated_completion TIMESTAMP,
ADD COLUMN IF NOT EXISTS work_notes TEXT;

-- Create work queue status enum type if it doesn't exist
DO $$ BEGIN
    CREATE TYPE workqueuestatus AS ENUM ('pending', 'assigned', 'in_progress', 'completed', 'failed', 'cancelled');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create work queue priority enum type if it doesn't exist
DO $$ BEGIN
    CREATE TYPE workqueuepriority AS ENUM ('low', 'medium', 'high', 'urgent');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create work_queue table if it doesn't exist
CREATE TABLE IF NOT EXISTS work_queue (
    id SERIAL PRIMARY KEY,
    claim_id INTEGER NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    assigned_by VARCHAR(100) NOT NULL,
    assigned_to VARCHAR(100) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status workqueuestatus DEFAULT 'pending',
    priority workqueuepriority DEFAULT 'medium',
    estimated_completion TIMESTAMP,
    actual_completion TIMESTAMP,
    work_notes TEXT,
    action_taken TEXT,
    result_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_work_queue_claim_id ON work_queue(claim_id);
CREATE INDEX IF NOT EXISTS idx_work_queue_status ON work_queue(status);
CREATE INDEX IF NOT EXISTS idx_work_queue_priority ON work_queue(priority);
CREATE INDEX IF NOT EXISTS idx_work_queue_assigned_to ON work_queue(assigned_to);
CREATE INDEX IF NOT EXISTS idx_work_queue_created_at ON work_queue(created_at);

-- Add indexes to claims table for work queue fields
CREATE INDEX IF NOT EXISTS idx_claims_work_queue_status ON claims(work_queue_status);
CREATE INDEX IF NOT EXISTS idx_claims_work_queue_priority ON claims(work_queue_priority);
CREATE INDEX IF NOT EXISTS idx_claims_assigned_to ON claims(assigned_to);

-- Update existing claims to have default work queue status
UPDATE claims SET work_queue_status = 'pending' WHERE work_queue_status IS NULL;
UPDATE claims SET work_queue_priority = 'medium' WHERE work_queue_priority IS NULL; 
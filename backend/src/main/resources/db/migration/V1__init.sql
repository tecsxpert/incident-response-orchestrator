-- Enable UUID support
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create main table
CREATE TABLE incident (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    
    status VARCHAR(50) NOT NULL,
    priority VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,

    created_by VARCHAR(100),
    assigned_to VARCHAR(100),

    is_deleted BOOLEAN DEFAULT FALSE
);

-- Indexes (important for performance)
CREATE INDEX idx_incident_status ON incident(status);
CREATE INDEX idx_incident_created_at ON incident(created_at);
CREATE INDEX idx_incident_assigned_to ON incident(assigned_to);
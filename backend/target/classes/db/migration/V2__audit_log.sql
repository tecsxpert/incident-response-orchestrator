CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,

    action VARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE

    old_value TEXT,
    new_value TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100)
);

-- Composite index (important)
CREATE INDEX idx_audit_entity
ON audit_log (entity_type, entity_id);

-- Additional indexes
CREATE INDEX idx_audit_created_at
ON audit_log (created_at);

CREATE INDEX idx_audit_created_by
ON audit_log (created_by);
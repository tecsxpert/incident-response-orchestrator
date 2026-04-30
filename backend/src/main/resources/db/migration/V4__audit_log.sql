CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    action VARCHAR(100),
    username VARCHAR(50),
    timestamp TIMESTAMP
);

ALTER TABLE audit_log
ADD COLUMN old_data TEXT,
ADD COLUMN new_data TEXT;
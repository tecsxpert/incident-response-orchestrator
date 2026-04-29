CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    action VARCHAR(100),
    username VARCHAR(50),
    timestamp TIMESTAMP
);
-- MediSense-AI Demo Database Seed Data
-- PostgreSQL initialization script

-- Create tables (will be created by SQLAlchemy, but included for reference)

-- Insert demo users
INSERT INTO users (email, hashed_password, full_name, role, is_active, is_verified, phone_number, created_at) VALUES
('admin@medisense.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYVxpJ8xu5u', 'Admin User', 'admin', true, true, '+1234567890', NOW()),
('dr.smith@medisense.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYVxpJ8xu5u', 'Dr. John Smith', 'clinician', true, true, '+1234567891', NOW()),
('patient@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYVxpJ8xu5u', 'Jane Doe', 'patient', true, true, '+1234567892', NOW());

-- Note: All passwords are hashed "password123" for demo purposes
-- In production, use secure password hashing

-- Insert demo appointments
INSERT INTO appointments (patient_id, clinician_id, appointment_type, status, scheduled_start, scheduled_end, chief_complaint, created_at) VALUES
(3, 2, 'consultation', 'scheduled', NOW() + INTERVAL '1 day', NOW() + INTERVAL '1 day 30 minutes', 'Annual checkup', NOW()),
(3, 2, 'follow_up', 'confirmed', NOW() + INTERVAL '7 days', NOW() + INTERVAL '7 days 30 minutes', 'Follow-up on test results', NOW());

-- Insert demo audit logs
INSERT INTO audit_logs (event_type, event_id, user_id, session_id, agent_name, action, success, timestamp) VALUES
('agent_action', 'evt_demo_001', 3, 'session_demo_001', 'routing_agent', 'classify_intent', 'true', NOW()),
('agent_action', 'evt_demo_002', 3, 'session_demo_001', 'rag_agent', 'search_documents', 'true', NOW()),
('llm_call', 'evt_demo_003', 3, 'session_demo_001', 'prescription_agent', 'generate', 'true', NOW());

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_clinician ON appointments(clinician_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_session ON audit_logs(session_id);

-- Insert sample clinical data (simplified)
-- Note: In production, this would include comprehensive EHR data

COMMENT ON TABLE users IS 'User accounts for patients, clinicians, and administrators';
COMMENT ON TABLE appointments IS 'Appointment scheduling and management';
COMMENT ON TABLE audit_logs IS 'Immutable audit trail for compliance and traceability';

-- MediSense-AI Database Initialization Script
-- Run this script to create schema and load all sample data
-- Usage: psql -U medisense -d medisense_db -f 000_init.sql

-- =====================================================
-- INITIALIZATION
-- =====================================================

\echo '=========================================='
\echo 'MediSense-AI Database Initialization'
\echo '=========================================='
\echo ''

-- Drop existing tables if any (for fresh start)
\echo 'Dropping existing tables...'
DROP TABLE IF EXISTS chat_messages CASCADE;
DROP TABLE IF EXISTS chat_sessions CASCADE;
DROP TABLE IF EXISTS vector_documents CASCADE;
DROP TABLE IF EXISTS guardrail_violations CASCADE;
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS image_analyses CASCADE;
DROP TABLE IF EXISTS medical_documents CASCADE;
DROP TABLE IF EXISTS prescription_items CASCADE;
DROP TABLE IF EXISTS prescriptions CASCADE;
DROP TABLE IF EXISTS drug_interactions CASCADE;
DROP TABLE IF EXISTS medications CASCADE;
DROP TABLE IF EXISTS appointments CASCADE;
DROP TABLE IF EXISTS clinician_availability CASCADE;
DROP TABLE IF EXISTS patient_profiles CASCADE;
DROP TABLE IF EXISTS clinician_profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop existing types
DROP TYPE IF EXISTS analysis_status CASCADE;
DROP TYPE IF EXISTS notification_status CASCADE;
DROP TYPE IF EXISTS notification_type CASCADE;
DROP TYPE IF EXISTS audit_event_type CASCADE;
DROP TYPE IF EXISTS document_type CASCADE;
DROP TYPE IF EXISTS prescription_status CASCADE;
DROP TYPE IF EXISTS payment_status CASCADE;
DROP TYPE IF EXISTS appointment_type CASCADE;
DROP TYPE IF EXISTS appointment_status CASCADE;
DROP TYPE IF EXISTS user_status CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;

\echo 'Existing tables dropped.'
\echo ''

-- =====================================================
-- LOAD SCHEMA
-- =====================================================
\echo 'Creating database schema...'
\i 001_schema.sql
\echo 'Schema created successfully.'
\echo ''

-- =====================================================
-- LOAD SAMPLE DATA
-- =====================================================
\echo 'Loading users data...'
\i 002_users_data.sql
\echo 'Users data loaded.'
\echo ''

\echo 'Loading appointments data...'
\i 003_appointments_data.sql
\echo 'Appointments data loaded.'
\echo ''

\echo 'Loading medications and prescriptions...'
\i 004_medications_prescriptions.sql
\echo 'Medications and prescriptions loaded.'
\echo ''

\echo 'Loading documents, images, and payments...'
\i 005_documents_images_payments.sql
\echo 'Documents, images, and payments loaded.'
\echo ''

\echo 'Loading audit logs and chat data...'
\i 006_audit_chat_data.sql
\echo 'Audit logs and chat data loaded.'
\echo ''

-- =====================================================
-- VERIFICATION
-- =====================================================
\echo '=========================================='
\echo 'Data Load Verification'
\echo '=========================================='

SELECT 'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL SELECT 'clinician_profiles', COUNT(*) FROM clinician_profiles
UNION ALL SELECT 'patient_profiles', COUNT(*) FROM patient_profiles
UNION ALL SELECT 'clinician_availability', COUNT(*) FROM clinician_availability
UNION ALL SELECT 'appointments', COUNT(*) FROM appointments
UNION ALL SELECT 'medications', COUNT(*) FROM medications
UNION ALL SELECT 'prescriptions', COUNT(*) FROM prescriptions
UNION ALL SELECT 'prescription_items', COUNT(*) FROM prescription_items
UNION ALL SELECT 'drug_interactions', COUNT(*) FROM drug_interactions
UNION ALL SELECT 'medical_documents', COUNT(*) FROM medical_documents
UNION ALL SELECT 'image_analyses', COUNT(*) FROM image_analyses
UNION ALL SELECT 'payments', COUNT(*) FROM payments
UNION ALL SELECT 'notifications', COUNT(*) FROM notifications
UNION ALL SELECT 'audit_logs', COUNT(*) FROM audit_logs
UNION ALL SELECT 'guardrail_violations', COUNT(*) FROM guardrail_violations
UNION ALL SELECT 'chat_sessions', COUNT(*) FROM chat_sessions
UNION ALL SELECT 'chat_messages', COUNT(*) FROM chat_messages
UNION ALL SELECT 'vector_documents', COUNT(*) FROM vector_documents
ORDER BY table_name;

\echo ''
\echo '=========================================='
\echo 'Database initialization complete!'
\echo '=========================================='

-- MediSense-AI Database Schema
-- Complete schema with all tables and relationships

-- =====================================================
-- EXTENSIONS
-- =====================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- ENUM TYPES
-- =====================================================

-- User roles
CREATE TYPE user_role AS ENUM ('patient', 'clinician', 'admin', 'nurse', 'pharmacist');

-- User status
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended', 'pending_verification');

-- Appointment status
CREATE TYPE appointment_status AS ENUM ('scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show');

-- Appointment type
CREATE TYPE appointment_type AS ENUM ('consultation', 'follow_up', 'emergency', 'routine_checkup', 'telemedicine');

-- Payment status
CREATE TYPE payment_status AS ENUM ('pending', 'authorized', 'captured', 'refunded', 'failed', 'cancelled');

-- Prescription status
CREATE TYPE prescription_status AS ENUM ('draft', 'pending_approval', 'approved', 'dispensed', 'cancelled', 'expired');

-- Document type
CREATE TYPE document_type AS ENUM ('lab_report', 'imaging', 'prescription', 'discharge_summary', 'medical_history', 'insurance', 'consent_form');

-- Notification type
CREATE TYPE notification_type AS ENUM ('email', 'sms', 'push', 'in_app');

-- Notification status
CREATE TYPE notification_status AS ENUM ('pending', 'sent', 'delivered', 'failed', 'read');

-- Audit event type
CREATE TYPE audit_event_type AS ENUM ('login', 'logout', 'query', 'agent_action', 'data_access', 'data_modify', 'phi_access', 'error');

-- Image analysis status
CREATE TYPE analysis_status AS ENUM ('pending', 'processing', 'completed', 'failed', 'review_required');

-- =====================================================
-- CORE TABLES
-- =====================================================

-- 1. USERS TABLE (Central user management)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(20),
    role user_role NOT NULL DEFAULT 'patient',
    status user_status NOT NULL DEFAULT 'active',
    profile_image_url VARCHAR(500),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'USA',
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE,
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE
);

-- 2. CLINICIAN PROFILES (Extended info for medical staff)
CREATE TABLE clinician_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    license_number VARCHAR(100) UNIQUE NOT NULL,
    license_state VARCHAR(50),
    license_expiry DATE,
    specialty VARCHAR(100) NOT NULL,
    sub_specialty VARCHAR(100),
    department VARCHAR(100),
    years_of_experience INTEGER,
    education TEXT,
    certifications TEXT[],
    consultation_fee DECIMAL(10, 2),
    telemedicine_enabled BOOLEAN DEFAULT TRUE,
    average_rating DECIMAL(3, 2) DEFAULT 0.00,
    total_reviews INTEGER DEFAULT 0,
    bio TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. PATIENT PROFILES (Extended patient info)
CREATE TABLE patient_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    blood_type VARCHAR(10),
    height_cm DECIMAL(5, 2),
    weight_kg DECIMAL(5, 2),
    allergies TEXT[],
    chronic_conditions TEXT[],
    current_medications TEXT[],
    family_history TEXT,
    insurance_provider VARCHAR(255),
    insurance_policy_number VARCHAR(100),
    insurance_group_number VARCHAR(100),
    primary_care_physician_id INTEGER REFERENCES users(id),
    preferred_pharmacy VARCHAR(255),
    preferred_language VARCHAR(50) DEFAULT 'English',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. CLINICIAN AVAILABILITY (Scheduling slots)
CREATE TABLE clinician_availability (
    id SERIAL PRIMARY KEY,
    clinician_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Sunday
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    slot_duration_minutes INTEGER DEFAULT 30,
    is_available BOOLEAN DEFAULT TRUE,
    location VARCHAR(255),
    telemedicine_only BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_time_range CHECK (start_time < end_time)
);

-- 5. APPOINTMENTS
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES users(id),
    clinician_id INTEGER NOT NULL REFERENCES users(id),
    scheduled_start TIMESTAMP WITH TIME ZONE NOT NULL,
    scheduled_end TIMESTAMP WITH TIME ZONE NOT NULL,
    actual_start TIMESTAMP WITH TIME ZONE,
    actual_end TIMESTAMP WITH TIME ZONE,
    appointment_type appointment_type NOT NULL DEFAULT 'consultation',
    status appointment_status NOT NULL DEFAULT 'scheduled',
    chief_complaint TEXT,
    notes TEXT,
    diagnosis TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    is_telemedicine BOOLEAN DEFAULT FALSE,
    telemedicine_link VARCHAR(500),
    location VARCHAR(255),
    cancellation_reason TEXT,
    cancelled_by INTEGER REFERENCES users(id),
    cancelled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_appointment_time CHECK (scheduled_start < scheduled_end)
);

-- 6. MEDICATIONS (Drug catalog)
CREATE TABLE medications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    generic_name VARCHAR(255),
    brand_names TEXT[],
    drug_class VARCHAR(100),
    dosage_forms TEXT[],
    strengths TEXT[],
    route_of_administration VARCHAR(100),
    description TEXT,
    warnings TEXT,
    contraindications TEXT[],
    side_effects TEXT[],
    interactions TEXT[],
    pregnancy_category VARCHAR(10),
    controlled_substance_schedule VARCHAR(20),
    requires_prescription BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. PRESCRIPTIONS
CREATE TABLE prescriptions (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES users(id),
    prescriber_id INTEGER NOT NULL REFERENCES users(id),
    appointment_id INTEGER REFERENCES appointments(id),
    status prescription_status NOT NULL DEFAULT 'draft',
    diagnosis TEXT,
    notes TEXT,
    pharmacy_name VARCHAR(255),
    pharmacy_address VARCHAR(500),
    pharmacy_phone VARCHAR(20),
    valid_from DATE NOT NULL DEFAULT CURRENT_DATE,
    valid_until DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP WITH TIME ZONE,
    approved_by INTEGER REFERENCES users(id),
    dispensed_at TIMESTAMP WITH TIME ZONE
);

-- 8. PRESCRIPTION ITEMS (Individual medications in prescription)
CREATE TABLE prescription_items (
    id SERIAL PRIMARY KEY,
    prescription_id INTEGER NOT NULL REFERENCES prescriptions(id) ON DELETE CASCADE,
    medication_id INTEGER NOT NULL REFERENCES medications(id),
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100),
    quantity INTEGER,
    refills_allowed INTEGER DEFAULT 0,
    refills_remaining INTEGER DEFAULT 0,
    instructions TEXT,
    take_with_food BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. MEDICAL DOCUMENTS
CREATE TABLE medical_documents (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES users(id),
    uploaded_by INTEGER NOT NULL REFERENCES users(id),
    appointment_id INTEGER REFERENCES appointments(id),
    document_type document_type NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    ocr_text TEXT,
    extracted_data JSONB,
    is_confidential BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. IMAGE ANALYSES (For symptom image analysis)
CREATE TABLE image_analyses (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES users(id),
    uploaded_by INTEGER NOT NULL REFERENCES users(id),
    appointment_id INTEGER REFERENCES appointments(id),
    image_path VARCHAR(500) NOT NULL,
    image_name VARCHAR(255) NOT NULL,
    body_part VARCHAR(100),
    symptom_description TEXT,
    status analysis_status NOT NULL DEFAULT 'pending',
    ai_predictions JSONB,
    ai_confidence DECIMAL(5, 4),
    ai_model_version VARCHAR(50),
    clinician_review TEXT,
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    final_diagnosis TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. PAYMENTS
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES users(id),
    appointment_id INTEGER REFERENCES appointments(id),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status payment_status NOT NULL DEFAULT 'pending',
    payment_method VARCHAR(50),
    transaction_id VARCHAR(255),
    gateway_response JSONB,
    description TEXT,
    invoice_number VARCHAR(100),
    billing_address TEXT,
    insurance_claim_id VARCHAR(100),
    insurance_amount DECIMAL(10, 2) DEFAULT 0,
    patient_responsibility DECIMAL(10, 2),
    refund_amount DECIMAL(10, 2) DEFAULT 0,
    refund_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP WITH TIME ZONE
);

-- 12. NOTIFICATIONS
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id),
    type notification_type NOT NULL,
    status notification_status NOT NULL DEFAULT 'pending',
    subject VARCHAR(255),
    message TEXT NOT NULL,
    template_id VARCHAR(100),
    template_data JSONB,
    recipient_address VARCHAR(255),
    sent_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    read_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 13. AUDIT LOGS
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(255),
    event_type audit_event_type NOT NULL,
    agent_name VARCHAR(100),
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    input_data JSONB,
    output_data JSONB,
    ip_address INET,
    user_agent TEXT,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    execution_time_ms INTEGER,
    provenance JSONB,
    phi_accessed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 14. GUARDRAIL VIOLATIONS
CREATE TABLE guardrail_violations (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    audit_log_id INTEGER REFERENCES audit_logs(id),
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(255),
    agent_name VARCHAR(100),
    violation_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    original_content TEXT,
    redacted_content TEXT,
    patterns_matched TEXT[],
    action_taken VARCHAR(100),
    blocked BOOLEAN DEFAULT FALSE,
    reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 15. CHAT SESSIONS
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,
    total_messages INTEGER DEFAULT 0,
    agents_used TEXT[],
    summary TEXT,
    satisfaction_rating INTEGER CHECK (satisfaction_rating BETWEEN 1 AND 5),
    feedback TEXT
);

-- 16. CHAT MESSAGES
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    agent_name VARCHAR(100),
    confidence DECIMAL(5, 4),
    tokens_used INTEGER,
    response_time_ms INTEGER,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 17. VECTOR DOCUMENTS (For RAG)
CREATE TABLE vector_documents (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    source_id INTEGER,
    title VARCHAR(255),
    content TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    embedding_id VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 18. DRUG INTERACTIONS
CREATE TABLE drug_interactions (
    id SERIAL PRIMARY KEY,
    medication_1_id INTEGER NOT NULL REFERENCES medications(id),
    medication_2_id INTEGER NOT NULL REFERENCES medications(id),
    severity VARCHAR(20) NOT NULL, -- 'minor', 'moderate', 'major', 'contraindicated'
    description TEXT NOT NULL,
    clinical_effects TEXT,
    management TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_interaction UNIQUE (medication_1_id, medication_2_id),
    CONSTRAINT different_medications CHECK (medication_1_id != medication_2_id)
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);

CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_clinician ON appointments(clinician_id);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_scheduled ON appointments(scheduled_start);

CREATE INDEX idx_prescriptions_patient ON prescriptions(patient_id);
CREATE INDEX idx_prescriptions_status ON prescriptions(status);

CREATE INDEX idx_medical_documents_patient ON medical_documents(patient_id);
CREATE INDEX idx_medical_documents_type ON medical_documents(document_type);

CREATE INDEX idx_image_analyses_patient ON image_analyses(patient_id);
CREATE INDEX idx_image_analyses_status ON image_analyses(status);

CREATE INDEX idx_payments_patient ON payments(patient_id);
CREATE INDEX idx_payments_status ON payments(status);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_status ON notifications(status);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_event ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

CREATE INDEX idx_guardrail_violations_user ON guardrail_violations(user_id);
CREATE INDEX idx_guardrail_violations_type ON guardrail_violations(violation_type);

CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);

-- =====================================================
-- TRIGGERS FOR UPDATED_AT
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_prescriptions_updated_at BEFORE UPDATE ON prescriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_medical_documents_updated_at BEFORE UPDATE ON medical_documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_image_analyses_updated_at BEFORE UPDATE ON image_analyses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE users IS 'Central user table for patients, clinicians, and staff';
COMMENT ON TABLE clinician_profiles IS 'Extended profile information for medical professionals';
COMMENT ON TABLE patient_profiles IS 'Extended health information for patients';
COMMENT ON TABLE appointments IS 'Medical appointments between patients and clinicians';
COMMENT ON TABLE prescriptions IS 'E-prescriptions with medication details';
COMMENT ON TABLE medical_documents IS 'Uploaded medical documents and reports';
COMMENT ON TABLE image_analyses IS 'AI-powered symptom image analysis results';
COMMENT ON TABLE payments IS 'Payment transactions and billing';
COMMENT ON TABLE audit_logs IS 'Comprehensive audit trail for compliance';
COMMENT ON TABLE guardrail_violations IS 'PHI/PII violations and safety incidents';

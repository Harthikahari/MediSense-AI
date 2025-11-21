-- MediSense-AI Sample Data - Users
-- Contains: Users, Clinician Profiles, Patient Profiles

-- =====================================================
-- USERS (15 users: 10 patients, 3 clinicians, 2 admins)
-- =====================================================

INSERT INTO users (id, email, hashed_password, full_name, phone, date_of_birth, gender, role, status, address_line1, city, state, postal_code, country, emergency_contact_name, emergency_contact_phone, email_verified, phone_verified) VALUES

-- Clinicians (IDs 1-3)
(1, 'dr.sarah.johnson@medisense.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Dr. Sarah Johnson', '+1-555-0101', '1975-03-15', 'Female', 'clinician', 'active', '123 Medical Center Dr', 'Boston', 'Massachusetts', '02101', 'USA', 'Michael Johnson', '+1-555-0102', TRUE, TRUE),

(2, 'dr.james.wilson@medisense.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Dr. James Wilson', '+1-555-0103', '1968-07-22', 'Male', 'clinician', 'active', '456 Healthcare Ave', 'Boston', 'Massachusetts', '02102', 'USA', 'Emily Wilson', '+1-555-0104', TRUE, TRUE),

(3, 'dr.priya.patel@medisense.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Dr. Priya Patel', '+1-555-0105', '1982-11-08', 'Female', 'clinician', 'active', '789 Wellness Blvd', 'Cambridge', 'Massachusetts', '02139', 'USA', 'Raj Patel', '+1-555-0106', TRUE, TRUE),

-- Admins (IDs 4-5)
(4, 'admin@medisense.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'System Administrator', '+1-555-0107', '1985-01-20', 'Male', 'admin', 'active', '100 Admin Plaza', 'Boston', 'Massachusetts', '02103', 'USA', 'HR Department', '+1-555-0108', TRUE, TRUE),

(5, 'nurse.manager@medisense.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Maria Garcia', '+1-555-0109', '1979-06-12', 'Female', 'nurse', 'active', '200 Care Center', 'Boston', 'Massachusetts', '02104', 'USA', 'Carlos Garcia', '+1-555-0110', TRUE, TRUE),

-- Patients (IDs 6-15)
(6, 'john.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'John Doe', '+1-555-1001', '1990-05-14', 'Male', 'patient', 'active', '45 Oak Street', 'Boston', 'Massachusetts', '02105', 'USA', 'Jane Doe', '+1-555-1002', TRUE, TRUE),

(7, 'jane.smith@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Jane Smith', '+1-555-1003', '1985-09-23', 'Female', 'patient', 'active', '78 Maple Avenue', 'Cambridge', 'Massachusetts', '02140', 'USA', 'Robert Smith', '+1-555-1004', TRUE, TRUE),

(8, 'robert.brown@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Robert Brown', '+1-555-1005', '1978-12-03', 'Male', 'patient', 'active', '234 Pine Road', 'Somerville', 'Massachusetts', '02143', 'USA', 'Lisa Brown', '+1-555-1006', TRUE, TRUE),

(9, 'emily.davis@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Emily Davis', '+1-555-1007', '1992-04-17', 'Female', 'patient', 'active', '567 Cedar Lane', 'Brookline', 'Massachusetts', '02445', 'USA', 'Michael Davis', '+1-555-1008', TRUE, TRUE),

(10, 'michael.wilson@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Michael Wilson', '+1-555-1009', '1965-08-30', 'Male', 'patient', 'active', '890 Birch Street', 'Newton', 'Massachusetts', '02458', 'USA', 'Susan Wilson', '+1-555-1010', TRUE, TRUE),

(11, 'sarah.martinez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Sarah Martinez', '+1-555-1011', '1988-02-28', 'Female', 'patient', 'active', '123 Elm Court', 'Quincy', 'Massachusetts', '02169', 'USA', 'Carlos Martinez', '+1-555-1012', TRUE, TRUE),

(12, 'david.lee@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'David Lee', '+1-555-1013', '1995-11-11', 'Male', 'patient', 'active', '456 Willow Way', 'Medford', 'Massachusetts', '02155', 'USA', 'Grace Lee', '+1-555-1014', TRUE, TRUE),

(13, 'jennifer.taylor@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Jennifer Taylor', '+1-555-1015', '1972-07-05', 'Female', 'patient', 'active', '789 Spruce Drive', 'Malden', 'Massachusetts', '02148', 'USA', 'Mark Taylor', '+1-555-1016', TRUE, TRUE),

(14, 'christopher.anderson@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Christopher Anderson', '+1-555-1017', '1983-10-19', 'Male', 'patient', 'active', '321 Ash Boulevard', 'Waltham', 'Massachusetts', '02451', 'USA', 'Nancy Anderson', '+1-555-1018', TRUE, TRUE),

(15, 'amanda.thomas@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4o3u1X9qHqXxF1Aq', 'Amanda Thomas', '+1-555-1019', '1998-03-25', 'Female', 'patient', 'active', '654 Hickory Place', 'Arlington', 'Massachusetts', '02474', 'USA', 'James Thomas', '+1-555-1020', TRUE, TRUE);

-- Reset sequence
SELECT setval('users_id_seq', 15, true);

-- =====================================================
-- CLINICIAN PROFILES
-- =====================================================

INSERT INTO clinician_profiles (user_id, license_number, license_state, license_expiry, specialty, sub_specialty, department, years_of_experience, education, certifications, consultation_fee, telemedicine_enabled, average_rating, total_reviews, bio) VALUES

(1, 'MA-MD-2005-12345', 'Massachusetts', '2026-12-31', 'Internal Medicine', 'Primary Care', 'General Medicine', 19, 'MD from Harvard Medical School, Residency at Massachusetts General Hospital', ARRAY['Board Certified Internal Medicine', 'ACLS Certified', 'BLS Certified'], 150.00, TRUE, 4.85, 127, 'Dr. Sarah Johnson is a compassionate internal medicine physician with nearly 20 years of experience. She specializes in preventive care and chronic disease management.'),

(2, 'MA-MD-1998-67890', 'Massachusetts', '2025-06-30', 'Cardiology', 'Interventional Cardiology', 'Cardiology', 26, 'MD from Johns Hopkins University, Fellowship at Cleveland Clinic', ARRAY['Board Certified Cardiology', 'Board Certified Interventional Cardiology', 'FACC'], 250.00, TRUE, 4.92, 89, 'Dr. James Wilson is a renowned cardiologist specializing in complex cardiac interventions. He has performed over 5,000 cardiac procedures throughout his career.'),

(3, 'MA-MD-2010-54321', 'Massachusetts', '2027-03-15', 'Dermatology', 'Medical Dermatology', 'Dermatology', 14, 'MD from Stanford University, Residency at UCSF', ARRAY['Board Certified Dermatology', 'Fellow AAD', 'Dermoscopy Certified'], 175.00, TRUE, 4.78, 156, 'Dr. Priya Patel is an expert dermatologist with special interests in skin cancer detection, acne treatment, and cosmetic dermatology. She uses advanced imaging techniques for accurate diagnosis.');

-- =====================================================
-- PATIENT PROFILES
-- =====================================================

INSERT INTO patient_profiles (user_id, blood_type, height_cm, weight_kg, allergies, chronic_conditions, current_medications, family_history, insurance_provider, insurance_policy_number, insurance_group_number, primary_care_physician_id, preferred_pharmacy, preferred_language) VALUES

(6, 'O+', 178.5, 82.3, ARRAY['Penicillin', 'Shellfish'], ARRAY['Type 2 Diabetes', 'Hypertension'], ARRAY['Metformin 500mg', 'Lisinopril 10mg'], 'Father had heart disease, Mother has diabetes', 'Blue Cross Blue Shield', 'BCBS-12345678', 'GRP-001', 1, 'CVS Pharmacy - 123 Main St, Boston', 'English'),

(7, 'A-', 165.0, 58.7, ARRAY['Latex'], ARRAY['Asthma'], ARRAY['Albuterol inhaler PRN'], 'No significant family history', 'Aetna', 'AET-98765432', 'GRP-002', 1, 'Walgreens - 456 Center St, Cambridge', 'English'),

(8, 'B+', 182.0, 95.4, ARRAY['Sulfa drugs'], ARRAY['Hyperlipidemia', 'Obesity'], ARRAY['Atorvastatin 20mg'], 'Both parents had high cholesterol', 'United Healthcare', 'UHC-55667788', 'GRP-003', 1, 'Rite Aid - 789 North Ave, Somerville', 'English'),

(9, 'AB+', 160.5, 54.2, NULL, ARRAY['Anxiety', 'Migraine'], ARRAY['Sertraline 50mg', 'Sumatriptan PRN'], 'Mother has anxiety disorder', 'Cigna', 'CIG-11223344', 'GRP-004', 1, 'CVS Pharmacy - 321 East St, Brookline', 'English'),

(10, 'A+', 175.0, 88.9, ARRAY['Aspirin', 'NSAIDs'], ARRAY['Coronary Artery Disease', 'Type 2 Diabetes', 'Hypertension'], ARRAY['Clopidogrel 75mg', 'Metformin 1000mg', 'Amlodipine 5mg', 'Atorvastatin 40mg'], 'Father died of heart attack at 60', 'Medicare', 'MED-44556677', 'GRP-005', 2, 'Walgreens - 567 West Blvd, Newton', 'English'),

(11, 'O-', 168.0, 62.5, ARRAY['Codeine'], ARRAY['Hypothyroidism'], ARRAY['Levothyroxine 75mcg'], 'Mother has thyroid disease', 'Harvard Pilgrim', 'HP-33445566', 'GRP-006', 1, 'CVS Pharmacy - 890 South St, Quincy', 'Spanish'),

(12, 'B-', 170.5, 70.3, NULL, NULL, NULL, 'No significant family history', 'Blue Cross Blue Shield', 'BCBS-77889900', 'GRP-007', 3, 'Walgreens - 234 Park Ave, Medford', 'English'),

(13, 'A+', 162.0, 72.8, ARRAY['Ibuprofen'], ARRAY['Osteoarthritis', 'Hypertension'], ARRAY['Acetaminophen PRN', 'Hydrochlorothiazide 25mg'], 'Both parents had arthritis', 'Tufts Health Plan', 'THP-66778899', 'GRP-008', 1, 'Rite Aid - 567 River Rd, Malden', 'English'),

(14, 'AB-', 185.0, 91.2, ARRAY['Amoxicillin'], ARRAY['GERD', 'Sleep Apnea'], ARRAY['Omeprazole 20mg'], 'Father has GERD', 'Aetna', 'AET-22334455', 'GRP-009', 1, 'CVS Pharmacy - 890 Hill St, Waltham', 'English'),

(15, 'O+', 157.5, 50.8, NULL, NULL, ARRAY['Multivitamin'], 'No significant family history', 'United Healthcare', 'UHC-99001122', 'GRP-010', 3, 'Walgreens - 123 Valley Dr, Arlington', 'English');

-- =====================================================
-- CLINICIAN AVAILABILITY
-- =====================================================

INSERT INTO clinician_availability (clinician_id, day_of_week, start_time, end_time, slot_duration_minutes, is_available, location, telemedicine_only) VALUES

-- Dr. Sarah Johnson (user_id = 1)
(1, 1, '09:00', '17:00', 30, TRUE, 'Main Clinic - Room 101', FALSE),
(1, 2, '09:00', '17:00', 30, TRUE, 'Main Clinic - Room 101', FALSE),
(1, 3, '09:00', '13:00', 30, TRUE, 'Main Clinic - Room 101', FALSE),
(1, 4, '09:00', '17:00', 30, TRUE, 'Main Clinic - Room 101', FALSE),
(1, 5, '09:00', '15:00', 30, TRUE, 'Telemedicine', TRUE),

-- Dr. James Wilson (user_id = 2)
(2, 1, '08:00', '16:00', 45, TRUE, 'Cardiology Center - Room 201', FALSE),
(2, 2, '08:00', '16:00', 45, TRUE, 'Cardiology Center - Room 201', FALSE),
(2, 3, '08:00', '12:00', 45, TRUE, 'Cardiology Center - Room 201', FALSE),
(2, 4, '08:00', '16:00', 45, TRUE, 'Cardiology Center - Room 201', FALSE),
(2, 5, '10:00', '14:00', 45, TRUE, 'Telemedicine', TRUE),

-- Dr. Priya Patel (user_id = 3)
(3, 1, '10:00', '18:00', 20, TRUE, 'Dermatology Clinic - Room 301', FALSE),
(3, 2, '10:00', '18:00', 20, TRUE, 'Dermatology Clinic - Room 301', FALSE),
(3, 3, '10:00', '18:00', 20, TRUE, 'Dermatology Clinic - Room 301', FALSE),
(3, 4, '10:00', '18:00', 20, TRUE, 'Dermatology Clinic - Room 301', FALSE),
(3, 5, '10:00', '14:00', 20, TRUE, 'Telemedicine', TRUE);

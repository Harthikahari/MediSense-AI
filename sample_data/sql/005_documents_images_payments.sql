-- MediSense-AI Sample Data - Documents, Images, Payments
-- Contains: Medical Documents, Image Analyses, Payments, Notifications

-- =====================================================
-- MEDICAL DOCUMENTS (12 documents)
-- =====================================================

INSERT INTO medical_documents (id, patient_id, uploaded_by, appointment_id, document_type, title, description, file_path, file_name, file_size_bytes, mime_type, ocr_text, extracted_data, is_confidential) VALUES

(1, 6, 1, 1, 'lab_report', 'HbA1c and Lipid Panel Results', 'Quarterly diabetes monitoring labs', '/documents/patient_6/lab_report_2025_11_15.pdf', 'lab_report_2025_11_15.pdf', 245678, 'application/pdf',
'LABORATORY REPORT\nPatient: John Doe\nDOB: 05/14/1990\nDate: 11/15/2025\n\nHbA1c: 6.8% (Target: <7.0%)\nFasting Glucose: 126 mg/dL\nTotal Cholesterol: 185 mg/dL\nLDL: 98 mg/dL\nHDL: 52 mg/dL\nTriglycerides: 145 mg/dL',
'{"hba1c": "6.8%", "fasting_glucose": "126 mg/dL", "total_cholesterol": "185 mg/dL", "ldl": "98 mg/dL", "hdl": "52 mg/dL", "triglycerides": "145 mg/dL"}',
FALSE),

(2, 10, 2, 3, 'imaging', 'Echocardiogram Report', 'Cardiac function assessment', '/documents/patient_10/echo_2025_11_14.pdf', 'echo_2025_11_14.pdf', 512456, 'application/pdf',
'ECHOCARDIOGRAM REPORT\nPatient: Michael Wilson\nDate: 11/14/2025\n\nLeft Ventricular Ejection Fraction: 55%\nNo wall motion abnormalities\nMild mitral regurgitation\nNormal LV size and function',
'{"lvef": "55%", "wall_motion": "normal", "mitral_valve": "mild regurgitation", "lv_function": "normal"}',
FALSE),

(3, 10, 2, 3, 'lab_report', 'Cardiac Enzymes Panel', 'Troponin and BNP levels', '/documents/patient_10/cardiac_enzymes_2025_11_14.pdf', 'cardiac_enzymes_2025_11_14.pdf', 156789, 'application/pdf',
'CARDIAC BIOMARKERS\nPatient: Michael Wilson\nDate: 11/14/2025\n\nTroponin I: <0.04 ng/mL (Normal)\nBNP: 125 pg/mL (Mildly elevated)\nCK-MB: 2.1 ng/mL (Normal)',
'{"troponin_i": "<0.04 ng/mL", "bnp": "125 pg/mL", "ck_mb": "2.1 ng/mL", "interpretation": "No acute MI"}',
FALSE),

(4, 7, 1, 2, 'lab_report', 'Pulmonary Function Test', 'Asthma severity assessment', '/documents/patient_7/pft_2025_11_15.pdf', 'pft_2025_11_15.pdf', 189456, 'application/pdf',
'PULMONARY FUNCTION TEST\nPatient: Jane Smith\nDate: 11/15/2025\n\nFEV1: 2.8L (85% predicted)\nFVC: 3.4L (92% predicted)\nFEV1/FVC: 82%\nPEF: 380 L/min',
'{"fev1": "2.8L", "fev1_percent": "85%", "fvc": "3.4L", "fvc_percent": "92%", "fev1_fvc_ratio": "82%"}',
FALSE),

(5, 8, 1, 4, 'lab_report', 'Complete Metabolic Panel', 'Annual physical labs', '/documents/patient_8/cmp_2025_11_16.pdf', 'cmp_2025_11_16.pdf', 178234, 'application/pdf',
'COMPREHENSIVE METABOLIC PANEL\nPatient: Robert Brown\nDate: 11/16/2025\n\nGlucose: 108 mg/dL\nBUN: 18 mg/dL\nCreatinine: 1.0 mg/dL\nSodium: 140 mEq/L\nPotassium: 4.2 mEq/L\nALT: 32 U/L\nAST: 28 U/L',
'{"glucose": "108 mg/dL", "bun": "18 mg/dL", "creatinine": "1.0 mg/dL", "sodium": "140 mEq/L", "potassium": "4.2 mEq/L"}',
FALSE),

(6, 11, 1, NULL, 'lab_report', 'Thyroid Function Test', 'TSH and T4 levels', '/documents/patient_11/thyroid_2025_11_10.pdf', 'thyroid_2025_11_10.pdf', 134567, 'application/pdf',
'THYROID PANEL\nPatient: Sarah Martinez\nDate: 11/10/2025\n\nTSH: 5.8 mIU/L (Slightly elevated)\nFree T4: 0.9 ng/dL (Low normal)\nFree T3: 2.8 pg/mL (Normal)',
'{"tsh": "5.8 mIU/L", "free_t4": "0.9 ng/dL", "free_t3": "2.8 pg/mL", "interpretation": "Subclinical hypothyroidism"}',
FALSE),

(7, 6, 6, NULL, 'insurance', 'Insurance Card', 'Blue Cross Blue Shield coverage', '/documents/patient_6/insurance_card.pdf', 'insurance_card.pdf', 89234, 'application/pdf',
'Blue Cross Blue Shield\nMember: John Doe\nPolicy: BCBS-12345678\nGroup: GRP-001\nEffective: 01/01/2025',
'{"provider": "Blue Cross Blue Shield", "policy_number": "BCBS-12345678", "group_number": "GRP-001"}',
TRUE),

(8, 13, 1, NULL, 'medical_history', 'Medical History Summary', 'Comprehensive health history', '/documents/patient_13/medical_history.pdf', 'medical_history.pdf', 234567, 'application/pdf',
'MEDICAL HISTORY\nPatient: Jennifer Taylor\nConditions: Hypertension (2018), Osteoarthritis (2020)\nSurgeries: Cholecystectomy (2015)\nAllergies: Ibuprofen',
'{"conditions": ["Hypertension", "Osteoarthritis"], "surgeries": ["Cholecystectomy 2015"], "allergies": ["Ibuprofen"]}',
FALSE),

(9, 12, 3, 5, 'imaging', 'Dermatoscopy Images', 'Skin lesion documentation', '/documents/patient_12/dermoscopy_2025_11_17.pdf', 'dermoscopy_2025_11_17.pdf', 1245678, 'application/pdf',
'DERMATOSCOPY REPORT\nPatient: David Lee\nDate: 11/17/2025\nLocation: Right forearm\nFindings: Contact dermatitis pattern\nNo concerning features',
'{"location": "Right forearm", "findings": "Contact dermatitis", "malignancy_risk": "Low"}',
FALSE),

(10, 14, 1, NULL, 'lab_report', 'H. Pylori Test Results', 'Breath test for H. pylori', '/documents/patient_14/hpylori_2025_11_12.pdf', 'hpylori_2025_11_12.pdf', 98765, 'application/pdf',
'H. PYLORI BREATH TEST\nPatient: Christopher Anderson\nDate: 11/12/2025\nResult: NEGATIVE\nNo active H. pylori infection detected',
'{"test_type": "Urea breath test", "result": "Negative", "h_pylori_detected": false}',
FALSE),

(11, 10, 2, 14, 'discharge_summary', 'Emergency Discharge Summary', 'Chest pain evaluation discharge', '/documents/patient_10/discharge_2025_11_20.pdf', 'discharge_2025_11_20.pdf', 345678, 'application/pdf',
'DISCHARGE SUMMARY\nPatient: Michael Wilson\nAdmit: 11/20/2025\nDischarge: 11/20/2025\nDiagnosis: Chest pain - non-cardiac\nFollow-up: Cardiology in 1 week',
'{"diagnosis": "Non-cardiac chest pain", "admit_date": "2025-11-20", "discharge_date": "2025-11-20", "follow_up": "1 week"}',
FALSE),

(12, 9, 1, NULL, 'consent_form', 'Telemedicine Consent Form', 'Signed consent for virtual visits', '/documents/patient_9/telemedicine_consent.pdf', 'telemedicine_consent.pdf', 67890, 'application/pdf',
'TELEMEDICINE CONSENT\nPatient: Emily Davis\nDate Signed: 11/01/2025\nConsent given for telemedicine consultations',
'{"consent_type": "Telemedicine", "date_signed": "2025-11-01", "consent_given": true}',
FALSE);

-- Reset sequence
SELECT setval('medical_documents_id_seq', 12, true);

-- =====================================================
-- IMAGE ANALYSES (10 image analysis records)
-- =====================================================

INSERT INTO image_analyses (id, patient_id, uploaded_by, appointment_id, image_path, image_name, body_part, symptom_description, status, ai_predictions, ai_confidence, ai_model_version, clinician_review, reviewed_by, reviewed_at, final_diagnosis) VALUES

(1, 12, 12, 5, '/images/patient_12/skin_rash_001.jpg', 'skin_rash_001.jpg', 'Right forearm', 'Red, itchy rash appeared after using new detergent', 'completed',
'{"predictions": [{"label": "contact_dermatitis", "confidence": 0.87}, {"label": "eczema", "confidence": 0.08}, {"label": "psoriasis", "confidence": 0.03}]}',
0.87, 'medisense-derm-v2.1', 'AI prediction confirmed. Classic presentation of allergic contact dermatitis.', 3, '2025-11-17 10:25:00+00', 'Allergic Contact Dermatitis'),

(2, 15, 15, NULL, '/images/patient_15/mole_back_001.jpg', 'mole_back_001.jpg', 'Upper back', 'Mole that has changed in size over past month', 'review_required',
'{"predictions": [{"label": "melanocytic_nevus", "confidence": 0.62}, {"label": "dysplastic_nevus", "confidence": 0.28}, {"label": "melanoma", "confidence": 0.08}]}',
0.62, 'medisense-derm-v2.1', NULL, NULL, NULL, NULL),

(3, 6, 6, NULL, '/images/patient_6/foot_wound_001.jpg', 'foot_wound_001.jpg', 'Left foot', 'Small wound not healing properly, diabetic patient', 'completed',
'{"predictions": [{"label": "diabetic_foot_ulcer", "confidence": 0.78}, {"label": "wound_infection", "confidence": 0.15}, {"label": "normal_wound", "confidence": 0.05}]}',
0.78, 'medisense-wound-v1.3', 'Early diabetic ulcer. Referred to wound care clinic.', 1, '2025-11-18 14:30:00+00', 'Diabetic Foot Ulcer - Grade 1'),

(4, 7, 7, NULL, '/images/patient_7/throat_001.jpg', 'throat_001.jpg', 'Throat', 'Sore throat for 3 days, difficulty swallowing', 'completed',
'{"predictions": [{"label": "pharyngitis_viral", "confidence": 0.72}, {"label": "pharyngitis_bacterial", "confidence": 0.20}, {"label": "tonsillitis", "confidence": 0.06}]}',
0.72, 'medisense-ent-v1.2', 'Viral pharyngitis likely. No strep test needed.', 1, '2025-11-16 09:45:00+00', 'Acute Viral Pharyngitis'),

(5, 9, 9, NULL, '/images/patient_9/scalp_001.jpg', 'scalp_001.jpg', 'Scalp', 'Itchy, flaky patches on scalp', 'completed',
'{"predictions": [{"label": "seborrheic_dermatitis", "confidence": 0.85}, {"label": "psoriasis", "confidence": 0.10}, {"label": "tinea_capitis", "confidence": 0.03}]}',
0.85, 'medisense-derm-v2.1', 'Classic seborrheic dermatitis. Recommend medicated shampoo.', 3, '2025-11-19 11:20:00+00', 'Seborrheic Dermatitis'),

(6, 8, 8, NULL, '/images/patient_8/eye_001.jpg', 'eye_001.jpg', 'Right eye', 'Red, irritated eye with discharge', 'processing',
'{"predictions": [{"label": "conjunctivitis_bacterial", "confidence": 0.55}, {"label": "conjunctivitis_viral", "confidence": 0.35}, {"label": "allergic_conjunctivitis", "confidence": 0.08}]}',
0.55, 'medisense-eye-v1.1', NULL, NULL, NULL, NULL),

(7, 11, 11, NULL, '/images/patient_11/neck_swelling_001.jpg', 'neck_swelling_001.jpg', 'Anterior neck', 'Visible swelling in front of neck, no pain', 'completed',
'{"predictions": [{"label": "thyroid_nodule", "confidence": 0.68}, {"label": "goiter", "confidence": 0.25}, {"label": "lymphadenopathy", "confidence": 0.05}]}',
0.68, 'medisense-endo-v1.0', 'Consistent with thyroid enlargement. Ultrasound recommended.', 1, '2025-11-17 16:00:00+00', 'Thyroid Goiter - Benign'),

(8, 13, 13, NULL, '/images/patient_13/knee_001.jpg', 'knee_001.jpg', 'Right knee', 'Swelling and redness around knee joint', 'completed',
'{"predictions": [{"label": "osteoarthritis_flare", "confidence": 0.75}, {"label": "bursitis", "confidence": 0.15}, {"label": "gout", "confidence": 0.08}]}',
0.75, 'medisense-msk-v1.4', 'OA flare consistent with patient history. No infection signs.', 1, '2025-11-18 10:15:00+00', 'Osteoarthritis Flare - Right Knee'),

(9, 14, 14, NULL, '/images/patient_14/tongue_001.jpg', 'tongue_001.jpg', 'Tongue', 'White patches on tongue', 'pending',
NULL, NULL, 'medisense-ent-v1.2', NULL, NULL, NULL, NULL),

(10, 10, 10, NULL, '/images/patient_10/chest_xray_001.jpg', 'chest_xray_001.jpg', 'Chest', 'Routine chest X-ray for cardiac evaluation', 'completed',
'{"predictions": [{"label": "cardiomegaly_mild", "confidence": 0.65}, {"label": "normal", "confidence": 0.30}, {"label": "pulmonary_congestion", "confidence": 0.03}]}',
0.65, 'medisense-radiology-v2.0', 'Mild cardiomegaly consistent with patient history. No acute findings.', 2, '2025-11-14 09:30:00+00', 'Mild Cardiomegaly - Stable');

-- Reset sequence
SELECT setval('image_analyses_id_seq', 10, true);

-- =====================================================
-- PAYMENTS (12 payment records)
-- =====================================================

INSERT INTO payments (id, patient_id, appointment_id, amount, currency, status, payment_method, transaction_id, gateway_response, description, invoice_number, insurance_claim_id, insurance_amount, patient_responsibility, paid_at) VALUES

(1, 6, 1, 150.00, 'USD', 'captured', 'credit_card', 'TXN-2025111501', '{"status": "approved", "auth_code": "A12345"}', 'Consultation - Dr. Sarah Johnson', 'INV-2025-0001', 'CLM-BCBS-001', 120.00, 30.00, '2025-11-15 09:40:00+00'),

(2, 7, 2, 150.00, 'USD', 'captured', 'credit_card', 'TXN-2025111502', '{"status": "approved", "auth_code": "A12346"}', 'Follow-up - Dr. Sarah Johnson', 'INV-2025-0002', 'CLM-AET-001', 135.00, 15.00, '2025-11-15 10:35:00+00'),

(3, 10, 3, 250.00, 'USD', 'captured', 'credit_card', 'TXN-2025111401', '{"status": "approved", "auth_code": "A12347"}', 'Cardiology Consultation - Dr. James Wilson', 'INV-2025-0003', 'CLM-MED-001', 200.00, 50.00, '2025-11-14 08:55:00+00'),

(4, 8, 4, 150.00, 'USD', 'captured', 'debit_card', 'TXN-2025111601', '{"status": "approved", "auth_code": "A12348"}', 'Annual Physical - Dr. Sarah Johnson', 'INV-2025-0004', 'CLM-UHC-001', 150.00, 0.00, '2025-11-16 14:45:00+00'),

(5, 12, 5, 175.00, 'USD', 'captured', 'credit_card', 'TXN-2025111701', '{"status": "approved", "auth_code": "A12349"}', 'Dermatology Consultation - Dr. Priya Patel', 'INV-2025-0005', 'CLM-BCBS-002', 140.00, 35.00, '2025-11-17 10:30:00+00'),

(6, 6, 6, 250.00, 'USD', 'authorized', 'credit_card', 'TXN-2025112501', '{"status": "authorized", "auth_code": "A12350"}', 'Upcoming Cardiology Consultation', 'INV-2025-0006', NULL, 0.00, 250.00, NULL),

(7, 9, 7, 150.00, 'USD', 'pending', 'insurance', NULL, NULL, 'Telemedicine Follow-up', 'INV-2025-0007', 'CLM-CIG-001', 135.00, 15.00, NULL),

(8, 10, 14, 500.00, 'USD', 'captured', 'credit_card', 'TXN-2025112001', '{"status": "approved", "auth_code": "A12351"}', 'Emergency Cardiac Evaluation', 'INV-2025-0008', 'CLM-MED-002', 400.00, 100.00, '2025-11-20 09:20:00+00'),

(9, 11, 8, 150.00, 'USD', 'pending', 'insurance', NULL, NULL, 'Upcoming Consultation', 'INV-2025-0009', NULL, 0.00, 150.00, NULL),

(10, 13, 9, 150.00, 'USD', 'authorized', 'credit_card', 'TXN-2025112801', '{"status": "authorized", "auth_code": "A12352"}', 'Blood Pressure Follow-up', 'INV-2025-0010', 'CLM-THP-001', 120.00, 30.00, NULL),

(11, 15, 11, 175.00, 'USD', 'refunded', 'credit_card', 'TXN-2025111801', '{"status": "refunded", "refund_id": "REF-001"}', 'Cancelled Dermatology Appointment', 'INV-2025-0011', NULL, 0.00, 175.00, NULL),

(12, 14, 10, 150.00, 'USD', 'pending', 'insurance', NULL, NULL, 'Upcoming Telemedicine Consultation', 'INV-2025-0012', 'CLM-AET-002', 135.00, 15.00, NULL);

-- Update refunded payment
UPDATE payments SET refund_amount = 175.00, refund_reason = 'Patient cancelled appointment' WHERE id = 11;

-- Reset sequence
SELECT setval('payments_id_seq', 12, true);

-- =====================================================
-- NOTIFICATIONS (15 notifications)
-- =====================================================

INSERT INTO notifications (id, user_id, type, status, subject, message, recipient_address, sent_at, delivered_at, read_at) VALUES

(1, 6, 'email', 'delivered', 'Appointment Confirmation', 'Your appointment with Dr. Sarah Johnson on Nov 15, 2025 at 9:00 AM has been confirmed.', 'john.doe@email.com', '2025-11-14 10:00:00+00', '2025-11-14 10:01:00+00', '2025-11-14 12:30:00+00'),

(2, 6, 'sms', 'delivered', 'Appointment Reminder', 'Reminder: Your appointment is tomorrow at 9:00 AM with Dr. Johnson.', '+1-555-1001', '2025-11-14 18:00:00+00', '2025-11-14 18:00:05+00', NULL),

(3, 10, 'email', 'delivered', 'Lab Results Available', 'Your cardiac enzyme results are now available in your patient portal.', 'michael.wilson@email.com', '2025-11-14 14:00:00+00', '2025-11-14 14:01:00+00', '2025-11-14 16:45:00+00'),

(4, 7, 'email', 'delivered', 'Prescription Ready', 'Your prescription for Albuterol is ready for pickup at Walgreens.', 'jane.smith@email.com', '2025-11-15 11:00:00+00', '2025-11-15 11:01:00+00', '2025-11-15 13:20:00+00'),

(5, 12, 'sms', 'delivered', 'Follow-up Reminder', 'Please schedule your follow-up appointment for Dec 1, 2025.', '+1-555-1013', '2025-11-17 12:00:00+00', '2025-11-17 12:00:08+00', NULL),

(6, 9, 'email', 'sent', 'Telemedicine Link', 'Your telemedicine appointment link: https://telemedicine.medisense.com/room/abc123', 'emily.davis@email.com', '2025-11-25 09:00:00+00', NULL, NULL),

(7, 6, 'email', 'delivered', 'Payment Receipt', 'Payment of $30.00 received for your visit on Nov 15, 2025. Thank you!', 'john.doe@email.com', '2025-11-15 09:45:00+00', '2025-11-15 09:46:00+00', '2025-11-15 10:30:00+00'),

(8, 15, 'email', 'delivered', 'Appointment Cancelled', 'Your appointment on Nov 18, 2025 has been cancelled as requested.', 'amanda.thomas@email.com', '2025-11-17 09:05:00+00', '2025-11-17 09:06:00+00', '2025-11-17 09:30:00+00'),

(9, 10, 'email', 'delivered', 'Discharge Instructions', 'Please review your discharge instructions and follow-up care plan.', 'michael.wilson@email.com', '2025-11-20 09:30:00+00', '2025-11-20 09:31:00+00', '2025-11-20 10:15:00+00'),

(10, 11, 'sms', 'pending', 'Appointment Reminder', 'Reminder: Your appointment is on Nov 27 at 3:00 PM.', '+1-555-1011', NULL, NULL, NULL),

(11, 8, 'email', 'delivered', 'New Prescription', 'A new prescription for Atorvastatin has been sent to your pharmacy.', 'robert.brown@email.com', '2025-11-16 15:00:00+00', '2025-11-16 15:01:00+00', '2025-11-16 17:45:00+00'),

(12, 13, 'email', 'sent', 'Appointment Confirmation', 'Your appointment with Dr. Johnson on Nov 28 at 9:30 AM is confirmed.', 'jennifer.taylor@email.com', '2025-11-21 10:00:00+00', NULL, NULL),

(13, 6, 'push', 'delivered', 'Lab Results', 'Your HbA1c results are available. Tap to view.', NULL, '2025-11-15 14:00:00+00', '2025-11-15 14:00:02+00', '2025-11-15 14:05:00+00'),

(14, 14, 'email', 'pending', 'Telemedicine Appointment', 'Your telemedicine appointment is scheduled for Nov 29 at 2:00 PM.', 'christopher.anderson@email.com', NULL, NULL, NULL),

(15, 10, 'sms', 'failed', 'Medication Reminder', 'Remember to take your evening medications.', '+1-555-1009', '2025-11-20 20:00:00+00', NULL, NULL);

-- Update failed notification
UPDATE notifications SET error_message = 'Invalid phone number format', retry_count = 3 WHERE id = 15;

-- Reset sequence
SELECT setval('notifications_id_seq', 15, true);

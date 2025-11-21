-- MediSense-AI Sample Data - Audit Logs, Guardrail Violations, Chat Sessions
-- Contains: Audit trail, security events, and chat history

-- =====================================================
-- AUDIT LOGS (20 audit entries)
-- =====================================================

INSERT INTO audit_logs (id, user_id, session_id, event_type, agent_name, action, resource_type, resource_id, input_data, output_data, ip_address, user_agent, success, execution_time_ms, provenance, phi_accessed) VALUES

(1, 6, 'sess_001', 'login', NULL, 'user_login', 'auth', NULL, '{"email": "john.doe@email.com"}', '{"success": true, "token_issued": true}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 245, '{"source": "web_app", "version": "1.0.0"}', FALSE),

(2, 6, 'sess_001', 'agent_action', 'routing_agent', 'classify_intent', 'query', NULL, '{"query": "I want to book an appointment with Dr. Johnson"}', '{"target_agent": "appointment", "confidence": 0.92}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 156, '{"agent_version": "1.0", "model": "rule_based"}', FALSE),

(3, 6, 'sess_001', 'agent_action', 'appointment_agent', 'check_availability', 'appointment', NULL, '{"clinician_id": 1, "date": "2025-11-25"}', '{"available_slots": ["09:00", "10:30", "14:00"]}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 312, '{"agent_version": "1.0", "data_source": "scheduling_db"}', FALSE),

(4, 6, 'sess_001', 'agent_action', 'appointment_agent', 'book_appointment', 'appointment', '6', '{"slot": "09:00", "type": "consultation"}', '{"appointment_id": 6, "status": "scheduled"}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 428, '{"agent_version": "1.0", "action": "create"}', FALSE),

(5, 6, 'sess_001', 'agent_action', 'guardrail_agent', 'validate_response', 'response', NULL, '{"content": "Appointment confirmed for Nov 25"}', '{"violations": [], "safe": true}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 89, '{"agent_version": "1.0", "policies_checked": 5}', FALSE),

(6, 1, 'sess_002', 'login', NULL, 'clinician_login', 'auth', NULL, '{"email": "dr.sarah.johnson@medisense.com"}', '{"success": true, "role": "clinician"}', '10.0.0.50', 'Mozilla/5.0 (Macintosh; Intel Mac OS X) Safari/17.0', TRUE, 198, '{"source": "web_app", "version": "1.0.0"}', FALSE),

(7, 1, 'sess_002', 'phi_access', NULL, 'view_patient_record', 'patient', '6', '{"patient_id": 6}', '{"accessed_fields": ["name", "dob", "conditions"]}', '10.0.0.50', 'Mozilla/5.0 (Macintosh; Intel Mac OS X) Safari/17.0', TRUE, 156, '{"reason": "scheduled_appointment", "authorization": "treating_physician"}', TRUE),

(8, 1, 'sess_002', 'agent_action', 'prescription_agent', 'generate_prescription', 'prescription', '1', '{"patient_id": 6, "medications": ["Metformin"]}', '{"prescription_id": 1, "status": "created"}', '10.0.0.50', 'Mozilla/5.0 (Macintosh; Intel Mac OS X) Safari/17.0', TRUE, 534, '{"agent_version": "1.0", "interactions_checked": true}', TRUE),

(9, 7, 'sess_003', 'login', NULL, 'user_login', 'auth', NULL, '{"email": "jane.smith@email.com"}', '{"success": true}', '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Mobile Safari', TRUE, 267, '{"source": "mobile_app", "version": "2.1.0"}', FALSE),

(10, 7, 'sess_003', 'agent_action', 'rag_agent', 'search_documents', 'document', NULL, '{"query": "asthma management tips"}', '{"documents_found": 5, "top_score": 0.89}', '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Mobile Safari', TRUE, 423, '{"agent_version": "1.0", "vector_db": "chroma"}', FALSE),

(11, 12, 'sess_004', 'agent_action', 'image_agent', 'analyze_image', 'image', '1', '{"image_path": "/images/patient_12/skin_rash_001.jpg"}', '{"prediction": "contact_dermatitis", "confidence": 0.87}', '192.168.1.102', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/119.0', TRUE, 1245, '{"agent_version": "1.0", "model": "medisense-derm-v2.1"}', FALSE),

(12, 10, 'sess_005', 'agent_action', 'sql_agent', 'execute_query', 'database', NULL, '{"intent": "get my recent lab results"}', '{"query": "SELECT * FROM medical_documents WHERE patient_id = $1", "results": 3}', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 178, '{"agent_version": "1.0", "parameterized": true}', TRUE),

(13, 4, 'sess_006', 'login', NULL, 'admin_login', 'auth', NULL, '{"email": "admin@medisense.com"}', '{"success": true, "role": "admin"}', '10.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 145, '{"source": "admin_portal", "version": "1.0.0"}', FALSE),

(14, 4, 'sess_006', 'data_access', NULL, 'view_audit_logs', 'audit', NULL, '{"date_range": "2025-11-15 to 2025-11-21"}', '{"logs_retrieved": 50}', '10.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 234, '{"reason": "security_review"}', FALSE),

(15, 9, 'sess_007', 'agent_action', 'routing_agent', 'classify_intent', 'query', NULL, '{"query": "My SSN is 123-45-6789 and I need medication"}', '{"target_agent": "prescription", "phi_detected": true}', '192.168.1.104', 'Mozilla/5.0 (Android 14) Chrome/119.0', TRUE, 167, '{"agent_version": "1.0", "guardrail_triggered": true}', FALSE),

(16, 9, 'sess_007', 'agent_action', 'guardrail_agent', 'redact_phi', 'response', NULL, '{"content": "SSN: 123-45-6789"}', '{"redacted": "SSN: [REDACTED_SSN]", "violations": 1}', '192.168.1.104', 'Mozilla/5.0 (Android 14) Chrome/119.0', TRUE, 45, '{"agent_version": "1.0", "pattern": "ssn"}', FALSE),

(17, 2, 'sess_008', 'phi_access', NULL, 'view_cardiac_results', 'patient', '10', '{"patient_id": 10, "document_type": "lab_report"}', '{"document_id": 3}', '10.0.0.51', 'Mozilla/5.0 (Macintosh; Intel Mac OS X) Safari/17.0', TRUE, 189, '{"reason": "emergency_care", "authorization": "treating_physician"}', TRUE),

(18, 6, 'sess_001', 'logout', NULL, 'user_logout', 'auth', NULL, '{}', '{"session_duration_minutes": 25}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 34, '{"source": "web_app"}', FALSE),

(19, 15, 'sess_009', 'error', 'appointment_agent', 'booking_failed', 'appointment', NULL, '{"clinician_id": 3, "date": "2025-11-18"}', '{"error": "Appointment cancelled by patient"}', '192.168.1.105', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/120.0', FALSE, 0, '{"reason": "user_cancelled"}', FALSE),

(20, 10, 'sess_005', 'agent_action', 'notification_agent', 'send_notification', 'notification', '9', '{"type": "email", "template": "discharge_instructions"}', '{"notification_id": 9, "status": "sent"}', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0', TRUE, 567, '{"agent_version": "1.0", "channel": "email"}', FALSE);

-- Reset sequence
SELECT setval('audit_logs_id_seq', 20, true);

-- =====================================================
-- GUARDRAIL VIOLATIONS (8 violation records)
-- =====================================================

INSERT INTO guardrail_violations (id, audit_log_id, user_id, session_id, agent_name, violation_type, severity, original_content, redacted_content, patterns_matched, action_taken, blocked, reviewed, reviewed_by, reviewed_at, notes) VALUES

(1, 16, 9, 'sess_007', 'guardrail_agent', 'phi_exposure', 'critical', 'My SSN is 123-45-6789 and I need medication refill', 'My SSN is [REDACTED_SSN] and I need medication refill', ARRAY['ssn_pattern'], 'redacted', FALSE, TRUE, 4, '2025-11-20 14:00:00+00', 'User inadvertently shared SSN. Redacted successfully.'),

(2, NULL, 8, 'sess_010', 'guardrail_agent', 'phi_exposure', 'high', 'Please send results to my email robert.brown@email.com', 'Please send results to my email [REDACTED_EMAIL]', ARRAY['email_pattern'], 'redacted', FALSE, TRUE, 4, '2025-11-19 11:30:00+00', 'Email address redacted from chat log'),

(3, NULL, 6, 'sess_011', 'guardrail_agent', 'phi_exposure', 'high', 'My phone number is 555-1001 for callback', 'My phone number is [REDACTED_PHONE] for callback', ARRAY['phone_pattern'], 'redacted', FALSE, FALSE, NULL, NULL, NULL),

(4, NULL, 11, 'sess_012', 'guardrail_agent', 'unsafe_content', 'medium', 'Can you prescribe me some sleeping pills without seeing me?', NULL, ARRAY['prescription_request_pattern'], 'flagged', FALSE, TRUE, 1, '2025-11-18 16:45:00+00', 'User attempted to get prescription without appointment. Redirected to scheduling.'),

(5, NULL, 14, 'sess_013', 'guardrail_agent', 'phi_exposure', 'critical', 'My insurance ID is UHC-12345678', 'My insurance ID is [REDACTED_INSURANCE]', ARRAY['insurance_pattern'], 'redacted', FALSE, FALSE, NULL, NULL, NULL),

(6, NULL, 7, 'sess_003', 'guardrail_agent', 'medical_advice', 'low', 'Is it okay to double my inhaler dose?', NULL, ARRAY['dosage_modification_pattern'], 'flagged', FALSE, TRUE, 1, '2025-11-15 10:40:00+00', 'Advised patient to consult with physician before changing dosage.'),

(7, NULL, 13, 'sess_014', 'guardrail_agent', 'unsafe_content', 'high', 'I want to stop all my medications', NULL, ARRAY['medication_discontinuation_pattern'], 'flagged', FALSE, TRUE, 1, '2025-11-17 09:20:00+00', 'Patient expressed desire to stop medications. Follow-up scheduled.'),

(8, NULL, 10, 'sess_015', 'guardrail_agent', 'emergency_detection', 'critical', 'I am having severe chest pain right now', NULL, ARRAY['emergency_symptom_pattern'], 'escalated', FALSE, TRUE, 2, '2025-11-20 08:00:00+00', 'Emergency detected. Patient directed to call 911. Follow-up confirmed patient was seen in ED.');

-- Reset sequence
SELECT setval('guardrail_violations_id_seq', 8, true);

-- =====================================================
-- CHAT SESSIONS (10 chat sessions)
-- =====================================================

INSERT INTO chat_sessions (id, user_id, started_at, ended_at, total_messages, agents_used, summary, satisfaction_rating, feedback) VALUES

(1, 6, '2025-11-15 08:30:00+00', '2025-11-15 08:55:00+00', 8, ARRAY['routing', 'appointment', 'guardrail'], 'Patient booked cardiology appointment successfully', 5, 'Very easy to use! Booking was quick.'),

(2, 7, '2025-11-15 10:00:00+00', '2025-11-15 10:20:00+00', 6, ARRAY['routing', 'rag', 'guardrail'], 'Patient inquired about asthma management', 4, 'Good information provided'),

(3, 10, '2025-11-14 07:45:00+00', '2025-11-14 08:10:00+00', 10, ARRAY['routing', 'sql', 'rag', 'guardrail'], 'Patient reviewed lab results and asked questions', 5, 'Excellent! Got all the information I needed.'),

(4, 12, '2025-11-17 09:30:00+00', '2025-11-17 09:50:00+00', 7, ARRAY['routing', 'image', 'guardrail'], 'Patient uploaded skin rash image for analysis', 4, 'AI analysis was helpful'),

(5, 9, '2025-11-16 14:00:00+00', '2025-11-16 14:25:00+00', 9, ARRAY['routing', 'prescription', 'guardrail'], 'Patient inquired about medication refill', 3, 'Had to talk to human agent to complete request'),

(6, 8, '2025-11-16 11:00:00+00', '2025-11-16 11:15:00+00', 5, ARRAY['routing', 'rag', 'guardrail'], 'Patient asked about cholesterol management', 4, NULL),

(7, 11, '2025-11-17 15:30:00+00', '2025-11-17 15:45:00+00', 6, ARRAY['routing', 'appointment', 'guardrail'], 'Patient scheduled thyroid follow-up', 5, 'Quick and easy!'),

(8, 13, '2025-11-18 09:00:00+00', '2025-11-18 09:20:00+00', 8, ARRAY['routing', 'sql', 'prescription', 'guardrail'], 'Patient reviewed medications and requested refill', 4, 'Worked well overall'),

(9, 14, '2025-11-19 16:00:00+00', '2025-11-19 16:30:00+00', 12, ARRAY['routing', 'rag', 'appointment', 'guardrail'], 'Patient researched GERD and booked telemedicine appointment', 5, 'Love the telemedicine option!'),

(10, 15, '2025-11-17 08:45:00+00', '2025-11-17 09:00:00+00', 4, ARRAY['routing', 'appointment', 'guardrail'], 'Patient cancelled dermatology appointment', 3, 'Cancellation process was straightforward');

-- Reset sequence
SELECT setval('chat_sessions_id_seq', 10, true);

-- =====================================================
-- CHAT MESSAGES (Sample messages from sessions)
-- =====================================================

INSERT INTO chat_messages (id, session_id, role, content, agent_name, confidence, tokens_used, response_time_ms, metadata) VALUES

-- Session 1 - Appointment booking
(1, 1, 'user', 'Hi, I would like to book an appointment with a cardiologist', NULL, NULL, 15, NULL, NULL),
(2, 1, 'assistant', 'I can help you book a cardiology appointment. Let me check available cardiologists for you.', 'routing_agent', 0.95, 25, 156, '{"intent": "appointment"}'),
(3, 1, 'assistant', 'Dr. James Wilson is available. Here are the available slots:\n- Nov 25: 9:00 AM, 10:30 AM, 2:00 PM\n- Nov 26: 8:00 AM, 11:00 AM\nWhich would you prefer?', 'appointment_agent', 0.92, 45, 312, '{"clinician_id": 2}'),
(4, 1, 'user', 'November 25th at 9 AM works for me', NULL, NULL, 10, NULL, NULL),
(5, 1, 'assistant', 'Your appointment has been scheduled with Dr. James Wilson on November 25, 2025 at 9:00 AM at the Cardiology Center. You will receive a confirmation email shortly.', 'appointment_agent', 0.98, 40, 428, '{"appointment_id": 6}'),

-- Session 2 - RAG query
(6, 2, 'user', 'What are some tips for managing asthma?', NULL, NULL, 10, NULL, NULL),
(7, 2, 'assistant', 'Based on our medical knowledge base, here are key tips for asthma management:\n\n1. **Take medications as prescribed** - Use your controller inhaler daily\n2. **Identify triggers** - Common triggers include dust, pollen, and exercise\n3. **Monitor symptoms** - Track peak flow readings\n4. **Have an action plan** - Know what to do during an attack\n5. **Keep rescue inhaler accessible** - Always carry your quick-relief inhaler\n\nWould you like more specific information about any of these?', 'rag_agent', 0.89, 120, 423, '{"documents_used": 3}'),

-- Session 3 - Lab results query
(8, 3, 'user', 'Can I see my recent lab results?', NULL, NULL, 8, NULL, NULL),
(9, 3, 'assistant', 'I found your recent lab results. Here is a summary:\n\n**Cardiac Enzymes (Nov 14, 2025)**\n- Troponin I: <0.04 ng/mL (Normal)\n- BNP: 125 pg/mL (Mildly elevated)\n- CK-MB: 2.1 ng/mL (Normal)\n\nYour troponin levels are normal, which is reassuring. Would you like me to explain any of these results?', 'sql_agent', 0.94, 85, 178, '{"documents_retrieved": 1}'),

-- Session 4 - Image analysis
(10, 4, 'user', 'I have a rash on my arm. Can you analyze this image?', NULL, NULL, 12, NULL, '{"has_attachment": true}'),
(11, 4, 'assistant', 'I have analyzed your image. Here are the findings:\n\n**AI Analysis Results:**\n- Most likely: Contact Dermatitis (87% confidence)\n- The rash pattern suggests an allergic reaction to an external substance\n\n**Recommendations:**\n1. Avoid contact with suspected irritant\n2. Apply over-the-counter hydrocortisone cream\n3. If symptoms worsen, schedule a dermatology appointment\n\nWould you like me to book an appointment with Dr. Patel for further evaluation?', 'image_agent', 0.87, 95, 1245, '{"model_version": "medisense-derm-v2.1"}'),

-- Session 5 - Prescription inquiry with PHI
(12, 5, 'user', 'I need to refill my anxiety medication. My name is Emily Davis and my phone is 555-1007', NULL, NULL, 18, NULL, NULL),
(13, 5, 'assistant', 'I can help you with your medication refill request. I notice you included personal information - for your privacy, this has been protected.\n\nI see you have an active prescription for Sertraline 50mg. Since your prescription needs a review for renewal, I recommend scheduling a follow-up appointment with Dr. Johnson. Would you like me to schedule a telemedicine visit?', 'prescription_agent', 0.88, 75, 534, '{"phi_redacted": true}'),

-- More messages for other sessions
(14, 6, 'user', 'What should I know about managing high cholesterol?', NULL, NULL, 10, NULL, NULL),
(15, 6, 'assistant', 'Here are key points for managing high cholesterol:\n\n1. **Diet modifications** - Reduce saturated fats, increase fiber\n2. **Exercise regularly** - Aim for 150 minutes of moderate activity weekly\n3. **Take medications as prescribed** - Statins are highly effective\n4. **Monitor levels** - Regular lipid panel tests\n5. **Maintain healthy weight** - Even small weight loss helps\n\nI see you were recently prescribed Atorvastatin. Are you experiencing any side effects?', 'rag_agent', 0.91, 100, 389, '{"documents_used": 2}');

-- Reset sequence
SELECT setval('chat_messages_id_seq', 15, true);

-- =====================================================
-- VECTOR DOCUMENTS (Sample for RAG)
-- =====================================================

INSERT INTO vector_documents (id, source_type, source_id, title, content, chunk_index, embedding_id, metadata) VALUES

(1, 'medical_guideline', NULL, 'Asthma Management Guidelines', 'Asthma is a chronic respiratory condition characterized by airway inflammation and hyperresponsiveness. Management includes: 1) Controller medications (inhaled corticosteroids) for daily use, 2) Quick-relief medications (short-acting beta-agonists) for acute symptoms, 3) Trigger avoidance, 4) Regular monitoring with peak flow meters, 5) Written asthma action plan.', 0, 'emb_001', '{"category": "respiratory", "last_updated": "2025-01-15"}'),

(2, 'medical_guideline', NULL, 'Diabetes Management Overview', 'Type 2 Diabetes management focuses on glycemic control through lifestyle modifications and medications. Target HbA1c is typically <7% for most adults. Key components include: 1) Diet modification - reduce refined carbohydrates, 2) Regular exercise - 150 minutes moderate activity weekly, 3) Medication adherence - Metformin is first-line therapy, 4) Blood glucose monitoring, 5) Regular screening for complications.', 0, 'emb_002', '{"category": "endocrine", "last_updated": "2025-02-20"}'),

(3, 'medical_guideline', NULL, 'Hypertension Treatment Guidelines', 'Blood pressure targets: <130/80 mmHg for most adults with hypertension. First-line medications include ACE inhibitors, ARBs, calcium channel blockers, and thiazide diuretics. Lifestyle modifications: sodium restriction (<2300mg/day), DASH diet, regular exercise, weight management, limiting alcohol, and smoking cessation.', 0, 'emb_003', '{"category": "cardiovascular", "last_updated": "2025-03-10"}'),

(4, 'medical_guideline', NULL, 'Cholesterol Management', 'Statin therapy is recommended for: 1) Clinical ASCVD, 2) LDL ≥190 mg/dL, 3) Diabetes ages 40-75 with LDL 70-189 mg/dL, 4) 10-year ASCVD risk ≥7.5%. Lifestyle modifications include heart-healthy diet, regular physical activity, weight management, and smoking cessation. Monitor liver function and muscle symptoms on statin therapy.', 0, 'emb_004', '{"category": "cardiovascular", "last_updated": "2025-01-25"}'),

(5, 'medical_guideline', NULL, 'Contact Dermatitis Guide', 'Contact dermatitis is an inflammatory skin reaction caused by direct contact with irritants or allergens. Types: 1) Irritant contact dermatitis - caused by chemical irritants, 2) Allergic contact dermatitis - immune-mediated reaction. Treatment: Identify and avoid causative agent, topical corticosteroids, moisturizers, antihistamines for itching. Patch testing may be needed to identify specific allergens.', 0, 'emb_005', '{"category": "dermatology", "last_updated": "2025-04-05"}'),

(6, 'medical_guideline', NULL, 'Anxiety Disorder Management', 'Generalized anxiety disorder treatment options: 1) Psychotherapy - CBT is first-line, 2) Pharmacotherapy - SSRIs (sertraline, escitalopram) are first-line, SNRIs as alternative, 3) Lifestyle modifications - regular exercise, sleep hygiene, stress management, 4) Avoid caffeine and alcohol. Response to medication typically takes 4-6 weeks. Consider combination therapy for refractory cases.', 0, 'emb_006', '{"category": "psychiatry", "last_updated": "2025-02-15"}'),

(7, 'medical_guideline', NULL, 'GERD Treatment Protocol', 'Gastroesophageal reflux disease management: 1) Lifestyle modifications - weight loss, elevate head of bed, avoid trigger foods, stop smoking, 2) PPIs are most effective for healing and symptom relief, 3) H2 blockers as alternative, 4) Antacids for breakthrough symptoms. Red flags requiring urgent evaluation: dysphagia, weight loss, GI bleeding, anemia.', 0, 'emb_007', '{"category": "gastroenterology", "last_updated": "2025-03-20"}'),

(8, 'medical_guideline', NULL, 'Hypothyroidism Management', 'Hypothyroidism treatment with levothyroxine: Start low dose (25-50 mcg) in elderly or cardiac patients. Take on empty stomach, 30-60 minutes before breakfast. Avoid taking with calcium, iron, or antacids. Monitor TSH every 6-8 weeks until stable, then annually. Goal TSH typically 0.5-4.0 mIU/L, may differ based on age and comorbidities.', 0, 'emb_008', '{"category": "endocrine", "last_updated": "2025-01-30"}'),

(9, 'drug_information', 1, 'Metformin Drug Information', 'Metformin (Glucophage): Biguanide antidiabetic. Mechanism: Decreases hepatic glucose production, increases insulin sensitivity. Dosing: Start 500mg BID, max 2550mg/day. Take with meals. Key warnings: Hold before contrast procedures, monitor renal function. Common side effects: GI upset, lactic acidosis (rare).', 0, 'emb_009', '{"drug_class": "biguanide", "controlled": false}'),

(10, 'drug_information', 3, 'Atorvastatin Drug Information', 'Atorvastatin (Lipitor): HMG-CoA reductase inhibitor. Mechanism: Inhibits cholesterol synthesis in liver. Dosing: 10-80mg once daily, preferably at bedtime. Avoid grapefruit. Monitor liver function. Side effects: Myalgia, elevated transaminases, rarely rhabdomyolysis. Drug interactions: Avoid with strong CYP3A4 inhibitors.', 0, 'emb_010', '{"drug_class": "statin", "controlled": false}');

-- Reset sequence
SELECT setval('vector_documents_id_seq', 10, true);

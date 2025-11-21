-- MediSense-AI Sample Data - Appointments
-- Contains: Appointments with various statuses

-- =====================================================
-- APPOINTMENTS (15 appointments)
-- =====================================================

INSERT INTO appointments (id, patient_id, clinician_id, scheduled_start, scheduled_end, actual_start, actual_end, appointment_type, status, chief_complaint, notes, diagnosis, follow_up_required, follow_up_date, is_telemedicine, telemedicine_link, location) VALUES

-- Completed appointments
(1, 6, 1, '2025-11-15 09:00:00+00', '2025-11-15 09:30:00+00', '2025-11-15 09:05:00+00', '2025-11-15 09:35:00+00', 'consultation', 'completed', 'Routine diabetes checkup', 'Patient reports good glucose control. HbA1c improved from last visit.', 'Type 2 Diabetes Mellitus - Well controlled', TRUE, '2026-02-15', FALSE, NULL, 'Main Clinic - Room 101'),

(2, 7, 1, '2025-11-15 10:00:00+00', '2025-11-15 10:30:00+00', '2025-11-15 10:02:00+00', '2025-11-15 10:28:00+00', 'follow_up', 'completed', 'Asthma follow-up', 'Asthma well controlled with current inhaler regimen.', 'Asthma - Mild persistent, controlled', FALSE, NULL, FALSE, NULL, 'Main Clinic - Room 101'),

(3, 10, 2, '2025-11-14 08:00:00+00', '2025-11-14 08:45:00+00', '2025-11-14 08:00:00+00', '2025-11-14 08:50:00+00', 'consultation', 'completed', 'Chest pain and shortness of breath', 'ECG performed - normal sinus rhythm. Scheduled stress test.', 'Stable angina - evaluation in progress', TRUE, '2025-11-28', FALSE, NULL, 'Cardiology Center - Room 201'),

(4, 8, 1, '2025-11-16 14:00:00+00', '2025-11-16 14:30:00+00', '2025-11-16 14:10:00+00', '2025-11-16 14:40:00+00', 'routine_checkup', 'completed', 'Annual physical exam', 'Recommended weight loss program. Cholesterol slightly elevated.', 'Hyperlipidemia, Obesity', TRUE, '2026-05-16', FALSE, NULL, 'Main Clinic - Room 101'),

(5, 12, 3, '2025-11-17 10:00:00+00', '2025-11-17 10:20:00+00', '2025-11-17 10:00:00+00', '2025-11-17 10:25:00+00', 'consultation', 'completed', 'Skin rash on arms', 'Examination revealed contact dermatitis. Prescribed topical corticosteroid.', 'Allergic contact dermatitis', TRUE, '2025-12-01', FALSE, NULL, 'Dermatology Clinic - Room 301'),

-- Scheduled appointments (upcoming)
(6, 6, 2, '2025-11-25 09:00:00+00', '2025-11-25 09:45:00+00', NULL, NULL, 'consultation', 'scheduled', 'Cardiac evaluation - referred by PCP', NULL, NULL, FALSE, NULL, FALSE, NULL, 'Cardiology Center - Room 201'),

(7, 9, 1, '2025-11-26 11:00:00+00', '2025-11-26 11:30:00+00', NULL, NULL, 'follow_up', 'confirmed', 'Anxiety medication review', NULL, NULL, FALSE, NULL, TRUE, 'https://telemedicine.medisense.com/room/abc123', 'Telemedicine'),

(8, 11, 1, '2025-11-27 15:00:00+00', '2025-11-27 15:30:00+00', NULL, NULL, 'consultation', 'scheduled', 'Thyroid medication adjustment', NULL, NULL, FALSE, NULL, FALSE, NULL, 'Main Clinic - Room 101'),

(9, 13, 1, '2025-11-28 09:30:00+00', '2025-11-28 10:00:00+00', NULL, NULL, 'follow_up', 'confirmed', 'Blood pressure check', NULL, NULL, FALSE, NULL, FALSE, NULL, 'Main Clinic - Room 101'),

(10, 14, 1, '2025-11-29 14:00:00+00', '2025-11-29 14:30:00+00', NULL, NULL, 'consultation', 'scheduled', 'GERD symptoms worsening', NULL, NULL, FALSE, NULL, TRUE, 'https://telemedicine.medisense.com/room/def456', 'Telemedicine'),

-- Cancelled appointments
(11, 15, 3, '2025-11-18 11:00:00+00', '2025-11-18 11:20:00+00', NULL, NULL, 'consultation', 'cancelled', 'Acne treatment consultation', NULL, NULL, FALSE, NULL, FALSE, NULL, 'Dermatology Clinic - Room 301'),

(12, 7, 1, '2025-11-19 10:00:00+00', '2025-11-19 10:30:00+00', NULL, NULL, 'routine_checkup', 'cancelled', 'Annual checkup', NULL, NULL, FALSE, NULL, FALSE, NULL, 'Main Clinic - Room 101'),

-- In-progress appointment
(13, 15, 3, '2025-11-21 10:00:00+00', '2025-11-21 10:20:00+00', '2025-11-21 10:02:00+00', NULL, 'consultation', 'in_progress', 'Skin evaluation for moles', 'Currently examining suspicious mole on back', NULL, FALSE, NULL, FALSE, NULL, 'Dermatology Clinic - Room 301'),

-- Emergency appointment
(14, 10, 2, '2025-11-20 08:00:00+00', '2025-11-20 09:00:00+00', '2025-11-20 08:05:00+00', '2025-11-20 09:15:00+00', 'emergency', 'completed', 'Severe chest pain - urgent evaluation', 'Troponin negative. ECG showed no acute changes. Admitted for observation.', 'Acute chest pain - non-cardiac, likely musculoskeletal', TRUE, '2025-11-27', FALSE, NULL, 'Cardiology Center - Emergency'),

-- Telemedicine appointment
(15, 9, 3, '2025-11-30 13:00:00+00', '2025-11-30 13:20:00+00', NULL, NULL, 'telemedicine', 'scheduled', 'Follow-up on skin condition', NULL, NULL, FALSE, NULL, TRUE, 'https://telemedicine.medisense.com/room/ghi789', 'Telemedicine');

-- Update cancelled appointments with cancellation details
UPDATE appointments SET
    cancellation_reason = 'Patient requested reschedule due to work conflict',
    cancelled_by = 15,
    cancelled_at = '2025-11-17 09:00:00+00'
WHERE id = 11;

UPDATE appointments SET
    cancellation_reason = 'Patient illness - will reschedule when feeling better',
    cancelled_by = 7,
    cancelled_at = '2025-11-18 08:00:00+00'
WHERE id = 12;

-- Reset sequence
SELECT setval('appointments_id_seq', 15, true);

-- MediSense-AI Sample Data - Medications and Prescriptions
-- Contains: Medications catalog, Prescriptions, Prescription Items, Drug Interactions

-- =====================================================
-- MEDICATIONS CATALOG (20 common medications)
-- =====================================================

INSERT INTO medications (id, name, generic_name, brand_names, drug_class, dosage_forms, strengths, route_of_administration, description, warnings, contraindications, side_effects, interactions, pregnancy_category, controlled_substance_schedule, requires_prescription) VALUES

(1, 'Metformin', 'Metformin Hydrochloride', ARRAY['Glucophage', 'Fortamet', 'Glumetza'], 'Biguanide', ARRAY['Tablet', 'Extended-release tablet', 'Oral solution'], ARRAY['500mg', '850mg', '1000mg'], 'Oral', 'First-line medication for type 2 diabetes mellitus', 'Risk of lactic acidosis. Discontinue before contrast procedures.', ARRAY['Severe renal impairment', 'Metabolic acidosis', 'Diabetic ketoacidosis'], ARRAY['Nausea', 'Diarrhea', 'Abdominal pain', 'Vitamin B12 deficiency'], ARRAY['Alcohol', 'Iodinated contrast agents'], 'B', NULL, TRUE),

(2, 'Lisinopril', 'Lisinopril', ARRAY['Prinivil', 'Zestril'], 'ACE Inhibitor', ARRAY['Tablet'], ARRAY['2.5mg', '5mg', '10mg', '20mg', '40mg'], 'Oral', 'Used for hypertension, heart failure, and post-MI', 'Risk of angioedema. Monitor potassium levels.', ARRAY['History of angioedema', 'Pregnancy', 'Bilateral renal artery stenosis'], ARRAY['Dry cough', 'Dizziness', 'Hyperkalemia', 'Hypotension'], ARRAY['Potassium supplements', 'NSAIDs', 'Lithium'], 'D', NULL, TRUE),

(3, 'Atorvastatin', 'Atorvastatin Calcium', ARRAY['Lipitor'], 'HMG-CoA Reductase Inhibitor (Statin)', ARRAY['Tablet'], ARRAY['10mg', '20mg', '40mg', '80mg'], 'Oral', 'Used for hyperlipidemia and cardiovascular risk reduction', 'Risk of myopathy and rhabdomyolysis. Monitor liver function.', ARRAY['Active liver disease', 'Pregnancy', 'Breastfeeding'], ARRAY['Muscle pain', 'Joint pain', 'Diarrhea', 'Nausea'], ARRAY['Grapefruit juice', 'Cyclosporine', 'Gemfibrozil'], 'X', NULL, TRUE),

(4, 'Amlodipine', 'Amlodipine Besylate', ARRAY['Norvasc'], 'Calcium Channel Blocker', ARRAY['Tablet'], ARRAY['2.5mg', '5mg', '10mg'], 'Oral', 'Used for hypertension and angina', 'May cause peripheral edema', ARRAY['Severe aortic stenosis', 'Cardiogenic shock'], ARRAY['Peripheral edema', 'Flushing', 'Headache', 'Fatigue'], ARRAY['Simvastatin', 'Cyclosporine'], 'C', NULL, TRUE),

(5, 'Omeprazole', 'Omeprazole', ARRAY['Prilosec', 'Losec'], 'Proton Pump Inhibitor', ARRAY['Capsule', 'Tablet'], ARRAY['10mg', '20mg', '40mg'], 'Oral', 'Used for GERD, peptic ulcer, and H. pylori eradication', 'Long-term use may increase risk of bone fractures and C. diff infection', ARRAY['Hypersensitivity to PPIs'], ARRAY['Headache', 'Abdominal pain', 'Nausea', 'Diarrhea'], ARRAY['Clopidogrel', 'Methotrexate'], 'C', NULL, TRUE),

(6, 'Albuterol', 'Albuterol Sulfate', ARRAY['ProAir', 'Ventolin', 'Proventil'], 'Beta-2 Agonist', ARRAY['Inhaler', 'Nebulizer solution', 'Tablet'], ARRAY['90mcg/inhalation', '2.5mg/3ml', '2mg', '4mg'], 'Inhalation/Oral', 'Used for asthma and COPD', 'May cause paradoxical bronchospasm', ARRAY['Hypersensitivity to albuterol'], ARRAY['Tremor', 'Nervousness', 'Tachycardia', 'Headache'], ARRAY['Beta-blockers', 'MAOIs', 'Tricyclic antidepressants'], 'C', NULL, TRUE),

(7, 'Sertraline', 'Sertraline Hydrochloride', ARRAY['Zoloft'], 'SSRI Antidepressant', ARRAY['Tablet', 'Oral solution'], ARRAY['25mg', '50mg', '100mg'], 'Oral', 'Used for depression, anxiety, PTSD, OCD', 'Black box warning for suicidal thoughts in young adults', ARRAY['MAOIs within 14 days', 'Pimozide use', 'Disulfiram use with oral solution'], ARRAY['Nausea', 'Insomnia', 'Diarrhea', 'Sexual dysfunction'], ARRAY['MAOIs', 'Pimozide', 'Warfarin', 'NSAIDs'], 'C', NULL, TRUE),

(8, 'Levothyroxine', 'Levothyroxine Sodium', ARRAY['Synthroid', 'Levoxyl', 'Tirosint'], 'Thyroid Hormone', ARRAY['Tablet', 'Capsule', 'Injection'], ARRAY['25mcg', '50mcg', '75mcg', '100mcg', '125mcg', '150mcg'], 'Oral', 'Used for hypothyroidism', 'Overreplacement can cause hyperthyroidism symptoms', ARRAY['Untreated adrenal insufficiency', 'Acute MI', 'Thyrotoxicosis'], ARRAY['Weight loss', 'Tremor', 'Headache', 'Insomnia'], ARRAY['Calcium supplements', 'Iron supplements', 'Antacids'], 'A', NULL, TRUE),

(9, 'Hydrochlorothiazide', 'Hydrochlorothiazide', ARRAY['Microzide', 'HydroDIURIL'], 'Thiazide Diuretic', ARRAY['Tablet', 'Capsule'], ARRAY['12.5mg', '25mg', '50mg'], 'Oral', 'Used for hypertension and edema', 'Monitor electrolytes. May worsen gout.', ARRAY['Anuria', 'Sulfonamide allergy'], ARRAY['Hypokalemia', 'Hyperuricemia', 'Photosensitivity', 'Dizziness'], ARRAY['Lithium', 'Digoxin', 'NSAIDs'], 'B', NULL, TRUE),

(10, 'Clopidogrel', 'Clopidogrel Bisulfate', ARRAY['Plavix'], 'Antiplatelet Agent', ARRAY['Tablet'], ARRAY['75mg', '300mg'], 'Oral', 'Used for acute coronary syndrome and stroke prevention', 'Increased bleeding risk. Discontinue 5-7 days before surgery.', ARRAY['Active bleeding', 'Severe hepatic impairment'], ARRAY['Bleeding', 'Bruising', 'Rash', 'Diarrhea'], ARRAY['Omeprazole', 'Aspirin', 'Warfarin'], 'B', NULL, TRUE),

(11, 'Sumatriptan', 'Sumatriptan Succinate', ARRAY['Imitrex'], 'Triptan', ARRAY['Tablet', 'Nasal spray', 'Injection'], ARRAY['25mg', '50mg', '100mg', '6mg/0.5ml'], 'Oral/Nasal/Subcutaneous', 'Used for acute migraine treatment', 'Cardiovascular risk. Not for hemiplegic migraine.', ARRAY['History of stroke/TIA', 'CAD', 'Uncontrolled hypertension', 'Hemiplegic migraine'], ARRAY['Injection site reactions', 'Tingling', 'Chest tightness', 'Drowsiness'], ARRAY['MAOIs', 'Ergotamine', 'Other triptans', 'SSRIs'], 'C', NULL, TRUE),

(12, 'Prednisone', 'Prednisone', ARRAY['Deltasone', 'Rayos'], 'Corticosteroid', ARRAY['Tablet', 'Oral solution'], ARRAY['1mg', '2.5mg', '5mg', '10mg', '20mg', '50mg'], 'Oral', 'Used for inflammation, autoimmune conditions, allergies', 'Taper gradually after prolonged use. Many systemic effects.', ARRAY['Systemic fungal infections', 'Live vaccines during therapy'], ARRAY['Weight gain', 'Mood changes', 'Insomnia', 'Hyperglycemia'], ARRAY['NSAIDs', 'Warfarin', 'Diabetes medications'], 'C', NULL, TRUE),

(13, 'Gabapentin', 'Gabapentin', ARRAY['Neurontin', 'Gralise'], 'Anticonvulsant/Analgesic', ARRAY['Capsule', 'Tablet', 'Oral solution'], ARRAY['100mg', '300mg', '400mg', '600mg', '800mg'], 'Oral', 'Used for seizures, neuropathic pain, and restless legs', 'May cause CNS depression. Taper when discontinuing.', ARRAY['Hypersensitivity'], ARRAY['Dizziness', 'Drowsiness', 'Peripheral edema', 'Ataxia'], ARRAY['Antacids', 'Opioids', 'CNS depressants'], 'C', NULL, TRUE),

(14, 'Acetaminophen', 'Acetaminophen', ARRAY['Tylenol', 'Panadol'], 'Analgesic/Antipyretic', ARRAY['Tablet', 'Capsule', 'Liquid', 'Suppository'], ARRAY['325mg', '500mg', '650mg', '1000mg'], 'Oral/Rectal', 'Used for pain and fever', 'Hepatotoxicity risk with overdose or alcohol use', ARRAY['Severe hepatic impairment'], ARRAY['Rare at therapeutic doses'], ARRAY['Warfarin', 'Alcohol'], 'B', NULL, FALSE),

(15, 'Ibuprofen', 'Ibuprofen', ARRAY['Advil', 'Motrin'], 'NSAID', ARRAY['Tablet', 'Capsule', 'Liquid'], ARRAY['200mg', '400mg', '600mg', '800mg'], 'Oral', 'Used for pain, inflammation, and fever', 'GI bleeding risk. Cardiovascular risk with long-term use.', ARRAY['Active GI bleeding', 'Severe renal impairment', 'Third trimester pregnancy', 'Post-CABG surgery'], ARRAY['GI upset', 'Heartburn', 'Dizziness', 'Rash'], ARRAY['Aspirin', 'Warfarin', 'ACE inhibitors', 'Lithium'], 'C/D', NULL, FALSE),

(16, 'Amoxicillin', 'Amoxicillin', ARRAY['Amoxil', 'Trimox'], 'Penicillin Antibiotic', ARRAY['Capsule', 'Tablet', 'Oral suspension'], ARRAY['250mg', '500mg', '875mg'], 'Oral', 'Used for bacterial infections', 'Risk of allergic reactions. C. diff associated diarrhea.', ARRAY['Penicillin allergy', 'History of amoxicillin-related cholestatic jaundice'], ARRAY['Diarrhea', 'Nausea', 'Rash', 'Vomiting'], ARRAY['Warfarin', 'Methotrexate'], 'B', NULL, TRUE),

(17, 'Azithromycin', 'Azithromycin', ARRAY['Zithromax', 'Z-Pak'], 'Macrolide Antibiotic', ARRAY['Tablet', 'Oral suspension', 'IV'], ARRAY['250mg', '500mg', '100mg/5ml', '200mg/5ml'], 'Oral/IV', 'Used for bacterial infections', 'QT prolongation risk. Hepatotoxicity risk.', ARRAY['History of cholestatic jaundice with azithromycin', 'Hypersensitivity to macrolides'], ARRAY['Diarrhea', 'Nausea', 'Abdominal pain', 'Headache'], ARRAY['Warfarin', 'Antacids', 'QT-prolonging drugs'], 'B', NULL, TRUE),

(18, 'Fluticasone', 'Fluticasone Propionate', ARRAY['Flonase', 'Flovent'], 'Corticosteroid', ARRAY['Nasal spray', 'Inhaler'], ARRAY['50mcg/spray', '44mcg', '110mcg', '220mcg'], 'Nasal/Inhalation', 'Used for allergic rhinitis and asthma', 'Adrenal suppression with high doses', ARRAY['Untreated fungal, bacterial, or viral infections'], ARRAY['Headache', 'Nasal irritation', 'Nosebleed', 'Throat irritation'], ARRAY['Ritonavir', 'Ketoconazole'], 'C', NULL, TRUE),

(19, 'Warfarin', 'Warfarin Sodium', ARRAY['Coumadin', 'Jantoven'], 'Anticoagulant', ARRAY['Tablet'], ARRAY['1mg', '2mg', '2.5mg', '3mg', '4mg', '5mg', '6mg', '7.5mg', '10mg'], 'Oral', 'Used for thromboembolic disorders', 'Bleeding risk. Requires regular INR monitoring.', ARRAY['Active bleeding', 'Pregnancy', 'Severe hepatic disease'], ARRAY['Bleeding', 'Bruising', 'Purple toe syndrome'], ARRAY['NSAIDs', 'Aspirin', 'Antibiotics', 'Many drug interactions'], 'X', NULL, TRUE),

(20, 'Insulin Glargine', 'Insulin Glargine', ARRAY['Lantus', 'Basaglar', 'Toujeo'], 'Long-acting Insulin', ARRAY['Injection'], ARRAY['100 units/ml', '300 units/ml'], 'Subcutaneous', 'Used for diabetes mellitus', 'Hypoglycemia risk. Do not dilute or mix with other insulins.', ARRAY['Hypoglycemia', 'Hypersensitivity'], ARRAY['Hypoglycemia', 'Weight gain', 'Injection site reactions', 'Lipodystrophy'], ARRAY['Beta-blockers', 'Thiazolidinediones', 'ACE inhibitors'], 'B', NULL, TRUE);

-- Reset sequence
SELECT setval('medications_id_seq', 20, true);

-- =====================================================
-- DRUG INTERACTIONS
-- =====================================================

INSERT INTO drug_interactions (medication_1_id, medication_2_id, severity, description, clinical_effects, management) VALUES
(10, 5, 'major', 'Clopidogrel + Omeprazole interaction', 'Omeprazole may reduce the antiplatelet effect of clopidogrel by inhibiting CYP2C19', 'Consider using pantoprazole or H2 blockers instead'),
(19, 15, 'major', 'Warfarin + Ibuprofen interaction', 'NSAIDs increase bleeding risk and may increase INR', 'Avoid combination if possible. If necessary, monitor INR closely and watch for bleeding'),
(2, 15, 'moderate', 'Lisinopril + Ibuprofen interaction', 'NSAIDs may reduce antihypertensive effect and increase renal impairment risk', 'Monitor blood pressure and renal function'),
(3, 13, 'moderate', 'Atorvastatin + Gabapentin', 'No significant interaction, but monitor for myopathy symptoms', 'Safe to use together with monitoring'),
(7, 11, 'moderate', 'Sertraline + Sumatriptan interaction', 'Risk of serotonin syndrome', 'Use with caution. Monitor for symptoms of serotonin syndrome'),
(19, 14, 'minor', 'Warfarin + Acetaminophen interaction', 'High doses of acetaminophen may increase INR', 'Limit acetaminophen use. Monitor INR if using regularly'),
(1, 20, 'moderate', 'Metformin + Insulin interaction', 'Additive hypoglycemic effect', 'Monitor blood glucose closely. May need dose adjustments'),
(6, 2, 'minor', 'Albuterol + Lisinopril', 'No significant clinical interaction', 'Safe to use together');

-- =====================================================
-- PRESCRIPTIONS (12 prescriptions)
-- =====================================================

INSERT INTO prescriptions (id, patient_id, prescriber_id, appointment_id, status, diagnosis, notes, pharmacy_name, pharmacy_address, pharmacy_phone, valid_from, valid_until) VALUES

(1, 6, 1, 1, 'dispensed', 'Type 2 Diabetes Mellitus', 'Continue current regimen. Good glucose control.', 'CVS Pharmacy', '123 Main St, Boston, MA 02105', '+1-555-2001', '2025-11-15', '2026-05-15'),

(2, 6, 1, 1, 'dispensed', 'Essential Hypertension', 'Blood pressure well controlled', 'CVS Pharmacy', '123 Main St, Boston, MA 02105', '+1-555-2001', '2025-11-15', '2026-05-15'),

(3, 7, 1, 2, 'approved', 'Asthma - Mild Persistent', 'Use rescue inhaler as needed', 'Walgreens', '456 Center St, Cambridge, MA 02140', '+1-555-2002', '2025-11-15', '2026-05-15'),

(4, 10, 2, 3, 'dispensed', 'Coronary Artery Disease, Type 2 Diabetes, Hypertension', 'Post-stent medications. Compliance critical.', 'Walgreens', '567 West Blvd, Newton, MA 02458', '+1-555-2003', '2025-11-14', '2026-05-14'),

(5, 8, 1, 4, 'approved', 'Hyperlipidemia', 'Start statin therapy. Diet and exercise counseling provided.', 'Rite Aid', '789 North Ave, Somerville, MA 02143', '+1-555-2004', '2025-11-16', '2026-05-16'),

(6, 12, 3, 5, 'dispensed', 'Allergic Contact Dermatitis', 'Apply to affected areas twice daily for 2 weeks', 'Walgreens', '234 Park Ave, Medford, MA 02155', '+1-555-2005', '2025-11-17', '2025-12-17'),

(7, 9, 1, NULL, 'pending_approval', 'Generalized Anxiety Disorder', 'Patient reports increased anxiety. Consider dose increase.', 'CVS Pharmacy', '321 East St, Brookline, MA 02445', '+1-555-2006', '2025-11-20', '2026-05-20'),

(8, 11, 1, NULL, 'draft', 'Hypothyroidism', 'TSH slightly elevated. Consider dose adjustment.', 'CVS Pharmacy', '890 South St, Quincy, MA 02169', '+1-555-2007', '2025-11-21', '2026-05-21'),

(9, 13, 1, NULL, 'approved', 'Essential Hypertension, Osteoarthritis', 'Continue current medications', 'Rite Aid', '567 River Rd, Malden, MA 02148', '+1-555-2008', '2025-11-18', '2026-05-18'),

(10, 14, 1, NULL, 'pending_approval', 'Gastroesophageal Reflux Disease', 'Symptoms worsening. Increase PPI dose.', 'CVS Pharmacy', '890 Hill St, Waltham, MA 02451', '+1-555-2009', '2025-11-20', '2026-05-20'),

(11, 10, 2, 14, 'approved', 'Acute Chest Pain - Rule out MI', 'Continue antiplatelet therapy. Follow-up in 1 week.', 'Walgreens', '567 West Blvd, Newton, MA 02458', '+1-555-2003', '2025-11-20', '2025-12-20'),

(12, 15, 3, NULL, 'cancelled', 'Acne Vulgaris', 'Patient cancelled appointment', NULL, NULL, NULL, '2025-11-18', '2026-05-18');

-- Reset sequence
SELECT setval('prescriptions_id_seq', 12, true);

-- =====================================================
-- PRESCRIPTION ITEMS
-- =====================================================

INSERT INTO prescription_items (prescription_id, medication_id, dosage, frequency, duration, quantity, refills_allowed, refills_remaining, instructions, take_with_food) VALUES

-- Prescription 1 (Diabetes - Patient 6)
(1, 1, '500mg', 'Twice daily', '6 months', 180, 3, 3, 'Take with meals to reduce GI upset', TRUE),

-- Prescription 2 (Hypertension - Patient 6)
(2, 2, '10mg', 'Once daily', '6 months', 90, 3, 3, 'Take in the morning. Monitor for dizziness.', FALSE),

-- Prescription 3 (Asthma - Patient 7)
(3, 6, '90mcg', '2 puffs every 4-6 hours as needed', '6 months', 1, 5, 5, 'Shake well before use. Rinse mouth after use.', FALSE),

-- Prescription 4 (CAD + Diabetes + HTN - Patient 10)
(4, 10, '75mg', 'Once daily', '6 months', 90, 3, 3, 'Do not stop without consulting doctor', FALSE),
(4, 1, '1000mg', 'Twice daily', '6 months', 180, 3, 3, 'Take with meals', TRUE),
(4, 4, '5mg', 'Once daily', '6 months', 90, 3, 3, 'Take at bedtime', FALSE),
(4, 3, '40mg', 'Once daily', '6 months', 90, 3, 3, 'Take at bedtime', FALSE),

-- Prescription 5 (Hyperlipidemia - Patient 8)
(5, 3, '20mg', 'Once daily', '6 months', 90, 3, 3, 'Take at bedtime. Avoid grapefruit.', FALSE),

-- Prescription 6 (Dermatitis - Patient 12)
(6, 12, '0.1% cream', 'Apply twice daily', '2 weeks', 1, 0, 0, 'Apply thin layer to affected areas. Do not use on face.', FALSE),

-- Prescription 7 (Anxiety - Patient 9)
(7, 7, '100mg', 'Once daily', '6 months', 90, 3, 3, 'Take in the morning. May take 4-6 weeks for full effect.', FALSE),
(7, 11, '50mg', 'As needed for migraine', '6 months', 9, 2, 2, 'Take at first sign of migraine. Max 200mg/day.', FALSE),

-- Prescription 8 (Hypothyroidism - Patient 11)
(8, 8, '88mcg', 'Once daily', '6 months', 90, 3, 3, 'Take on empty stomach, 30-60 min before breakfast', FALSE),

-- Prescription 9 (HTN + Arthritis - Patient 13)
(9, 9, '25mg', 'Once daily', '6 months', 90, 3, 3, 'Take in the morning', FALSE),
(9, 14, '650mg', 'Every 6 hours as needed', '1 month', 120, 2, 2, 'Do not exceed 3000mg/day', FALSE),

-- Prescription 10 (GERD - Patient 14)
(10, 5, '40mg', 'Once daily', '3 months', 90, 1, 1, 'Take 30 minutes before breakfast', FALSE),

-- Prescription 11 (Chest pain follow-up - Patient 10)
(11, 10, '75mg', 'Once daily', '1 month', 30, 0, 0, 'Continue taking. Critical for stent protection.', FALSE);

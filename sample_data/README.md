# MediSense-AI Sample Data

This directory contains comprehensive sample data for deploying and testing the MediSense-AI Clinical AI Multi-Agent Application.

## Directory Structure

```
sample_data/
├── sql/                    # SQL scripts for database setup
│   ├── 000_init.sql       # Master initialization script
│   ├── 001_schema.sql     # Database schema (tables, indexes, triggers)
│   ├── 002_users_data.sql # Users, clinicians, patients data
│   ├── 003_appointments_data.sql
│   ├── 004_medications_prescriptions.sql
│   ├── 005_documents_images_payments.sql
│   └── 006_audit_chat_data.sql
├── images/                 # Sample medical images for AI analysis
│   ├── README.md          # Image documentation
│   ├── skin_rash_001.svg  # Dermatology sample
│   └── chest_xray_001.svg # Radiology sample
├── documents/             # Sample medical documents (PDFs, reports)
├── vectors/               # Vector embeddings for RAG
└── README.md              # This file
```

## Quick Start

### Initialize Database with Sample Data

```bash
# Option 1: Using the master init script
cd sample_data/sql
psql -U medisense -d medisense_db -f 000_init.sql

# Option 2: Using Docker
docker-compose exec db psql -U medisense -d medisense_db -f /sample_data/sql/000_init.sql

# Option 3: Individual files
psql -U medisense -d medisense_db -f 001_schema.sql
psql -U medisense -d medisense_db -f 002_users_data.sql
# ... continue with remaining files
```

## Database Schema Overview

### Entity Relationship Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     USERS       │     │  APPOINTMENTS   │     │  PRESCRIPTIONS  │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │◄────│ patient_id (FK) │     │ id (PK)         │
│ email           │◄────│ clinician_id(FK)│◄────│ patient_id (FK) │
│ role            │     │ status          │     │ prescriber_id   │
│ full_name       │     │ scheduled_start │◄────│ appointment_id  │
└────────┬────────┘     └─────────────────┘     └────────┬────────┘
         │                                               │
         │                                               │
    ┌────┴────┐                                    ┌─────┴─────┐
    │         │                                    │           │
┌───┴───┐ ┌───┴───┐                          ┌────┴────┐ ┌────┴────┐
│CLINICIAN│ │PATIENT│                          │PRESCRIP.│ │MEDICATIONS│
│PROFILES │ │PROFILES│                          │  ITEMS  │ │           │
└─────────┘ └─────────┘                          └─────────┘ └───────────┘
```

### Table Summary

| Table | Records | Description |
|-------|---------|-------------|
| `users` | 15 | All users (patients, clinicians, admins) |
| `clinician_profiles` | 3 | Extended clinician information |
| `patient_profiles` | 10 | Patient health information |
| `clinician_availability` | 15 | Scheduling slots |
| `appointments` | 15 | Medical appointments |
| `medications` | 20 | Drug catalog |
| `prescriptions` | 12 | E-prescriptions |
| `prescription_items` | 16 | Prescription line items |
| `drug_interactions` | 8 | Drug-drug interactions |
| `medical_documents` | 12 | Uploaded documents |
| `image_analyses` | 10 | AI image analysis results |
| `payments` | 12 | Payment transactions |
| `notifications` | 15 | User notifications |
| `audit_logs` | 20 | Compliance audit trail |
| `guardrail_violations` | 8 | PHI/safety violations |
| `chat_sessions` | 10 | Conversation sessions |
| `chat_messages` | 15 | Individual messages |
| `vector_documents` | 10 | RAG knowledge base |

## Sample Users

### Test Credentials

| Role | Email | Password | Notes |
|------|-------|----------|-------|
| Admin | admin@medisense.com | `password123` | Full system access |
| Clinician | dr.sarah.johnson@medisense.com | `password123` | Internal Medicine |
| Clinician | dr.james.wilson@medisense.com | `password123` | Cardiology |
| Clinician | dr.priya.patel@medisense.com | `password123` | Dermatology |
| Patient | john.doe@email.com | `password123` | Diabetes, Hypertension |
| Patient | jane.smith@email.com | `password123` | Asthma |
| Patient | michael.wilson@email.com | `password123` | CAD, Diabetes |

**Note**: All passwords are hashed with bcrypt. The hash in the SQL represents `password123`.

## Data Relationships

### User Hierarchy
- **Users** (base table) → **Clinician Profiles** (1:1) OR **Patient Profiles** (1:1)
- Patients reference their **Primary Care Physician** (self-referencing FK)

### Appointment Flow
- **Appointment** links **Patient** ↔ **Clinician**
- Appointments can have:
  - Associated **Prescriptions**
  - Associated **Medical Documents**
  - Associated **Image Analyses**
  - Associated **Payments**

### Prescription Chain
- **Prescription** → **Prescription Items** → **Medications**
- **Drug Interactions** link pairs of **Medications**

### Audit Trail
- **Audit Logs** track all system actions
- **Guardrail Violations** reference **Audit Logs**
- **Chat Sessions** → **Chat Messages**

## Sample Data Scenarios

### 1. Diabetes Management (Patient: John Doe)
- Regular HbA1c monitoring
- Metformin prescription
- Diabetic foot wound image analysis
- Cardiology referral

### 2. Asthma Follow-up (Patient: Jane Smith)
- Pulmonary function test
- Albuterol prescription
- RAG query about asthma management

### 3. Cardiac Evaluation (Patient: Michael Wilson)
- Emergency chest pain evaluation
- Echocardiogram and cardiac enzymes
- Multiple cardiac medications
- Discharge summary

### 4. Skin Condition (Patient: David Lee)
- Image upload for rash analysis
- AI prediction: Contact dermatitis
- Dermatology consultation
- Topical treatment prescription

## Extending Sample Data

### Adding New Users
```sql
INSERT INTO users (email, hashed_password, full_name, role, status)
VALUES ('new.user@email.com', '$2b$12$...', 'New User', 'patient', 'active');
```

### Adding New Medications
```sql
INSERT INTO medications (name, generic_name, drug_class, dosage_forms, strengths)
VALUES ('NewDrug', 'Generic Name', 'Drug Class', ARRAY['Tablet'], ARRAY['10mg', '20mg']);
```

## Privacy & Compliance

This sample data is **synthetic** and does not contain any real:
- Patient information
- Protected Health Information (PHI)
- Personally Identifiable Information (PII)
- Medical images from real patients

All data is generated for demonstration and testing purposes only.

## Troubleshooting

### Common Issues

1. **Sequence out of sync**
   ```sql
   SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
   ```

2. **Foreign key violations**
   - Run SQL files in order (000 → 006)
   - Use the master init script

3. **Type errors**
   - Ensure PostgreSQL extensions are enabled
   - Run schema file first

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-21 | Initial sample data release |

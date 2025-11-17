# MediSense-AI Guardrails Documentation

## Overview

The Guardrails system enforces safety, privacy, and compliance policies across all agent interactions in MediSense-AI.

## Policy Framework

### Policy Categories

1. **PHI/PII Redaction** (Critical)
2. **Unsafe Content Filtering** (High)
3. **Medical Advice Disclaimers** (Medium)
4. **Prescription Validation** (High)

## PHI/PII Protection

### Automatic Redaction Patterns

The system automatically detects and redacts:

| Type | Pattern | Example | Redacted As |
|------|---------|---------|-------------|
| SSN | `\d{3}-\d{2}-\d{4}` | 123-45-6789 | [REDACTED_SSN] |
| Phone | `\d{3}[-.]?\d{3}[-.]?\d{4}` | 555-123-4567 | [REDACTED_PHONE] |
| Email | `[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}` | patient@example.com | [REDACTED_EMAIL] |
| DOB | `\d{1,2}/\d{1,2}/\d{2,4}` | 01/15/1980 | [REDACTED_DATE_OF_BIRTH] |
| MRN | `MRN[-:]?\s*\d+` | MRN: 123456 | [REDACTED_MRN] |

### Implementation

```python
from app.core.security import redact_phi

# Automatic redaction
safe_text = redact_phi(original_text)

# Dict redaction
safe_data = redact_phi_dict(data_dict)
```

## Unsafe Content Detection

### Blocked Patterns

- Self-harm references
- Illegal drug advice
- End-of-life discussions (without proper context)
- Unverified medical procedures

### Action on Detection

```
1. Block content immediately
2. Log violation
3. Return safe error message
4. Notify security team (if critical)
```

## Medical Advice Disclaimers

### Required Disclaimers

Any medical advice must include:

> "This information is not a substitute for professional medical advice. Always consult with a qualified healthcare provider for medical decisions."

### Automatic Insertion

The system automatically appends disclaimers when:
- Medical advice keywords detected
- Diagnosis or treatment recommendations
- Medication suggestions

## Prescription Validation

### Validation Checks

1. **Drug Interaction Check**
   - Cross-reference with current medications
   - Flag known dangerous combinations

2. **Contraindication Check**
   - Check against patient allergies
   - Verify category-based restrictions

3. **Dosage Validation**
   - Ensure dosage within safe ranges
   - Age-appropriate dosing

4. **Provenance Tracking**
   - Link to source clinical data
   - Record prescriber information

## Guardrail Enforcement Pipeline

```
User Input → Agent Processing → Guardrail Check → Output
                                      ↓
                             [Pass/Redact/Block]
                                      ↓
                              Audit Logging
```

### Enforcement Levels

| Level | Action | Use Case |
|-------|--------|----------|
| **Log** | Record violation, allow content | Low-severity issues |
| **Redact** | Remove sensitive data, allow | PHI/PII detection |
| **Block** | Prevent content delivery | Critical safety violations |
| **Alert** | Block + notify security team | Malicious activity |

## Configuration

### Guardrail Policies (YAML)

```yaml
policies:
  phi_redaction:
    enabled: true
    severity: critical
    action: redact

  unsafe_content:
    enabled: true
    severity: high
    action: block

  medical_disclaimer:
    enabled: true
    severity: medium
    action: append_disclaimer

  prescription_validation:
    enabled: true
    severity: high
    action: validate_and_warn
```

### Environment Variables

```bash
GUARDRAILS_ENABLED=true
PHI_REDACTION_ENABLED=true
GUARDRAILS_POLICY_FILE=/app/config/guardrail_policies.yaml
```

## Violation Tracking

All violations are logged to the database:

```sql
CREATE TABLE guardrail_violations (
    id SERIAL PRIMARY KEY,
    policy VARCHAR NOT NULL,
    violation_type VARCHAR NOT NULL,
    severity VARCHAR NOT NULL,
    user_id INTEGER,
    session_id VARCHAR,
    context JSONB,
    action_taken VARCHAR NOT NULL,
    resolved BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

## Monitoring & Alerts

### Metrics Tracked

- Violations per hour
- Redaction rate
- Blocked content count
- False positive rate (from manual review)

### Alerting Thresholds

- **Critical**: Block rate > 5% → Immediate alert
- **High**: Redaction rate > 20% → Alert within 1 hour
- **Medium**: Disclaimer insertion rate anomaly → Daily report

## Testing Guardrails

### Test Cases

```python
# Test PHI redaction
text = "Patient SSN: 123-45-6789"
result = guardrail_agent.run({
    "query": "validate",
    "context": {"content": text}
})
assert "[REDACTED_SSN]" in result.response["redacted_content"]

# Test unsafe content blocking
text = "Instructions for self-harm"
result = guardrail_agent.run({
    "query": "validate",
    "context": {"content": text}
})
assert result.response["should_block"] == True
```

## Compliance

### HIPAA Alignment

- **Privacy Rule**: PHI redaction ensures compliance
- **Security Rule**: Encrypted storage and transmission
- **Breach Notification**: Automatic logging for audits

### Audit Requirements

Every guardrail action is logged with:
- Timestamp
- User ID
- Content hash (not actual content)
- Policy violated
- Action taken
- Resolution status

## Best Practices

1. **Enable all guardrails in production**
2. **Regularly review violation logs**
3. **Update redaction patterns based on new PHI types**
4. **Test guardrails with real-world data**
5. **Monitor false positive rates**
6. **Train staff on guardrail policies**

## False Positive Handling

When guardrails incorrectly flag content:

1. Log as potential false positive
2. Allow manual override (with justification)
3. Update patterns to reduce recurrence
4. Track override rate

## Emergency Override

For emergencies (e.g., life-threatening situations):

```python
# Requires admin role
result = guardrail_agent.run({
    "query": "validate",
    "context": {
        "content": sensitive_content,
        "emergency_override": True,
        "override_reason": "Life-threatening emergency"
    }
})
```

Override requires:
- Admin role
- Justification
- Logged for post-incident review

## Future Enhancements

1. **ML-based PHI detection** (beyond regex)
2. **Context-aware disclaimers**
3. **Multi-language support**
4. **Real-time policy updates** (without deployment)
5. **Advanced drug interaction database**

---

**Version**: 1.0.0
**Last Updated**: 2025-01-17

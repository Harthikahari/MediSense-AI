"""
Audit log model for immutable tracking of clinical decisions and data access.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.db.base import Base


class AuditLog(Base):
    """Audit log model for compliance and traceability."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Event identification
    event_type = Column(String, index=True, nullable=False)  # agent_action, llm_call, data_access, etc.
    event_id = Column(String, index=True, unique=True, nullable=False)  # Unique identifier for this event

    # User and session tracking
    user_id = Column(Integer, index=True, nullable=True)
    session_id = Column(String, index=True, nullable=True)

    # Agent/Action tracking
    agent_name = Column(String, nullable=True)
    action = Column(String, nullable=True)

    # Resource tracking (for data access events)
    resource_type = Column(String, nullable=True)
    resource_id = Column(String, nullable=True)

    # Event data (stored as JSON)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)

    # Status
    success = Column(String, default="true")
    error_message = Column(Text, nullable=True)

    # Provenance - track the chain of reasoning
    provenance = Column(JSON, nullable=True)  # Links to source documents, previous decisions, etc.

    # Timestamps (immutable - never updated)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return (
            f"<AuditLog(id={self.id}, "
            f"event_type={self.event_type}, "
            f"user_id={self.user_id}, "
            f"timestamp={self.timestamp})>"
        )


class GuardrailViolation(Base):
    """Guardrail violation tracking for policy enforcement."""

    __tablename__ = "guardrail_violations"

    id = Column(Integer, primary_key=True, index=True)

    # Violation identification
    policy = Column(String, nullable=False)
    violation_type = Column(String, nullable=False)
    severity = Column(String, default="medium")  # low, medium, high, critical

    # User and session tracking
    user_id = Column(Integer, index=True, nullable=True)
    session_id = Column(String, index=True, nullable=True)

    # Violation context
    context = Column(JSON, nullable=True)
    action_taken = Column(String, nullable=False)  # blocked, redacted, logged, etc.

    # Resolution
    resolved = Column(String, default="false")
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)

    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return (
            f"<GuardrailViolation(id={self.id}, "
            f"policy={self.policy}, "
            f"violation_type={self.violation_type}, "
            f"severity={self.severity})>"
        )

"""
Appointment model for scheduling and booking management.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class AppointmentStatus(str, enum.Enum):
    """Appointment status enumeration."""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentType(str, enum.Enum):
    """Appointment type enumeration."""
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"
    ROUTINE_CHECKUP = "routine_checkup"


class Appointment(Base):
    """Appointment model."""

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    # Relationships
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    clinician_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Appointment details
    appointment_type = Column(Enum(AppointmentType), default=AppointmentType.CONSULTATION)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)

    # Scheduling
    scheduled_start = Column(DateTime(timezone=True), nullable=False)
    scheduled_end = Column(DateTime(timezone=True), nullable=False)
    actual_start = Column(DateTime(timezone=True), nullable=True)
    actual_end = Column(DateTime(timezone=True), nullable=True)

    # Clinical information
    chief_complaint = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)

    # Payment
    payment_status = Column(String, default="pending")
    payment_amount = Column(Float, nullable=True)
    payment_id = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancellation_reason = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f"<Appointment(id={self.id}, "
            f"patient_id={self.patient_id}, "
            f"clinician_id={self.clinician_id}, "
            f"status={self.status})>"
        )

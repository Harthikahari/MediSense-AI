"""
CRUD operations for database models.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from app.models.user import User, UserRoleEnum
from app.models.appointment import Appointment, AppointmentStatus
from app.models.audit import AuditLog, GuardrailViolation
from app.core.security import hash_password


# ============================================================================
# User CRUD
# ============================================================================

def create_user(db: Session, email: str, password: str, full_name: str, role: str = "patient") -> User:
    """Create a new user."""
    hashed_password = hash_password(password)
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=UserRoleEnum(role)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()


def get_clinicians(db: Session) -> List[User]:
    """Get all clinicians."""
    return db.query(User).filter(User.role == UserRoleEnum.CLINICIAN).all()


# ============================================================================
# Appointment CRUD
# ============================================================================

def create_appointment(
    db: Session,
    patient_id: int,
    clinician_id: int,
    appointment_type: str,
    scheduled_start: datetime,
    scheduled_end: datetime,
    chief_complaint: Optional[str] = None
) -> Appointment:
    """Create a new appointment."""
    db_appointment = Appointment(
        patient_id=patient_id,
        clinician_id=clinician_id,
        appointment_type=appointment_type,
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_end,
        chief_complaint=chief_complaint
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointment_by_id(db: Session, appointment_id: int) -> Optional[Appointment]:
    """Get appointment by ID."""
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_appointments_by_patient(db: Session, patient_id: int) -> List[Appointment]:
    """Get all appointments for a patient."""
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()


def get_appointments_by_clinician(
    db: Session,
    clinician_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Appointment]:
    """Get all appointments for a clinician, optionally filtered by date range."""
    query = db.query(Appointment).filter(Appointment.clinician_id == clinician_id)

    if start_date and end_date:
        query = query.filter(
            and_(
                Appointment.scheduled_start >= start_date,
                Appointment.scheduled_end <= end_date
            )
        )

    return query.all()


def update_appointment_status(
    db: Session,
    appointment_id: int,
    status: str
) -> Optional[Appointment]:
    """Update appointment status."""
    appointment = get_appointment_by_id(db, appointment_id)
    if appointment:
        appointment.status = AppointmentStatus(status)
        if status == "cancelled":
            appointment.cancelled_at = datetime.utcnow()
        db.commit()
        db.refresh(appointment)
    return appointment


def check_clinician_availability(
    db: Session,
    clinician_id: int,
    start_time: datetime,
    end_time: datetime
) -> bool:
    """Check if clinician is available for the given time slot."""
    conflicting_appointments = db.query(Appointment).filter(
        and_(
            Appointment.clinician_id == clinician_id,
            Appointment.status.in_([
                AppointmentStatus.SCHEDULED,
                AppointmentStatus.CONFIRMED,
                AppointmentStatus.IN_PROGRESS
            ]),
            Appointment.scheduled_start < end_time,
            Appointment.scheduled_end > start_time
        )
    ).count()

    return conflicting_appointments == 0


# ============================================================================
# Audit CRUD
# ============================================================================

def create_audit_log(
    db: Session,
    event_type: str,
    event_id: str,
    user_id: Optional[int] = None,
    session_id: Optional[str] = None,
    agent_name: Optional[str] = None,
    action: Optional[str] = None,
    input_data: Optional[dict] = None,
    output_data: Optional[dict] = None,
    metadata: Optional[dict] = None,
    success: bool = True,
    provenance: Optional[dict] = None
) -> AuditLog:
    """Create an audit log entry."""
    audit_log = AuditLog(
        event_type=event_type,
        event_id=event_id,
        user_id=user_id,
        session_id=session_id,
        agent_name=agent_name,
        action=action,
        input_data=input_data,
        output_data=output_data,
        metadata=metadata,
        success=str(success),
        provenance=provenance
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log


def get_audit_logs(
    db: Session,
    user_id: Optional[int] = None,
    session_id: Optional[str] = None,
    event_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[AuditLog]:
    """Get audit logs with optional filters."""
    query = db.query(AuditLog)

    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if session_id:
        query = query.filter(AuditLog.session_id == session_id)
    if event_type:
        query = query.filter(AuditLog.event_type == event_type)

    return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()


def create_guardrail_violation(
    db: Session,
    policy: str,
    violation_type: str,
    user_id: Optional[int] = None,
    session_id: Optional[str] = None,
    context: Optional[dict] = None,
    action_taken: str = "logged",
    severity: str = "medium"
) -> GuardrailViolation:
    """Create a guardrail violation record."""
    violation = GuardrailViolation(
        policy=policy,
        violation_type=violation_type,
        severity=severity,
        user_id=user_id,
        session_id=session_id,
        context=context,
        action_taken=action_taken
    )
    db.add(violation)
    db.commit()
    db.refresh(violation)
    return violation

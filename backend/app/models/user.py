"""
User model for authentication and authorization.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class UserRoleEnum(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    CLINICIAN = "clinician"
    PATIENT = "patient"
    STAFF = "staff"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.PATIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    phone_number = Column(String, nullable=True)

    # Clinician-specific fields
    license_number = Column(String, nullable=True)
    specialization = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

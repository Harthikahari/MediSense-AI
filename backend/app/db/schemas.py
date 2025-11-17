"""
Pydantic schemas for request/response validation.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# User Schemas
# ============================================================================

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: str
    role: str = "patient"
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str


class UserUpdate(BaseModel):
    """Schema for user updates."""
    full_name: Optional[str] = None
    phone_number: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user responses."""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Authentication Schemas
# ============================================================================

class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema."""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None


# ============================================================================
# Appointment Schemas
# ============================================================================

class AppointmentBase(BaseModel):
    """Base appointment schema."""
    clinician_id: int
    appointment_type: str = "consultation"
    scheduled_start: datetime
    scheduled_end: datetime
    chief_complaint: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    """Schema for appointment creation."""
    pass


class AppointmentUpdate(BaseModel):
    """Schema for appointment updates."""
    status: Optional[str] = None
    notes: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    """Schema for appointment responses."""
    id: int
    patient_id: int
    status: str
    payment_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Agent Schemas
# ============================================================================

class AgentRequest(BaseModel):
    """Generic agent request schema."""
    query: str
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None


class AgentResponse(BaseModel):
    """Generic agent response schema."""
    agent_name: str
    response: str
    confidence: float = Field(ge=0.0, le=1.0)
    provenance: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class RoutingResponse(BaseModel):
    """Routing agent response schema."""
    target_agent: str
    confidence: float
    reasoning: str


class RAGResponse(BaseModel):
    """RAG agent response schema."""
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float


class ImageAnalysisRequest(BaseModel):
    """Image analysis request schema."""
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    analysis_type: str = "symptom_classification"


class ImageAnalysisResponse(BaseModel):
    """Image analysis response schema."""
    predictions: List[Dict[str, Any]]
    confidence_scores: List[float]
    bounding_boxes: Optional[List[Dict[str, Any]]] = None
    metadata: Dict[str, Any]


class PrescriptionRequest(BaseModel):
    """Prescription generation request schema."""
    patient_id: int
    diagnosis: str
    symptoms: List[str]
    allergies: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None


class PrescriptionResponse(BaseModel):
    """Prescription response schema."""
    prescription_id: str
    medications: List[Dict[str, Any]]
    instructions: str
    interactions_checked: bool
    contraindications: Optional[List[str]] = None
    provenance: Dict[str, Any]


# ============================================================================
# Audit Schemas
# ============================================================================

class AuditLogResponse(BaseModel):
    """Audit log response schema."""
    id: int
    event_type: str
    event_id: str
    user_id: Optional[int]
    session_id: Optional[str]
    agent_name: Optional[str]
    action: Optional[str]
    timestamp: datetime
    metadata: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


# ============================================================================
# Health Check Schema
# ============================================================================

class HealthCheck(BaseModel):
    """Health check response schema."""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]

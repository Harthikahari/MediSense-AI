"""
Agent orchestration routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import uuid

from app.db.schemas import AgentRequest, AgentResponse
from app.api.v1.routes_auth import get_current_user_id
from app.agents import (
    RoutingAgent,
    RAGAgent,
    SQLAgent,
    AppointmentAgent,
    PaymentAgent,
    ImageAgent,
    ReportAgent,
    PrescriptionAgent,
    GuardrailAgent,
    AuditAgent
)
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

# Initialize agents
routing_agent = RoutingAgent()
rag_agent = RAGAgent()
sql_agent = SQLAgent()
appointment_agent = AppointmentAgent()
payment_agent = PaymentAgent()
image_agent = ImageAgent()
report_agent = ReportAgent()
prescription_agent = PrescriptionAgent()
guardrail_agent = GuardrailAgent()
audit_agent = AuditAgent()

# Agent registry
AGENTS = {
    "routing": routing_agent,
    "rag": rag_agent,
    "sql": sql_agent,
    "appointment": appointment_agent,
    "payment": payment_agent,
    "image": image_agent,
    "image_analysis": image_agent,  # Alias
    "report": report_agent,
    "report_understanding": report_agent,  # Alias
    "prescription": prescription_agent,
    "guardrail": guardrail_agent,
    "audit": audit_agent
}


@router.post("/chat", response_model=AgentResponse)
async def chat(
    request: AgentRequest,
    user_id: int = Depends(get_current_user_id)
):
    """
    General chat endpoint with automatic agent routing.

    Args:
        request: Agent request with query
        user_id: Current user ID

    Returns:
        Agent response
    """
    session_id = request.session_id or str(uuid.uuid4())

    # First, route the query
    routing_task = {
        "query": request.query,
        "context": request.context or {},
        "session_id": session_id,
        "user_id": user_id
    }

    routing_result = await routing_agent.run(routing_task)

    if not routing_result.success:
        raise HTTPException(status_code=500, detail="Routing failed")

    # Get target agent
    target_agent_name = routing_result.response.get("target_agent")
    target_agent = AGENTS.get(target_agent_name)

    if not target_agent:
        # Fallback to RAG agent
        target_agent = rag_agent
        target_agent_name = "rag"

    # Execute target agent
    agent_task = {
        "query": request.query,
        "context": request.context or {},
        "session_id": session_id,
        "user_id": user_id
    }

    result = await target_agent.run(agent_task)

    # Apply guardrails
    guardrail_result = await guardrail_agent.run({
        "query": "validate",
        "context": {
            "content": str(result.response),
            "source_agent": target_agent_name
        },
        "session_id": session_id,
        "user_id": user_id
    })

    # Use redacted content if guardrails applied
    if guardrail_result.success and not guardrail_result.response.get("should_block"):
        final_response = guardrail_result.response.get("redacted_content", result.response)
    else:
        final_response = "Response blocked by safety policies."

    return AgentResponse(
        agent_name=target_agent_name,
        response=str(final_response),
        confidence=result.confidence,
        provenance=result.provenance,
        metadata={
            "routing_confidence": routing_result.confidence,
            "guardrails_applied": len(guardrail_result.response.get("violations", []))
        }
    )


@router.post("/agent/{agent_name}", response_model=AgentResponse)
async def call_agent(
    agent_name: str,
    request: AgentRequest,
    user_id: int = Depends(get_current_user_id)
):
    """
    Call a specific agent directly.

    Args:
        agent_name: Name of the agent to call
        request: Agent request
        user_id: Current user ID

    Returns:
        Agent response
    """
    agent = AGENTS.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    session_id = request.session_id or str(uuid.uuid4())

    agent_task = {
        "query": request.query,
        "context": request.context or {},
        "session_id": session_id,
        "user_id": user_id
    }

    result = await agent.run(agent_task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return AgentResponse(
        agent_name=agent_name,
        response=str(result.response),
        confidence=result.confidence,
        provenance=result.provenance,
        metadata=result.metadata
    )


@router.get("/agents")
async def list_agents():
    """List all available agents."""
    return {
        "agents": list(AGENTS.keys()),
        "count": len(AGENTS)
    }


@router.post("/appointment/book")
async def book_appointment(
    clinician_id: int,
    start_time: str,
    duration_minutes: int = 30,
    appointment_type: str = "consultation",
    chief_complaint: str = None,
    user_id: int = Depends(get_current_user_id)
):
    """Book an appointment."""
    task = {
        "query": "book appointment",
        "context": {
            "action": "book",
            "clinician_id": clinician_id,
            "start_time": start_time,
            "duration_minutes": duration_minutes,
            "appointment_type": appointment_type,
            "chief_complaint": chief_complaint
        },
        "session_id": str(uuid.uuid4()),
        "user_id": user_id
    }

    result = await appointment_agent.run(task)

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    return result.response


@router.post("/prescription/generate")
async def generate_prescription(
    diagnosis: str,
    symptoms: list,
    allergies: list = None,
    current_medications: list = None,
    user_id: int = Depends(get_current_user_id)
):
    """Generate a prescription."""
    task = {
        "query": "generate prescription",
        "context": {
            "diagnosis": diagnosis,
            "symptoms": symptoms,
            "allergies": allergies or [],
            "current_medications": current_medications or []
        },
        "session_id": str(uuid.uuid4()),
        "user_id": user_id
    }

    result = await prescription_agent.run(task)

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    return result.response

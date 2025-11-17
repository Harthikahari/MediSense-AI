"""
Tests for agent implementations.
"""

import pytest
from app.agents import (
    RoutingAgent,
    RAGAgent,
    SQLAgent,
    PrescriptionAgent,
    GuardrailAgent
)


@pytest.mark.asyncio
async def test_routing_agent():
    """Test routing agent classification."""
    agent = RoutingAgent()

    task = {
        "query": "book an appointment with Dr. Smith",
        "context": {},
        "session_id": "test_session",
        "user_id": 1
    }

    result = await agent.run(task)

    assert result.success
    assert "appointment" in result.response["target_agent"]
    assert result.confidence > 0.5


@pytest.mark.asyncio
async def test_prescription_agent():
    """Test prescription generation."""
    agent = PrescriptionAgent()

    task = {
        "query": "generate prescription",
        "context": {
            "diagnosis": "bacterial infection",
            "symptoms": ["fever", "cough"],
            "allergies": [],
            "current_medications": []
        },
        "session_id": "test_session",
        "user_id": 1
    }

    result = await agent.run(task)

    assert result.success
    assert "prescription_id" in result.response
    assert len(result.response["medications"]) > 0
    assert result.response["interactions_checked"] is True


@pytest.mark.asyncio
async def test_guardrail_agent():
    """Test guardrail policy enforcement."""
    agent = GuardrailAgent()

    # Test PHI redaction
    task = {
        "query": "validate content",
        "context": {
            "content": "Patient SSN: 123-45-6789, Phone: 555-1234",
            "content_type": "text"
        },
        "session_id": "test_session",
        "user_id": 1
    }

    result = await agent.run(task)

    assert result.success
    assert len(result.response["violations"]) > 0
    assert "[REDACTED_" in result.response["redacted_content"]


@pytest.mark.asyncio
async def test_sql_agent_safety():
    """Test SQL agent safety checks."""
    agent = SQLAgent()

    # Test that dangerous queries are blocked
    task = {
        "query": "DROP TABLE users",
        "context": {
            "sql": "DROP TABLE users"
        },
        "session_id": "test_session",
        "user_id": 1
    }

    result = await agent.run(task)

    # Should fail safety check
    assert not result.success
    assert "unsafe" in result.error.lower()


def test_routing_agent_patterns():
    """Test routing agent pattern matching."""
    agent = RoutingAgent()

    test_queries = [
        ("schedule an appointment", "appointment"),
        ("analyze this image", "image_analysis"),
        ("read this lab report", "report_understanding"),
        ("prescribe medication", "prescription")
    ]

    for query, expected_agent in test_queries:
        matches = agent._rule_based_classification(query.lower())
        assert len(matches) > 0
        assert matches[0]["agent"] == expected_agent

"""
Tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "MediSense-AI"


def test_list_agents():
    """Test list agents endpoint."""
    response = client.get("/api/v1/agents/agents")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert len(data["agents"]) > 0


def test_mcp_status():
    """Test MCP status endpoint."""
    response = client.get("/api/v1/mcp/status")
    assert response.status_code == 200
    data = response.json()
    assert "mode" in data
    assert "available_clients" in data


# Note: Auth and agent endpoints require authentication
# Would add more comprehensive tests with mocked authentication

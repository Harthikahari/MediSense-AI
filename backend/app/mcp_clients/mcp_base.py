"""
Base MCP (Model Context Protocol) client abstraction.
Provides interface for both mock and Anthropic implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum
import httpx
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class MCPMode(str, Enum):
    """MCP operation modes."""
    MOCK = "mock"
    ANTHROPIC = "anthropic"


class ToolClient(ABC):
    """
    Abstract base class for MCP tool clients.
    All MCP clients must implement the call_tool method.
    """

    def __init__(self, mode: MCPMode = None):
        """
        Initialize the tool client.

        Args:
            mode: MCP mode (mock or anthropic)
        """
        self.mode = mode or MCPMode(settings.MCP_MODE)
        self.timeout = settings.MCP_TIMEOUT

    @abstractmethod
    async def call_tool(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool with the given name and payload.

        Args:
            name: Tool name
            payload: Tool payload/parameters

        Returns:
            Tool execution result

        Raises:
            Exception: If tool execution fails
        """
        pass

    def _validate_payload(self, payload: Dict[str, Any], required_keys: list) -> None:
        """
        Validate that payload contains required keys.

        Args:
            payload: Payload to validate
            required_keys: List of required keys

        Raises:
            ValueError: If required keys are missing
        """
        missing_keys = [key for key in required_keys if key not in payload]
        if missing_keys:
            raise ValueError(f"Missing required payload keys: {missing_keys}")


class AnthropicMCPClient(ToolClient):
    """
    Anthropic MCP client for production use.
    Communicates with Claude API via MCP protocol.
    """

    def __init__(self):
        """Initialize Anthropic MCP client."""
        super().__init__(mode=MCPMode.ANTHROPIC)

        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required for Anthropic MCP mode")

        self.api_key = settings.ANTHROPIC_API_KEY
        self.host = settings.MCP_HOST
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def call_tool(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool via Anthropic MCP endpoint.

        Args:
            name: Tool name
            payload: Tool payload

        Returns:
            Tool execution result
        """
        logger.info(f"Calling Anthropic MCP tool: {name}", payload=payload)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.host}/v1/tools/{name}",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Anthropic MCP tool {name} succeeded", result=result)
                return result

            except httpx.HTTPError as e:
                logger.error(f"Anthropic MCP tool {name} failed", error=str(e))
                raise Exception(f"MCP tool call failed: {str(e)}")


class MockMCPClient(ToolClient):
    """
    Mock MCP client for development and testing.
    Returns simulated responses without external API calls.
    """

    def __init__(self):
        """Initialize mock MCP client."""
        super().__init__(mode=MCPMode.MOCK)

    async def call_tool(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool with mock implementation.

        Args:
            name: Tool name
            payload: Tool payload

        Returns:
            Mocked tool execution result
        """
        logger.info(f"Calling mock MCP tool: {name}", payload=payload)

        # Return mock responses based on tool name
        mock_responses = {
            "search_documents": {
                "results": [
                    {
                        "id": "doc_1",
                        "title": "Mock Clinical Document",
                        "content": "This is a mock clinical document for testing.",
                        "score": 0.95
                    }
                ]
            },
            "execute_query": {
                "rows": [{"id": 1, "name": "Test Patient", "age": 35}],
                "row_count": 1
            },
            "classify_image": {
                "predictions": [
                    {"label": "rash", "confidence": 0.87},
                    {"label": "eczema", "confidence": 0.12}
                ]
            },
            "process_payment": {
                "transaction_id": "txn_mock_12345",
                "status": "success",
                "amount": 150.00
            },
            "send_notification": {
                "message_id": "msg_mock_67890",
                "status": "sent"
            }
        }

        # Return mock response or default
        result = mock_responses.get(name, {"status": "success", "message": f"Mock response for {name}"})
        logger.info(f"Mock MCP tool {name} succeeded", result=result)
        return result


def get_mcp_client() -> ToolClient:
    """
    Get the appropriate MCP client based on configuration.

    Returns:
        MCP client instance (Mock or Anthropic)
    """
    if settings.MCP_MODE == "anthropic":
        return AnthropicMCPClient()
    else:
        return MockMCPClient()

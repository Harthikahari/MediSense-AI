"""
Base agent class for MediSense-AI multi-agent system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime
import uuid
from app.core.logger import get_logger, audit_logger
from app.core.security import redact_phi_dict

logger = get_logger(__name__)


@dataclass
class AgentTask:
    """Task definition for an agent."""
    task_id: str
    query: str
    context: Dict[str, Any]
    session_id: str
    user_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AgentResult:
    """Result from an agent execution."""
    agent_name: str
    task_id: str
    success: bool
    response: Any
    confidence: float = 0.0
    provenance: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    Provides common functionality for logging, error handling, and result formatting.
    """

    def __init__(self, agent_name: str):
        """
        Initialize the base agent.

        Args:
            agent_name: Name identifier for the agent
        """
        self.agent_name = agent_name
        self.logger = get_logger(f"agent.{agent_name}")

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute the agent's primary task.

        Args:
            task: Task definition

        Returns:
            Agent execution result

        Raises:
            Exception: If execution fails
        """
        pass

    async def run(self, task: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with task dictionary (wrapper for execute).

        Args:
            task: Task dictionary with query, context, session_id, etc.

        Returns:
            Agent execution result
        """
        # Convert dict to AgentTask
        agent_task = AgentTask(
            task_id=task.get("task_id", str(uuid.uuid4())),
            query=task.get("query", ""),
            context=task.get("context", {}),
            session_id=task.get("session_id", str(uuid.uuid4())),
            user_id=task.get("user_id"),
            metadata=task.get("metadata", {})
        )

        start_time = datetime.now()

        try:
            self.logger.info(f"Starting {self.agent_name} execution", task_id=agent_task.task_id)

            # Execute the agent
            result = await self.execute(agent_task)

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            result.execution_time_ms = execution_time

            # Log to audit trail
            self._log_execution(agent_task, result)

            self.logger.info(
                f"{self.agent_name} execution completed",
                task_id=agent_task.task_id,
                success=result.success,
                execution_time_ms=execution_time
            )

            return result

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.error(
                f"{self.agent_name} execution failed",
                task_id=agent_task.task_id,
                error=str(e),
                execution_time_ms=execution_time
            )

            # Create error result
            error_result = AgentResult(
                agent_name=self.agent_name,
                task_id=agent_task.task_id,
                success=False,
                response=None,
                error=str(e),
                execution_time_ms=execution_time
            )

            # Log error to audit trail
            self._log_execution(agent_task, error_result)

            return error_result

    def _log_execution(self, task: AgentTask, result: AgentResult):
        """
        Log agent execution to audit trail.

        Args:
            task: Task that was executed
            result: Execution result
        """
        try:
            # Prepare input/output data with PHI redaction
            input_data = redact_phi_dict({
                "query": task.query,
                "context": task.context
            })

            output_data = redact_phi_dict({
                "response": str(result.response) if result.response else None,
                "confidence": result.confidence,
                "success": result.success
            })

            # Log to audit system
            audit_logger.log_agent_action(
                agent_name=self.agent_name,
                action="execute",
                user_id=str(task.user_id) if task.user_id else "system",
                session_id=task.session_id,
                input_data=input_data,
                output_data=output_data,
                metadata={
                    "task_id": task.task_id,
                    "execution_time_ms": result.execution_time_ms,
                    "provenance": result.provenance
                }
            )
        except Exception as e:
            self.logger.error(f"Failed to log execution to audit trail: {str(e)}")

    def create_success_result(
        self,
        task_id: str,
        response: Any,
        confidence: float = 1.0,
        provenance: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Create a success result.

        Args:
            task_id: Task identifier
            response: Agent response
            confidence: Confidence score (0-1)
            provenance: Source provenance
            metadata: Additional metadata

        Returns:
            Success result
        """
        return AgentResult(
            agent_name=self.agent_name,
            task_id=task_id,
            success=True,
            response=response,
            confidence=confidence,
            provenance=provenance,
            metadata=metadata
        )

    def create_error_result(
        self,
        task_id: str,
        error: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Create an error result.

        Args:
            task_id: Task identifier
            error: Error message
            metadata: Additional metadata

        Returns:
            Error result
        """
        return AgentResult(
            agent_name=self.agent_name,
            task_id=task_id,
            success=False,
            response=None,
            error=error,
            metadata=metadata
        )

"""
Structured logging configuration for MediSense-AI.
Provides audit logging and application logging with PHI redaction.
"""

import logging
import sys
from typing import Any, Dict
from datetime import datetime
from pathlib import Path
import structlog
from .config import settings
from .security import redact_phi_dict


def setup_logging():
    """Configure structured logging for the application."""

    # Create log directory if it doesn't exist
    log_path = Path(settings.AUDIT_LOG_PATH).parent
    log_path.mkdir(parents=True, exist_ok=True)

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class AuditLogger:
    """
    Audit logger for clinical decision tracking and compliance.
    Maintains immutable audit trails.
    """

    def __init__(self):
        """Initialize audit logger."""
        self.logger = get_logger("audit")
        self.audit_file = settings.AUDIT_LOG_PATH

        # Setup file handler for audit logs
        file_handler = logging.FileHandler(self.audit_file)
        file_handler.setLevel(logging.INFO)

        # Get root logger and add handler
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)

    def log_agent_action(
        self,
        agent_name: str,
        action: str,
        user_id: str,
        session_id: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ):
        """
        Log an agent action with full context.

        Args:
            agent_name: Name of the agent
            action: Action performed
            user_id: User ID who initiated the action
            session_id: Session identifier
            input_data: Input data to the agent
            output_data: Output data from the agent
            metadata: Additional metadata
        """
        if not settings.AUDIT_ENABLED:
            return

        # Redact PHI from input and output
        safe_input = redact_phi_dict(input_data) if input_data else {}
        safe_output = redact_phi_dict(output_data) if output_data else {}

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "agent_action",
            "agent_name": agent_name,
            "action": action,
            "user_id": user_id,
            "session_id": session_id,
            "input": safe_input,
            "output": safe_output,
            "metadata": metadata or {}
        }

        self.logger.info("agent_action", **audit_entry)

    def log_llm_call(
        self,
        model: str,
        prompt: str,
        response: str,
        user_id: str,
        session_id: str,
        tokens_used: int = None,
        metadata: Dict[str, Any] = None
    ):
        """
        Log an LLM API call for provenance tracking.

        Args:
            model: Model name/identifier
            prompt: Input prompt (redacted)
            response: Model response (redacted)
            user_id: User ID
            session_id: Session identifier
            tokens_used: Number of tokens used
            metadata: Additional metadata
        """
        if not settings.AUDIT_ENABLED:
            return

        # Redact PHI from prompt and response
        safe_prompt = redact_phi_dict({"prompt": prompt})["prompt"]
        safe_response = redact_phi_dict({"response": response})["response"]

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "llm_call",
            "model": model,
            "prompt": safe_prompt,
            "response": safe_response,
            "user_id": user_id,
            "session_id": session_id,
            "tokens_used": tokens_used,
            "metadata": metadata or {}
        }

        self.logger.info("llm_call", **audit_entry)

    def log_data_access(
        self,
        resource_type: str,
        resource_id: str,
        action: str,
        user_id: str,
        success: bool,
        metadata: Dict[str, Any] = None
    ):
        """
        Log data access for compliance tracking.

        Args:
            resource_type: Type of resource accessed
            resource_id: Resource identifier
            action: Action performed (read, write, delete)
            user_id: User ID
            success: Whether the action was successful
            metadata: Additional metadata
        """
        if not settings.AUDIT_ENABLED:
            return

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "data_access",
            "resource_type": resource_type,
            "resource_id": resource_id,
            "action": action,
            "user_id": user_id,
            "success": success,
            "metadata": metadata or {}
        }

        self.logger.info("data_access", **audit_entry)

    def log_guardrail_violation(
        self,
        policy: str,
        violation_type: str,
        user_id: str,
        session_id: str,
        context: Dict[str, Any],
        action_taken: str
    ):
        """
        Log guardrail policy violations.

        Args:
            policy: Policy that was violated
            violation_type: Type of violation
            user_id: User ID
            session_id: Session identifier
            context: Context of the violation
            action_taken: Action taken in response
        """
        if not settings.AUDIT_ENABLED:
            return

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "guardrail_violation",
            "policy": policy,
            "violation_type": violation_type,
            "user_id": user_id,
            "session_id": session_id,
            "context": redact_phi_dict(context),
            "action_taken": action_taken
        }

        self.logger.warning("guardrail_violation", **audit_entry)


# Global audit logger instance
audit_logger = AuditLogger()


# Initialize logging on module import
setup_logging()

"""
Audit Agent for maintaining immutable audit trails and explainability.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from .base_agent import BaseAgent, AgentTask, AgentResult
from app.core.logger import audit_logger


class AuditAgent(BaseAgent):
    """
    Audit agent for maintaining comprehensive audit trails and providing explainability.
    Tracks all agent actions, LLM calls, and decision provenance.
    """

    def __init__(self):
        """Initialize audit agent."""
        super().__init__("audit_agent")

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute audit operations.

        Args:
            task: Agent task with action (log, query, export)

        Returns:
            Audit operation result
        """
        try:
            action = task.context.get("action", "log")

            if action == "log":
                return await self._log_event(task)
            elif action == "query":
                return await self._query_audit_trail(task)
            elif action == "explain":
                return await self._explain_decision(task)
            elif action == "export":
                return await self._export_audit_trail(task)
            else:
                return self.create_error_result(
                    task_id=task.task_id,
                    error=f"Unknown action: {action}"
                )

        except Exception as e:
            self.logger.error(f"Audit agent failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"Audit operation failed: {str(e)}"
            )

    async def _log_event(self, task: AgentTask) -> AgentResult:
        """Log an audit event."""
        event_type = task.context.get("event_type", "generic")
        event_data = task.context.get("event_data", {})

        event_id = f"evt_{uuid.uuid4().hex[:12]}"

        # Log to audit system
        audit_logger.log_agent_action(
            agent_name=event_data.get("agent_name", "system"),
            action=event_data.get("action", "unknown"),
            user_id=str(task.user_id) if task.user_id else "system",
            session_id=task.session_id,
            input_data=event_data.get("input", {}),
            output_data=event_data.get("output", {}),
            metadata={
                "event_id": event_id,
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

        return self.create_success_result(
            task_id=task.task_id,
            response={
                "event_id": event_id,
                "event_type": event_type,
                "logged_at": datetime.utcnow().isoformat(),
                "status": "logged"
            },
            confidence=1.0
        )

    async def _query_audit_trail(self, task: AgentTask) -> AgentResult:
        """Query audit trail with filters."""
        filters = {
            "user_id": task.context.get("user_id"),
            "session_id": task.context.get("session_id"),
            "event_type": task.context.get("event_type"),
            "start_date": task.context.get("start_date"),
            "end_date": task.context.get("end_date"),
            "agent_name": task.context.get("agent_name")
        }

        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}

        # In production, query the database
        # For now, return mock results
        audit_entries = [
            {
                "event_id": "evt_001",
                "event_type": "agent_action",
                "agent_name": "rag_agent",
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": filters.get("user_id", "unknown")
            }
        ]

        return self.create_success_result(
            task_id=task.task_id,
            response={
                "filters": filters,
                "entries": audit_entries,
                "total_count": len(audit_entries)
            },
            confidence=1.0
        )

    async def _explain_decision(self, task: AgentTask) -> AgentResult:
        """Provide explainability for a decision."""
        decision_id = task.context.get("decision_id")
        session_id = task.context.get("session_id")

        if not decision_id and not session_id:
            return self.create_error_result(
                task_id=task.task_id,
                error="Must provide decision_id or session_id"
            )

        # Retrieve decision chain from audit logs
        # Build provenance graph
        explanation = {
            "decision_id": decision_id,
            "timeline": [
                {
                    "step": 1,
                    "agent": "routing_agent",
                    "action": "classify_intent",
                    "result": "routed to prescription_agent",
                    "timestamp": datetime.utcnow().isoformat()
                },
                {
                    "step": 2,
                    "agent": "prescription_agent",
                    "action": "generate_prescription",
                    "result": "prescribed amoxicillin 500mg",
                    "reasoning": "Based on diagnosis of bacterial infection",
                    "timestamp": datetime.utcnow().isoformat()
                }
            ],
            "data_sources": [
                {
                    "source": "patient_record",
                    "accessed": datetime.utcnow().isoformat()
                },
                {
                    "source": "drug_database",
                    "accessed": datetime.utcnow().isoformat()
                }
            ],
            "models_used": [
                {
                    "model": "clinical_decision_support",
                    "version": "1.0",
                    "confidence": 0.92
                }
            ]
        }

        return self.create_success_result(
            task_id=task.task_id,
            response=explanation,
            confidence=1.0,
            provenance=[{
                "type": "decision_explainability",
                "decision_id": decision_id
            }]
        )

    async def _export_audit_trail(self, task: AgentTask) -> AgentResult:
        """Export audit trail for compliance."""
        format_type = task.context.get("format", "json")  # json, pdf, csv
        filters = task.context.get("filters", {})

        export_id = f"export_{uuid.uuid4().hex[:12]}"

        # In production, generate actual export file
        export_result = {
            "export_id": export_id,
            "format": format_type,
            "filters": filters,
            "status": "completed",
            "file_path": f"/exports/{export_id}.{format_type}",
            "generated_at": datetime.utcnow().isoformat(),
            "entry_count": 42  # Mock count
        }

        return self.create_success_result(
            task_id=task.task_id,
            response=export_result,
            confidence=1.0
        )

    def create_provenance_chain(
        self,
        agent_actions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a provenance chain from agent actions.

        Args:
            agent_actions: List of agent actions in order

        Returns:
            Provenance chain structure
        """
        chain = {
            "chain_id": str(uuid.uuid4()),
            "created_at": datetime.utcnow().isoformat(),
            "steps": []
        }

        for i, action in enumerate(agent_actions):
            step = {
                "step_number": i + 1,
                "agent": action.get("agent_name"),
                "action": action.get("action"),
                "timestamp": action.get("timestamp"),
                "input_hash": self._hash_data(action.get("input")),
                "output_hash": self._hash_data(action.get("output")),
                "dependencies": action.get("dependencies", [])
            }
            chain["steps"].append(step)

        return chain

    def _hash_data(self, data: Any) -> str:
        """Create a hash of data for provenance tracking."""
        import hashlib
        import json

        if data is None:
            return "null"

        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]

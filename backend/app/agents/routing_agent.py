"""
Routing Agent - Classifies user intent and dispatches to appropriate specialist agents.
"""

from typing import Dict, Any, List
import re
from .base_agent import BaseAgent, AgentTask, AgentResult


class RoutingAgent(BaseAgent):
    """
    Routing agent that classifies user queries and routes them to specialist agents.
    Uses rule-based classification with LLM fallback for ambiguous cases.
    """

    def __init__(self):
        """Initialize routing agent."""
        super().__init__("routing_agent")

        # Define routing rules
        self.routing_rules = {
            "appointment": [
                r"book.*appointment",
                r"schedule.*appointment",
                r"available.*slot",
                r"doctor.*availability",
                r"cancel.*appointment",
                r"reschedule"
            ],
            "image_analysis": [
                r"analyze.*image",
                r"symptom.*photo",
                r"look at.*picture",
                r"rash",
                r"lesion",
                r"skin.*condition"
            ],
            "report_understanding": [
                r"read.*report",
                r"understand.*pdf",
                r"lab.*result",
                r"test.*result",
                r"medical.*record",
                r"extract.*report"
            ],
            "prescription": [
                r"prescri(be|ption)",
                r"medication",
                r"drug.*interaction",
                r"pharmacy",
                r"refill"
            ],
            "rag": [
                r"find.*document",
                r"search.*record",
                r"what does.*say",
                r"information.*about",
                r"history.*of"
            ],
            "sql": [
                r"query.*database",
                r"patient.*record",
                r"statistics",
                r"count.*patients",
                r"list.*all"
            ],
            "payment": [
                r"payment",
                r"billing",
                r"invoice",
                r"insurance",
                r"cost"
            ]
        }

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute routing classification.

        Args:
            task: Agent task with query

        Returns:
            Routing decision with target agent and confidence
        """
        query = task.query.lower()

        # Try rule-based classification first
        matches = self._rule_based_classification(query)

        if matches:
            # Get best match
            best_match = max(matches, key=lambda x: x["confidence"])

            return self.create_success_result(
                task_id=task.task_id,
                response={
                    "target_agent": best_match["agent"],
                    "confidence": best_match["confidence"],
                    "reasoning": f"Matched pattern: {best_match['pattern']}"
                },
                confidence=best_match["confidence"]
            )

        # Fallback to default RAG agent for general queries
        return self.create_success_result(
            task_id=task.task_id,
            response={
                "target_agent": "rag",
                "confidence": 0.5,
                "reasoning": "No specific pattern matched, routing to RAG agent for general query"
            },
            confidence=0.5
        )

    def _rule_based_classification(self, query: str) -> List[Dict[str, Any]]:
        """
        Classify query using rule-based patterns.

        Args:
            query: User query (lowercase)

        Returns:
            List of matching agents with confidence scores
        """
        matches = []

        for agent_name, patterns in self.routing_rules.items():
            for pattern in patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    matches.append({
                        "agent": agent_name,
                        "pattern": pattern,
                        "confidence": 0.9  # High confidence for rule-based matches
                    })
                    break  # Only count first match per agent

        return matches

    def get_available_agents(self) -> List[str]:
        """
        Get list of available specialist agents.

        Returns:
            List of agent names
        """
        return list(self.routing_rules.keys())

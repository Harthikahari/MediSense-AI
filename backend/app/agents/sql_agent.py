"""
SQL Agent for safe, parameterized database queries.
"""

from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentTask, AgentResult
from app.mcp_clients import DatabaseMCPClient


class SQLAgent(BaseAgent):
    """
    SQL agent for translating natural language to SQL and executing safe queries.
    Always uses parameterized queries and read-only mode by default.
    """

    def __init__(self, db_client: Optional[DatabaseMCPClient] = None):
        """Initialize SQL agent."""
        super().__init__("sql_agent")
        self.db_client = db_client or DatabaseMCPClient()

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute SQL query generation and execution.

        Args:
            task: Agent task with query

        Returns:
            Query results
        """
        try:
            query = task.query
            context = task.context

            # Determine query type
            if "sql" in context:
                # Direct SQL execution (for advanced users)
                sql_query = context["sql"]
                params = context.get("params", {})
            else:
                # NL to SQL translation
                sql_query, params = self._translate_nl_to_sql(query, context)

            # Validate query safety
            if not self._is_safe_query(sql_query):
                return self.create_error_result(
                    task_id=task.task_id,
                    error="Query validation failed: potentially unsafe query detected"
                )

            # Execute query with read-only mode
            self.logger.info("Executing SQL query", query_preview=sql_query[:100])
            result = await self.db_client.execute_query(
                query=sql_query,
                params=params,
                read_only=True
            )

            return self.create_success_result(
                task_id=task.task_id,
                response={
                    "query": sql_query,
                    "params": params,
                    "results": result.get("rows", []),
                    "row_count": result.get("row_count", 0)
                },
                confidence=0.9,
                provenance=[{
                    "type": "database_query",
                    "query": sql_query,
                    "timestamp": result.get("timestamp")
                }]
            )

        except Exception as e:
            self.logger.error(f"SQL execution failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"SQL agent failed: {str(e)}"
            )

    def _translate_nl_to_sql(
        self,
        natural_language: str,
        context: Dict[str, Any]
    ) -> tuple[str, Dict[str, Any]]:
        """
        Translate natural language to SQL query.

        This is a simplified implementation. In production, this would:
        1. Use LLM to generate SQL from NL
        2. Validate against schema
        3. Apply safety constraints

        Args:
            natural_language: Natural language query
            context: Additional context

        Returns:
            Tuple of (SQL query, parameters)
        """
        # Simplified pattern matching for common queries
        nl_lower = natural_language.lower()

        if "count" in nl_lower and "patient" in nl_lower:
            return "SELECT COUNT(*) as patient_count FROM users WHERE role = :role", {"role": "patient"}

        elif "appointment" in nl_lower and "today" in nl_lower:
            return (
                "SELECT * FROM appointments WHERE DATE(scheduled_start) = CURRENT_DATE "
                "ORDER BY scheduled_start LIMIT :limit",
                {"limit": context.get("limit", 50)}
            )

        elif "patient" in nl_lower and "name" in nl_lower:
            patient_name = context.get("patient_name", "")
            return (
                "SELECT * FROM users WHERE role = :role AND full_name ILIKE :name LIMIT :limit",
                {"role": "patient", "name": f"%{patient_name}%", "limit": 10}
            )

        else:
            # Default safe query
            return "SELECT 1 as result", {}

    def _is_safe_query(self, sql_query: str) -> bool:
        """
        Validate query safety.

        Args:
            sql_query: SQL query to validate

        Returns:
            True if query is safe
        """
        sql_upper = sql_query.upper().strip()

        # Must be SELECT query
        if not sql_upper.startswith("SELECT"):
            return False

        # No dangerous operations
        dangerous_keywords = [
            "DROP", "DELETE", "UPDATE", "INSERT",
            "ALTER", "CREATE", "TRUNCATE", "EXEC",
            "EXECUTE", "GRANT", "REVOKE"
        ]

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return False

        return True

    async def explain_query(self, sql_query: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get query execution plan.

        Args:
            sql_query: SQL query
            params: Query parameters

        Returns:
            Query execution plan
        """
        result = await self.db_client.explain_query(sql_query, params)
        return result

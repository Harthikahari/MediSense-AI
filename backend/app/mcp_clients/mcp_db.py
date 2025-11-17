"""
MCP Database client for safe SQL query execution.
"""

from typing import Any, Dict, List, Optional
from .mcp_base import ToolClient, get_mcp_client
from app.core.logger import get_logger
from app.core.security import sanitize_sql_input

logger = get_logger(__name__)


class DatabaseMCPClient:
    """
    MCP client for database operations.
    Provides safe, parameterized SQL execution with read-only access.
    """

    def __init__(self, client: Optional[ToolClient] = None):
        """
        Initialize database MCP client.

        Args:
            client: Optional MCP client instance
        """
        self.client = client or get_mcp_client()

    async def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        read_only: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a parameterized SQL query.

        Args:
            query: SQL query string with parameter placeholders
            params: Query parameters
            read_only: If True, only SELECT queries are allowed

        Returns:
            Query results and metadata

        Raises:
            ValueError: If read_only is True and query is not SELECT
        """
        # Validate read-only mode
        if read_only and not query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed in read-only mode")

        # Sanitize query (basic validation)
        sanitized_query = sanitize_sql_input(query)

        payload = {
            "query": sanitized_query,
            "params": params or {},
            "read_only": read_only
        }

        logger.info("Executing database query", query_preview=query[:100])
        result = await self.client.call_tool("execute_query", payload)
        return result

    async def explain_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get query execution plan without executing the query.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Query execution plan
        """
        payload = {
            "query": f"EXPLAIN {query}",
            "params": params or {}
        }

        logger.info("Explaining query", query_preview=query[:100])
        result = await self.client.call_tool("execute_query", payload)
        return result

    async def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Get schema information for a table.

        Args:
            table_name: Name of the table

        Returns:
            Table schema information
        """
        # Sanitize table name
        safe_table_name = sanitize_sql_input(table_name)

        payload = {
            "table_name": safe_table_name
        }

        logger.info("Getting table schema", table_name=table_name)
        result = await self.client.call_tool("get_table_schema", payload)
        return result

    async def search_patient_records(
        self,
        patient_name: Optional[str] = None,
        patient_id: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search patient records with filters.

        Args:
            patient_name: Patient name (partial match)
            patient_id: Patient ID (exact match)
            date_from: Start date for records
            date_to: End date for records
            limit: Maximum number of results

        Returns:
            List of matching patient records
        """
        filters = {
            "patient_name": patient_name,
            "patient_id": patient_id,
            "date_from": date_from,
            "date_to": date_to,
            "limit": limit
        }

        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}

        payload = {
            "operation": "search_patients",
            "filters": filters
        }

        logger.info("Searching patient records", filters=filters)
        result = await self.client.call_tool("search_patient_records", payload)
        return result.get("records", [])

    async def get_appointment_slots(
        self,
        clinician_id: int,
        date: str,
        duration_minutes: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get available appointment slots for a clinician.

        Args:
            clinician_id: Clinician ID
            date: Date in YYYY-MM-DD format
            duration_minutes: Appointment duration

        Returns:
            List of available time slots
        """
        payload = {
            "clinician_id": clinician_id,
            "date": date,
            "duration_minutes": duration_minutes
        }

        logger.info("Getting appointment slots", clinician_id=clinician_id, date=date)
        result = await self.client.call_tool("get_appointment_slots", payload)
        return result.get("slots", [])

    async def aggregate_health_metrics(
        self,
        patient_id: int,
        metric_type: str,
        date_from: str,
        date_to: str
    ) -> Dict[str, Any]:
        """
        Aggregate health metrics for a patient over time.

        Args:
            patient_id: Patient ID
            metric_type: Type of metric (e.g., 'blood_pressure', 'glucose')
            date_from: Start date
            date_to: End date

        Returns:
            Aggregated metrics and statistics
        """
        payload = {
            "patient_id": patient_id,
            "metric_type": metric_type,
            "date_from": date_from,
            "date_to": date_to
        }

        logger.info("Aggregating health metrics", patient_id=patient_id, metric_type=metric_type)
        result = await self.client.call_tool("aggregate_health_metrics", payload)
        return result

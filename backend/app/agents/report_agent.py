"""
Report Understanding Agent for extracting data from PDFs and clinical reports using OCR.
"""

from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent, AgentTask, AgentResult
from app.mcp_clients import DocumentMCPClient


class ReportAgent(BaseAgent):
    """
    Report understanding agent for processing clinical PDFs and extracting structured data.
    Uses OCR and LLM-assisted extraction.
    """

    def __init__(self, document_client: Optional[DocumentMCPClient] = None):
        """Initialize report agent."""
        super().__init__("report_agent")
        self.document_client = document_client or DocumentMCPClient()

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute report processing and data extraction.

        Args:
            task: Agent task with report file or content

        Returns:
            Extracted report data
        """
        try:
            report_path = task.context.get("report_path")
            report_content = task.context.get("report_content")
            report_type = task.context.get("report_type", "lab_results")

            if not report_path and not report_content:
                return self.create_error_result(
                    task_id=task.task_id,
                    error="Missing report_path or report_content"
                )

            # Extract text from PDF if path provided
            if report_path:
                if report_path.endswith(".pdf"):
                    result = await self.document_client.extract_pdf_text(report_path)
                    report_content = result.get("text", "")
                else:
                    # Assume it's an image, use OCR
                    result = await self.document_client.ocr_document(report_path)
                    report_content = result.get("text", "")

            # Extract structured data based on report type
            extracted_data = await self._extract_structured_data(
                report_content,
                report_type
            )

            # Generate summary
            summary = self._generate_summary(extracted_data, report_type)

            return self.create_success_result(
                task_id=task.task_id,
                response={
                    "report_type": report_type,
                    "extracted_data": extracted_data,
                    "summary": summary,
                    "raw_text_length": len(report_content),
                    "fields_extracted": len(extracted_data)
                },
                confidence=0.85,
                provenance=[{
                    "type": "document_extraction",
                    "source": report_path or "direct_content",
                    "extraction_method": "ocr_and_nlp"
                }]
            )

        except Exception as e:
            self.logger.error(f"Report agent failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"Report processing failed: {str(e)}"
            )

    async def _extract_structured_data(
        self,
        report_content: str,
        report_type: str
    ) -> Dict[str, Any]:
        """
        Extract structured data from report text.

        Args:
            report_content: Report text content
            report_type: Type of report

        Returns:
            Extracted structured data
        """
        # Define schema based on report type
        schemas = {
            "lab_results": {
                "patient_name": "string",
                "date": "date",
                "tests": "array",
                "results": "object",
                "abnormal_flags": "array"
            },
            "radiology": {
                "patient_name": "string",
                "study_type": "string",
                "findings": "string",
                "impression": "string",
                "radiologist": "string"
            },
            "pathology": {
                "patient_name": "string",
                "specimen_type": "string",
                "diagnosis": "string",
                "microscopic_description": "string",
                "pathologist": "string"
            }
        }

        schema = schemas.get(report_type, {})

        # Use document client to extract structured data
        result = await self.document_client.extract_structured_data(
            document_content=report_content,
            schema=schema
        )

        return result.get("extracted_data", {})

    def _generate_summary(
        self,
        extracted_data: Dict[str, Any],
        report_type: str
    ) -> str:
        """
        Generate a summary of extracted report data.

        Args:
            extracted_data: Extracted data
            report_type: Type of report

        Returns:
            Summary text
        """
        if report_type == "lab_results":
            return self._summarize_lab_results(extracted_data)
        elif report_type == "radiology":
            return self._summarize_radiology(extracted_data)
        elif report_type == "pathology":
            return self._summarize_pathology(extracted_data)
        else:
            return f"Extracted {len(extracted_data)} fields from {report_type} report."

    def _summarize_lab_results(self, data: Dict[str, Any]) -> str:
        """Summarize lab results."""
        patient = data.get("patient_name", "Unknown Patient")
        date = data.get("date", "Unknown Date")
        tests = data.get("tests", [])
        abnormal = data.get("abnormal_flags", [])

        summary = f"Lab results for {patient} dated {date}. "
        summary += f"Total tests: {len(tests)}. "

        if abnormal:
            summary += f"Abnormal results found: {', '.join(abnormal)}. "
        else:
            summary += "All results within normal ranges. "

        return summary

    def _summarize_radiology(self, data: Dict[str, Any]) -> str:
        """Summarize radiology report."""
        study_type = data.get("study_type", "Unknown Study")
        findings = data.get("findings", "")
        impression = data.get("impression", "")

        summary = f"{study_type} report. "
        if impression:
            summary += f"Impression: {impression[:200]}... "
        elif findings:
            summary += f"Findings: {findings[:200]}... "

        return summary

    def _summarize_pathology(self, data: Dict[str, Any]) -> str:
        """Summarize pathology report."""
        specimen = data.get("specimen_type", "Unknown Specimen")
        diagnosis = data.get("diagnosis", "")

        summary = f"Pathology report for {specimen}. "
        if diagnosis:
            summary += f"Diagnosis: {diagnosis}"

        return summary

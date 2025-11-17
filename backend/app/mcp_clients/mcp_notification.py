"""
MCP Notification client for email and SMS messaging.
"""

from typing import Any, Dict, List, Optional
from .mcp_base import ToolClient, get_mcp_client
from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)


class NotificationMCPClient:
    """
    MCP client for notification operations.
    Supports email and SMS notifications with template support.
    """

    def __init__(self, client: Optional[ToolClient] = None):
        """
        Initialize notification MCP client.

        Args:
            client: Optional MCP client instance
        """
        self.client = client or get_mcp_client()

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        template_name: Optional[str] = None,
        template_vars: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Send an email notification.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text or HTML)
            template_name: Optional template name
            template_vars: Variables for template rendering
            attachments: List of attachments

        Returns:
            Email sending result
        """
        payload = {
            "to_email": to_email,
            "subject": subject,
            "body": body,
            "template_name": template_name,
            "template_vars": template_vars or {},
            "attachments": attachments or [],
            "from_email": settings.SMTP_FROM_EMAIL
        }

        logger.info("Sending email", to=to_email, subject=subject)
        result = await self.client.call_tool("send_email", payload)
        return result

    async def send_sms(
        self,
        to_phone: str,
        message: str,
        template_name: Optional[str] = None,
        template_vars: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send an SMS notification.

        Args:
            to_phone: Recipient phone number
            message: SMS message text
            template_name: Optional template name
            template_vars: Variables for template rendering

        Returns:
            SMS sending result
        """
        payload = {
            "to_phone": to_phone,
            "message": message,
            "template_name": template_name,
            "template_vars": template_vars or {},
            "provider": settings.SMS_PROVIDER
        }

        logger.info("Sending SMS", to=to_phone)
        result = await self.client.call_tool("send_sms", payload)
        return result

    async def send_appointment_reminder(
        self,
        patient_email: str,
        patient_phone: Optional[str],
        appointment_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send appointment reminder via email and SMS.

        Args:
            patient_email: Patient email
            patient_phone: Patient phone (optional)
            appointment_details: Appointment information

        Returns:
            Reminder sending result
        """
        template_vars = {
            "patient_name": appointment_details.get("patient_name"),
            "clinician_name": appointment_details.get("clinician_name"),
            "appointment_time": appointment_details.get("scheduled_start"),
            "location": appointment_details.get("location", "Telehealth")
        }

        # Send email
        email_result = await self.send_email(
            to_email=patient_email,
            subject="Appointment Reminder",
            body="",  # Will use template
            template_name="appointment_reminder",
            template_vars=template_vars
        )

        # Send SMS if phone provided
        sms_result = None
        if patient_phone:
            sms_message = (
                f"Reminder: You have an appointment with Dr. {template_vars['clinician_name']} "
                f"on {template_vars['appointment_time']}."
            )
            sms_result = await self.send_sms(
                to_phone=patient_phone,
                message=sms_message
            )

        return {
            "email": email_result,
            "sms": sms_result
        }

    async def send_prescription_notification(
        self,
        patient_email: str,
        prescription_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send prescription notification to patient.

        Args:
            patient_email: Patient email
            prescription_details: Prescription information

        Returns:
            Notification result
        """
        template_vars = {
            "patient_name": prescription_details.get("patient_name"),
            "medications": prescription_details.get("medications", []),
            "prescriber": prescription_details.get("prescriber"),
            "instructions": prescription_details.get("instructions")
        }

        result = await self.send_email(
            to_email=patient_email,
            subject="New Prescription Available",
            body="",  # Will use template
            template_name="prescription_notification",
            template_vars=template_vars
        )

        logger.info("Prescription notification sent", patient_email=patient_email)
        return result

    async def send_test_results_notification(
        self,
        patient_email: str,
        test_results: Dict[str, Any],
        urgent: bool = False
    ) -> Dict[str, Any]:
        """
        Send test results notification to patient.

        Args:
            patient_email: Patient email
            test_results: Test result information
            urgent: Whether results are urgent

        Returns:
            Notification result
        """
        subject = "Urgent: Test Results Available" if urgent else "Test Results Available"

        template_vars = {
            "patient_name": test_results.get("patient_name"),
            "test_name": test_results.get("test_name"),
            "results_summary": test_results.get("summary"),
            "urgent": urgent,
            "follow_up_required": test_results.get("follow_up_required", False)
        }

        result = await self.send_email(
            to_email=patient_email,
            subject=subject,
            body="",  # Will use template
            template_name="test_results_notification",
            template_vars=template_vars
        )

        logger.info("Test results notification sent", patient_email=patient_email, urgent=urgent)
        return result

    async def send_bulk_notifications(
        self,
        recipients: List[Dict[str, str]],
        message_type: str,
        template_vars: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send bulk notifications to multiple recipients.

        Args:
            recipients: List of recipient details
            message_type: Type of message (email/sms)
            template_vars: Template variables

        Returns:
            Bulk send result
        """
        payload = {
            "recipients": recipients,
            "message_type": message_type,
            "template_vars": template_vars
        }

        logger.info("Sending bulk notifications", count=len(recipients), type=message_type)
        result = await self.client.call_tool("send_bulk_notifications", payload)
        return result

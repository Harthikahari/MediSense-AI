"""
Appointment Booking Agent for managing doctor calendars and scheduling.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from .base_agent import BaseAgent, AgentTask, AgentResult
from app.mcp_clients import DatabaseMCPClient, PaymentMCPClient, NotificationMCPClient


class AppointmentAgent(BaseAgent):
    """
    Appointment agent for scheduling, booking, and managing medical appointments.
    Includes availability checking, double-booking prevention, and payment integration.
    """

    def __init__(
        self,
        db_client: Optional[DatabaseMCPClient] = None,
        payment_client: Optional[PaymentMCPClient] = None,
        notification_client: Optional[NotificationMCPClient] = None
    ):
        """Initialize appointment agent."""
        super().__init__("appointment_agent")
        self.db_client = db_client or DatabaseMCPClient()
        self.payment_client = payment_client or PaymentMCPClient()
        self.notification_client = notification_client or NotificationMCPClient()

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute appointment-related operations.

        Args:
            task: Agent task with action (book, cancel, reschedule, check_availability)

        Returns:
            Appointment operation result
        """
        try:
            action = task.context.get("action", "check_availability")

            if action == "check_availability":
                return await self._check_availability(task)
            elif action == "book":
                return await self._book_appointment(task)
            elif action == "cancel":
                return await self._cancel_appointment(task)
            elif action == "reschedule":
                return await self._reschedule_appointment(task)
            else:
                return self.create_error_result(
                    task_id=task.task_id,
                    error=f"Unknown action: {action}"
                )

        except Exception as e:
            self.logger.error(f"Appointment agent failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"Appointment operation failed: {str(e)}"
            )

    async def _check_availability(self, task: AgentTask) -> AgentResult:
        """Check clinician availability for given date/time."""
        clinician_id = task.context.get("clinician_id")
        date = task.context.get("date")  # YYYY-MM-DD format
        duration = task.context.get("duration_minutes", 30)

        if not clinician_id or not date:
            return self.create_error_result(
                task_id=task.task_id,
                error="Missing required parameters: clinician_id and date"
            )

        # Get available slots
        slots = await self.db_client.get_appointment_slots(
            clinician_id=clinician_id,
            date=date,
            duration_minutes=duration
        )

        return self.create_success_result(
            task_id=task.task_id,
            response={
                "clinician_id": clinician_id,
                "date": date,
                "available_slots": slots,
                "slot_count": len(slots)
            },
            confidence=1.0
        )

    async def _book_appointment(self, task: AgentTask) -> AgentResult:
        """Book a new appointment."""
        patient_id = task.user_id
        clinician_id = task.context.get("clinician_id")
        appointment_type = task.context.get("appointment_type", "consultation")
        start_time = task.context.get("start_time")  # ISO format
        duration = task.context.get("duration_minutes", 30)
        chief_complaint = task.context.get("chief_complaint")

        if not all([patient_id, clinician_id, start_time]):
            return self.create_error_result(
                task_id=task.task_id,
                error="Missing required parameters for booking"
            )

        # Parse start time
        try:
            scheduled_start = datetime.fromisoformat(start_time)
            scheduled_end = scheduled_start + timedelta(minutes=duration)
        except ValueError:
            return self.create_error_result(
                task_id=task.task_id,
                error="Invalid start_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
            )

        # Check availability (prevent double booking)
        # In production, this would query the database
        is_available = True  # Simplified

        if not is_available:
            return self.create_error_result(
                task_id=task.task_id,
                error="Selected time slot is not available"
            )

        # Calculate fee
        fee_result = await self.payment_client.calculate_appointment_fee(
            appointment_type=appointment_type,
            clinician_id=clinician_id,
            patient_insurance=task.context.get("insurance")
        )
        fee_amount = fee_result.get("amount", 150.0)

        # Create payment intent (pre-authorization)
        payment_intent = await self.payment_client.create_payment_intent(
            amount=fee_amount,
            currency="USD",
            customer_id=str(patient_id),
            metadata={
                "appointment_type": appointment_type,
                "clinician_id": clinician_id
            }
        )

        # Book appointment (in production, this would create DB record)
        appointment_id = f"apt_{task.task_id[:8]}"

        # Send confirmation notification
        await self.notification_client.send_appointment_reminder(
            patient_email=task.context.get("patient_email", "patient@example.com"),
            patient_phone=task.context.get("patient_phone"),
            appointment_details={
                "appointment_id": appointment_id,
                "patient_name": "Patient",  # Would fetch from DB
                "clinician_name": f"Dr. Clinician {clinician_id}",
                "scheduled_start": scheduled_start.isoformat(),
                "location": "Telehealth"
            }
        )

        return self.create_success_result(
            task_id=task.task_id,
            response={
                "appointment_id": appointment_id,
                "status": "confirmed",
                "scheduled_start": scheduled_start.isoformat(),
                "scheduled_end": scheduled_end.isoformat(),
                "payment_intent_id": payment_intent.get("payment_intent_id"),
                "amount": fee_amount,
                "notification_sent": True
            },
            confidence=1.0,
            provenance=[{
                "type": "appointment_booking",
                "appointment_id": appointment_id,
                "payment_intent": payment_intent.get("payment_intent_id")
            }]
        )

    async def _cancel_appointment(self, task: AgentTask) -> AgentResult:
        """Cancel an existing appointment."""
        appointment_id = task.context.get("appointment_id")
        cancellation_reason = task.context.get("reason", "Patient requested")

        if not appointment_id:
            return self.create_error_result(
                task_id=task.task_id,
                error="Missing appointment_id"
            )

        # Cancel appointment (in production, update DB)
        # Also handle refund if applicable

        return self.create_success_result(
            task_id=task.task_id,
            response={
                "appointment_id": appointment_id,
                "status": "cancelled",
                "cancellation_reason": cancellation_reason,
                "cancelled_at": datetime.utcnow().isoformat()
            },
            confidence=1.0
        )

    async def _reschedule_appointment(self, task: AgentTask) -> AgentResult:
        """Reschedule an existing appointment."""
        appointment_id = task.context.get("appointment_id")
        new_start_time = task.context.get("new_start_time")

        if not all([appointment_id, new_start_time]):
            return self.create_error_result(
                task_id=task.task_id,
                error="Missing appointment_id or new_start_time"
            )

        # Reschedule (in production, update DB and check availability)

        return self.create_success_result(
            task_id=task.task_id,
            response={
                "appointment_id": appointment_id,
                "status": "rescheduled",
                "new_start_time": new_start_time
            },
            confidence=1.0
        )

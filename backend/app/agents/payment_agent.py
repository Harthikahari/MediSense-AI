"""
Payment Gateway Agent for handling payments and billing.
"""

from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentTask, AgentResult
from app.mcp_clients import PaymentMCPClient


class PaymentAgent(BaseAgent):
    """
    Payment agent for processing payments, refunds, and billing operations.
    Integrates with payment gateway in sandbox mode.
    """

    def __init__(self, payment_client: Optional[PaymentMCPClient] = None):
        """Initialize payment agent."""
        super().__init__("payment_agent")
        self.payment_client = payment_client or PaymentMCPClient()

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute payment-related operations.

        Args:
            task: Agent task with action (charge, refund, status)

        Returns:
            Payment operation result
        """
        try:
            action = task.context.get("action", "charge")

            if action == "create_intent":
                return await self._create_payment_intent(task)
            elif action == "charge":
                return await self._process_payment(task)
            elif action == "refund":
                return await self._process_refund(task)
            elif action == "status":
                return await self._get_payment_status(task)
            else:
                return self.create_error_result(
                    task_id=task.task_id,
                    error=f"Unknown action: {action}"
                )

        except Exception as e:
            self.logger.error(f"Payment agent failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"Payment operation failed: {str(e)}"
            )

    async def _create_payment_intent(self, task: AgentTask) -> AgentResult:
        """Create a payment intent for pre-authorization."""
        amount = task.context.get("amount")
        currency = task.context.get("currency", "USD")
        customer_id = task.context.get("customer_id")

        if not amount:
            return self.create_error_result(
                task_id=task.task_id,
                error="Missing required parameter: amount"
            )

        result = await self.payment_client.create_payment_intent(
            amount=amount,
            currency=currency,
            customer_id=customer_id,
            metadata=task.context.get("metadata", {})
        )

        return self.create_success_result(
            task_id=task.task_id,
            response=result,
            confidence=1.0
        )

    async def _process_payment(self, task: AgentTask) -> AgentResult:
        """Process a payment using payment intent."""
        payment_intent_id = task.context.get("payment_intent_id")
        payment_method = task.context.get("payment_method", "card")

        if not payment_intent_id:
            return self.create_error_result(
                task_id=task.task_id,
                error="Missing required parameter: payment_intent_id"
            )

        result = await self.payment_client.process_payment(
            payment_intent_id=payment_intent_id,
            payment_method=payment_method,
            billing_details=task.context.get("billing_details")
        )

        return self.create_success_result(
            task_id=task.task_id,
            response=result,
            confidence=1.0,
            provenance=[{
                "type": "payment_transaction",
                "transaction_id": result.get("transaction_id"),
                "payment_intent_id": payment_intent_id
            }]
        )

    async def _process_refund(self, task: AgentTask) -> AgentResult:
        """Process a payment refund."""
        transaction_id = task.context.get("transaction_id")
        amount = task.context.get("amount")
        reason = task.context.get("reason")

        if not transaction_id:
            return self.create_error_result(
                task_id=task.task_id,
                error="Missing required parameter: transaction_id"
            )

        result = await self.payment_client.refund_payment(
            transaction_id=transaction_id,
            amount=amount,
            reason=reason
        )

        return self.create_success_result(
            task_id=task.task_id,
            response=result,
            confidence=1.0,
            provenance=[{
                "type": "payment_refund",
                "transaction_id": transaction_id,
                "refund_id": result.get("refund_id")
            }]
        )

    async def _get_payment_status(self, task: AgentTask) -> AgentResult:
        """Get payment transaction status."""
        transaction_id = task.context.get("transaction_id")

        if not transaction_id:
            return self.create_error_result(
                task_id=task.task_id,
                error="Missing required parameter: transaction_id"
            )

        result = await self.payment_client.get_payment_status(transaction_id)

        return self.create_success_result(
            task_id=task.task_id,
            response=result,
            confidence=1.0
        )

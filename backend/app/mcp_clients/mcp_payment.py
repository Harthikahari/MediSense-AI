"""
MCP Payment client for payment gateway integration (sandbox mode).
"""

from typing import Any, Dict, Optional
from .mcp_base import ToolClient, get_mcp_client
from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)


class PaymentMCPClient:
    """
    MCP client for payment operations.
    Supports sandbox payment processing for testing.
    """

    def __init__(self, client: Optional[ToolClient] = None):
        """
        Initialize payment MCP client.

        Args:
            client: Optional MCP client instance
        """
        self.client = client or get_mcp_client()
        self.mode = settings.PAYMENT_MODE

    async def create_payment_intent(
        self,
        amount: float,
        currency: str = "USD",
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a payment intent for pre-authorization.

        Args:
            amount: Payment amount
            currency: Currency code
            customer_id: Optional customer identifier
            metadata: Additional metadata

        Returns:
            Payment intent details
        """
        payload = {
            "amount": amount,
            "currency": currency,
            "customer_id": customer_id,
            "metadata": metadata or {},
            "mode": self.mode
        }

        logger.info("Creating payment intent", amount=amount, currency=currency)
        result = await self.client.call_tool("create_payment_intent", payload)
        return result

    async def process_payment(
        self,
        payment_intent_id: str,
        payment_method: str,
        billing_details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a payment using payment intent.

        Args:
            payment_intent_id: Payment intent identifier
            payment_method: Payment method (e.g., 'card', 'bank_account')
            billing_details: Billing address and details

        Returns:
            Payment processing result
        """
        payload = {
            "payment_intent_id": payment_intent_id,
            "payment_method": payment_method,
            "billing_details": billing_details or {},
            "mode": self.mode
        }

        logger.info("Processing payment", payment_intent_id=payment_intent_id)
        result = await self.client.call_tool("process_payment", payload)
        return result

    async def refund_payment(
        self,
        transaction_id: str,
        amount: Optional[float] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Refund a payment (full or partial).

        Args:
            transaction_id: Original transaction ID
            amount: Refund amount (None for full refund)
            reason: Refund reason

        Returns:
            Refund result
        """
        payload = {
            "transaction_id": transaction_id,
            "amount": amount,
            "reason": reason,
            "mode": self.mode
        }

        logger.info("Refunding payment", transaction_id=transaction_id, amount=amount)
        result = await self.client.call_tool("refund_payment", payload)
        return result

    async def get_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get status of a payment transaction.

        Args:
            transaction_id: Transaction identifier

        Returns:
            Payment status and details
        """
        payload = {
            "transaction_id": transaction_id,
            "mode": self.mode
        }

        logger.info("Getting payment status", transaction_id=transaction_id)
        result = await self.client.call_tool("get_payment_status", payload)
        return result

    async def create_customer(
        self,
        email: str,
        name: str,
        phone: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a customer profile in payment system.

        Args:
            email: Customer email
            name: Customer name
            phone: Customer phone
            metadata: Additional metadata

        Returns:
            Customer profile details
        """
        payload = {
            "email": email,
            "name": name,
            "phone": phone,
            "metadata": metadata or {},
            "mode": self.mode
        }

        logger.info("Creating customer profile", email=email)
        result = await self.client.call_tool("create_customer", payload)
        return result

    async def attach_payment_method(
        self,
        customer_id: str,
        payment_method_type: str,
        payment_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Attach a payment method to customer profile.

        Args:
            customer_id: Customer identifier
            payment_method_type: Type of payment method
            payment_details: Payment method details

        Returns:
            Payment method attachment result
        """
        payload = {
            "customer_id": customer_id,
            "payment_method_type": payment_method_type,
            "payment_details": payment_details,
            "mode": self.mode
        }

        logger.info("Attaching payment method", customer_id=customer_id)
        result = await self.client.call_tool("attach_payment_method", payload)
        return result

    async def calculate_appointment_fee(
        self,
        appointment_type: str,
        clinician_id: int,
        patient_insurance: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate appointment fee based on type and insurance.

        Args:
            appointment_type: Type of appointment
            clinician_id: Clinician ID
            patient_insurance: Insurance information

        Returns:
            Fee calculation details
        """
        payload = {
            "appointment_type": appointment_type,
            "clinician_id": clinician_id,
            "patient_insurance": patient_insurance or {},
            "mode": self.mode
        }

        logger.info("Calculating appointment fee", appointment_type=appointment_type)
        result = await self.client.call_tool("calculate_appointment_fee", payload)
        return result

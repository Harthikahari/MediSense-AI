"""
MCP (Model Context Protocol) routes for direct MCP client access.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.api.v1.routes_auth import get_current_user_id
from app.mcp_clients import (
    DocumentMCPClient,
    DatabaseMCPClient,
    ModelMCPClient,
    PaymentMCPClient,
    NotificationMCPClient
)
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

# Initialize MCP clients
document_client = DocumentMCPClient()
db_client = DatabaseMCPClient()
model_client = ModelMCPClient()
payment_client = PaymentMCPClient()
notification_client = NotificationMCPClient()


@router.get("/status")
async def mcp_status():
    """Get MCP system status."""
    from app.core.config import settings

    return {
        "mode": settings.MCP_MODE,
        "host": settings.MCP_HOST,
        "timeout": settings.MCP_TIMEOUT,
        "available_clients": [
            "document",
            "database",
            "model",
            "payment",
            "notification"
        ]
    }


@router.post("/document/search")
async def search_documents(
    query: str,
    top_k: int = 5,
    filters: Dict[str, Any] = None,
    user_id: int = Depends(get_current_user_id)
):
    """Search documents."""
    try:
        results = await document_client.search_documents(
            query=query,
            filters=filters,
            top_k=top_k
        )
        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Document search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/document/ocr")
async def ocr_document(
    image_path: str,
    language: str = "eng",
    user_id: int = Depends(get_current_user_id)
):
    """Perform OCR on document image."""
    try:
        result = await document_client.ocr_document(
            image_path=image_path,
            language=language
        )
        return result
    except Exception as e:
        logger.error(f"OCR failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/model/classify")
async def classify_image(
    image_data: str,
    model_name: str = "symptom_classifier",
    top_k: int = 3,
    user_id: int = Depends(get_current_user_id)
):
    """Classify image using ONNX model."""
    try:
        result = await model_client.classify_image(
            image_data=image_data,
            model_name=model_name,
            top_k=top_k
        )
        return result
    except Exception as e:
        logger.error(f"Image classification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/payment/create-intent")
async def create_payment_intent(
    amount: float,
    currency: str = "USD",
    metadata: Dict[str, Any] = None,
    user_id: int = Depends(get_current_user_id)
):
    """Create a payment intent."""
    try:
        result = await payment_client.create_payment_intent(
            amount=amount,
            currency=currency,
            customer_id=str(user_id),
            metadata=metadata
        )
        return result
    except Exception as e:
        logger.error(f"Payment intent creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notification/email")
async def send_email(
    to_email: str,
    subject: str,
    body: str,
    template_name: str = None,
    user_id: int = Depends(get_current_user_id)
):
    """Send email notification."""
    try:
        result = await notification_client.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            template_name=template_name
        )
        return result
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notification/sms")
async def send_sms(
    to_phone: str,
    message: str,
    user_id: int = Depends(get_current_user_id)
):
    """Send SMS notification."""
    try:
        result = await notification_client.send_sms(
            to_phone=to_phone,
            message=message
        )
        return result
    except Exception as e:
        logger.error(f"SMS sending failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

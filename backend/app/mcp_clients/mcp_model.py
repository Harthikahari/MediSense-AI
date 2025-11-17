"""
MCP Model client for ONNX inference and image analysis.
"""

from typing import Any, Dict, List, Optional
import base64
from .mcp_base import ToolClient, get_mcp_client
from app.core.logger import get_logger

logger = get_logger(__name__)


class ModelMCPClient:
    """
    MCP client for ML model inference operations.
    Supports ONNX models for image classification and segmentation.
    """

    def __init__(self, client: Optional[ToolClient] = None):
        """
        Initialize model MCP client.

        Args:
            client: Optional MCP client instance
        """
        self.client = client or get_mcp_client()

    async def classify_image(
        self,
        image_data: str,
        model_name: str = "symptom_classifier",
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Classify an image using ONNX model.

        Args:
            image_data: Base64-encoded image or image path
            model_name: Name of the model to use
            top_k: Number of top predictions to return

        Returns:
            Classification results with confidence scores
        """
        payload = {
            "image_data": image_data,
            "model_name": model_name,
            "top_k": top_k
        }

        logger.info("Classifying image", model_name=model_name, top_k=top_k)
        result = await self.client.call_tool("classify_image", payload)
        return result

    async def segment_image(
        self,
        image_data: str,
        model_name: str = "lesion_segmentation"
    ) -> Dict[str, Any]:
        """
        Perform image segmentation.

        Args:
            image_data: Base64-encoded image or image path
            model_name: Name of the segmentation model

        Returns:
            Segmentation mask and bounding boxes
        """
        payload = {
            "image_data": image_data,
            "model_name": model_name
        }

        logger.info("Segmenting image", model_name=model_name)
        result = await self.client.call_tool("segment_image", payload)
        return result

    async def detect_objects(
        self,
        image_data: str,
        model_name: str = "medical_object_detection",
        confidence_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Detect objects in an image.

        Args:
            image_data: Base64-encoded image or image path
            model_name: Name of the detection model
            confidence_threshold: Minimum confidence for detections

        Returns:
            List of detected objects with bounding boxes
        """
        payload = {
            "image_data": image_data,
            "model_name": model_name,
            "confidence_threshold": confidence_threshold
        }

        logger.info("Detecting objects", model_name=model_name, threshold=confidence_threshold)
        result = await self.client.call_tool("detect_objects", payload)
        return result.get("detections", [])

    async def analyze_symptom_image(
        self,
        image_data: str,
        symptoms: Optional[List[str]] = None,
        patient_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive symptom image analysis combining multiple models.

        Args:
            image_data: Base64-encoded image
            symptoms: List of reported symptoms
            patient_context: Additional patient context

        Returns:
            Comprehensive analysis including classification, segmentation, and recommendations
        """
        payload = {
            "image_data": image_data,
            "symptoms": symptoms or [],
            "patient_context": patient_context or {}
        }

        logger.info("Analyzing symptom image", symptoms=symptoms)
        result = await self.client.call_tool("analyze_symptom_image", payload)
        return result

    async def generate_embedding(
        self,
        text: str,
        model_name: str = "clinical_bert"
    ) -> List[float]:
        """
        Generate text embedding using specified model.

        Args:
            text: Input text
            model_name: Name of the embedding model

        Returns:
            Embedding vector
        """
        payload = {
            "text": text,
            "model_name": model_name
        }

        logger.info("Generating embedding", text_length=len(text))
        result = await self.client.call_tool("generate_embedding", payload)
        return result.get("embedding", [])

    async def batch_classify_images(
        self,
        images: List[str],
        model_name: str = "symptom_classifier"
    ) -> List[Dict[str, Any]]:
        """
        Classify multiple images in batch.

        Args:
            images: List of base64-encoded images
            model_name: Name of the model to use

        Returns:
            List of classification results
        """
        payload = {
            "images": images,
            "model_name": model_name
        }

        logger.info("Batch classifying images", count=len(images))
        result = await self.client.call_tool("batch_classify_images", payload)
        return result.get("results", [])

    def encode_image_to_base64(self, image_path: str) -> str:
        """
        Encode image file to base64 string.

        Args:
            image_path: Path to image file

        Returns:
            Base64-encoded image string
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded
        except Exception as e:
            logger.error(f"Failed to encode image: {str(e)}")
            raise

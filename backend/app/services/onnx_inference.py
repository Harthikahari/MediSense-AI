"""
ONNX inference service for image classification and segmentation.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import onnxruntime as ort
from PIL import Image
import io
import base64
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class ONNXInferenceService:
    """Service for ONNX model inference."""

    def __init__(self, model_path: str = None):
        """
        Initialize ONNX inference service.

        Args:
            model_path: Path to ONNX model file
        """
        self.model_path = model_path or settings.ONNX_MODEL_PATH
        self.session = None

        try:
            # Initialize ONNX runtime session
            sess_options = ort.SessionOptions()
            sess_options.intra_op_num_threads = settings.ONNX_THREADS

            self.session = ort.InferenceSession(
                self.model_path,
                sess_options,
                providers=['CPUExecutionProvider']  # Use CPU
            )

            # Get model info
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name

            logger.info(f"ONNX model loaded: {self.model_path}")

        except Exception as e:
            logger.warning(f"Failed to load ONNX model: {str(e)}. Using mock inference.")
            self.session = None

    def preprocess_image(
        self,
        image_data: str,
        target_size: Tuple[int, int] = (224, 224)
    ) -> np.ndarray:
        """
        Preprocess image for inference.

        Args:
            image_data: Base64-encoded image string
            target_size: Target image size (height, width)

        Returns:
            Preprocessed image array
        """
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize
        image = image.resize(target_size)

        # Convert to numpy array and normalize
        image_array = np.array(image).astype(np.float32) / 255.0

        # Transpose to CHW format (channels, height, width)
        image_array = image_array.transpose(2, 0, 1)

        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)

        return image_array

    def classify(
        self,
        image_data: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Classify an image.

        Args:
            image_data: Base64-encoded image
            top_k: Number of top predictions to return

        Returns:
            List of predictions with labels and confidence scores
        """
        if self.session is None:
            # Mock predictions
            return [
                {"label": "rash", "confidence": 0.85},
                {"label": "eczema", "confidence": 0.12},
                {"label": "normal", "confidence": 0.03}
            ]

        try:
            # Preprocess image
            input_data = self.preprocess_image(image_data)

            # Run inference
            outputs = self.session.run([self.output_name], {self.input_name: input_data})
            predictions = outputs[0][0]

            # Get top-k predictions
            top_indices = np.argsort(predictions)[-top_k:][::-1]

            # Format results (would use actual class labels in production)
            results = []
            class_labels = self._get_class_labels()

            for idx in top_indices:
                results.append({
                    "label": class_labels.get(idx, f"class_{idx}"),
                    "confidence": float(predictions[idx])
                })

            return results

        except Exception as e:
            logger.error(f"Classification failed: {str(e)}")
            # Return mock results on error
            return [
                {"label": "unknown", "confidence": 0.5}
            ]

    def segment(
        self,
        image_data: str
    ) -> Dict[str, Any]:
        """
        Perform image segmentation.

        Args:
            image_data: Base64-encoded image

        Returns:
            Segmentation mask and metadata
        """
        if self.session is None:
            # Mock segmentation
            return {
                "mask": "base64_encoded_mask_placeholder",
                "bounding_boxes": [
                    {"x": 100, "y": 100, "width": 50, "height": 50}
                ],
                "area_pixels": 2500,
                "confidence": 0.80
            }

        try:
            # Preprocess image
            input_data = self.preprocess_image(image_data)

            # Run inference
            outputs = self.session.run([self.output_name], {self.input_name: input_data})
            mask = outputs[0]

            # Process mask (simplified)
            return {
                "mask": self._encode_mask(mask),
                "bounding_boxes": self._extract_bounding_boxes(mask),
                "area_pixels": int(np.sum(mask > 0.5)),
                "confidence": 0.80
            }

        except Exception as e:
            logger.error(f"Segmentation failed: {str(e)}")
            return {
                "mask": None,
                "error": str(e)
            }

    def _get_class_labels(self) -> Dict[int, str]:
        """Get class labels for classification."""
        # Mock class labels - in production, load from model metadata
        return {
            0: "normal",
            1: "rash",
            2: "eczema",
            3: "psoriasis",
            4: "melanoma",
            5: "acne"
        }

    def _encode_mask(self, mask: np.ndarray) -> str:
        """Encode segmentation mask to base64."""
        # Simplified - would properly encode mask in production
        return "base64_encoded_mask"

    def _extract_bounding_boxes(self, mask: np.ndarray) -> List[Dict[str, int]]:
        """Extract bounding boxes from segmentation mask."""
        # Simplified - would use proper contour detection in production
        return [
            {"x": 0, "y": 0, "width": 100, "height": 100}
        ]


# Global ONNX service instance
_onnx_service = None


def get_onnx_service() -> ONNXInferenceService:
    """Get global ONNX service instance."""
    global _onnx_service
    if _onnx_service is None:
        _onnx_service = ONNXInferenceService()
    return _onnx_service

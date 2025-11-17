"""
Image Understanding Agent for symptom photo analysis using ONNX models.
"""

from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent, AgentTask, AgentResult
from app.mcp_clients import ModelMCPClient


class ImageAgent(BaseAgent):
    """
    Image understanding agent for analyzing symptom photos.
    Uses ONNX models for classification and segmentation.
    """

    def __init__(self, model_client: Optional[ModelMCPClient] = None):
        """Initialize image agent."""
        super().__init__("image_agent")
        self.model_client = model_client or ModelMCPClient()

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute image analysis.

        Args:
            task: Agent task with image data and analysis type

        Returns:
            Image analysis results
        """
        try:
            image_data = task.context.get("image_data")
            image_path = task.context.get("image_path")
            analysis_type = task.context.get("analysis_type", "symptom_classification")

            if not image_data and not image_path:
                return self.create_error_result(
                    task_id=task.task_id,
                    error="Missing image_data or image_path"
                )

            # Convert image_path to base64 if provided
            if image_path and not image_data:
                image_data = self.model_client.encode_image_to_base64(image_path)

            # Perform analysis based on type
            if analysis_type == "symptom_classification":
                return await self._classify_symptom(task, image_data)
            elif analysis_type == "lesion_segmentation":
                return await self._segment_lesion(task, image_data)
            elif analysis_type == "comprehensive":
                return await self._comprehensive_analysis(task, image_data)
            else:
                return self.create_error_result(
                    task_id=task.task_id,
                    error=f"Unknown analysis type: {analysis_type}"
                )

        except Exception as e:
            self.logger.error(f"Image agent failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"Image analysis failed: {str(e)}"
            )

    async def _classify_symptom(self, task: AgentTask, image_data: str) -> AgentResult:
        """Classify symptom in image."""
        self.logger.info("Classifying symptom image")

        result = await self.model_client.classify_image(
            image_data=image_data,
            model_name="symptom_classifier",
            top_k=3
        )

        predictions = result.get("predictions", [])

        return self.create_success_result(
            task_id=task.task_id,
            response={
                "analysis_type": "symptom_classification",
                "predictions": predictions,
                "top_prediction": predictions[0] if predictions else None,
                "confidence_scores": [p.get("confidence", 0) for p in predictions],
                "recommendations": self._generate_recommendations(predictions)
            },
            confidence=predictions[0].get("confidence", 0) if predictions else 0,
            provenance=[{
                "type": "ml_inference",
                "model": "symptom_classifier",
                "timestamp": result.get("timestamp")
            }]
        )

    async def _segment_lesion(self, task: AgentTask, image_data: str) -> AgentResult:
        """Perform lesion segmentation."""
        self.logger.info("Segmenting lesion in image")

        result = await self.model_client.segment_image(
            image_data=image_data,
            model_name="lesion_segmentation"
        )

        return self.create_success_result(
            task_id=task.task_id,
            response={
                "analysis_type": "lesion_segmentation",
                "segmentation_mask": result.get("mask"),
                "bounding_boxes": result.get("bounding_boxes", []),
                "lesion_area": result.get("area_pixels"),
                "characteristics": result.get("characteristics", {})
            },
            confidence=result.get("confidence", 0.8),
            provenance=[{
                "type": "ml_inference",
                "model": "lesion_segmentation",
                "timestamp": result.get("timestamp")
            }]
        )

    async def _comprehensive_analysis(self, task: AgentTask, image_data: str) -> AgentResult:
        """Perform comprehensive symptom analysis."""
        self.logger.info("Performing comprehensive image analysis")

        symptoms = task.context.get("symptoms", [])
        patient_context = task.context.get("patient_context", {})

        result = await self.model_client.analyze_symptom_image(
            image_data=image_data,
            symptoms=symptoms,
            patient_context=patient_context
        )

        return self.create_success_result(
            task_id=task.task_id,
            response=result,
            confidence=result.get("confidence", 0.7),
            provenance=[{
                "type": "ml_inference",
                "models": result.get("models_used", []),
                "timestamp": result.get("timestamp")
            }]
        )

    def _generate_recommendations(self, predictions: List[Dict[str, Any]]) -> List[str]:
        """
        Generate clinical recommendations based on predictions.

        Args:
            predictions: Model predictions

        Returns:
            List of recommendations
        """
        if not predictions:
            return ["Unable to provide recommendations without analysis results."]

        top_prediction = predictions[0]
        label = top_prediction.get("label", "unknown")
        confidence = top_prediction.get("confidence", 0)

        recommendations = []

        if confidence > 0.8:
            recommendations.append(f"High confidence detection of {label}. Consult with a healthcare provider.")
        elif confidence > 0.5:
            recommendations.append(f"Possible {label} detected. Further clinical evaluation recommended.")
        else:
            recommendations.append("Low confidence in automated analysis. Professional medical evaluation strongly recommended.")

        # Add general recommendations
        recommendations.append("This analysis is not a substitute for professional medical advice.")
        recommendations.append("Schedule an appointment with a dermatologist for definitive diagnosis.")

        return recommendations

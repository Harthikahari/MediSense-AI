"""
Guardrail Agent for enforcing safety policies and PHI/PII redaction.
"""

from typing import Dict, Any, List, Optional
import re
from .base_agent import BaseAgent, AgentTask, AgentResult
from app.core.security import redact_phi, redact_phi_dict
from app.core.config import settings


class GuardrailAgent(BaseAgent):
    """
    Guardrail agent for enforcing safety policies, content filtering, and PHI redaction.
    Acts as a policy enforcement layer for all agent outputs.
    """

    def __init__(self):
        """Initialize guardrail agent."""
        super().__init__("guardrail_agent")

        # Define safety policies
        self.policies = {
            "phi_redaction": {
                "enabled": settings.PHI_REDACTION_ENABLED,
                "severity": "critical"
            },
            "unsafe_content": {
                "enabled": True,
                "severity": "high"
            },
            "medical_advice_disclaimer": {
                "enabled": True,
                "severity": "medium"
            },
            "prescription_validation": {
                "enabled": True,
                "severity": "high"
            }
        }

        # Unsafe content patterns
        self.unsafe_patterns = [
            r"end.*life",
            r"harm.*self",
            r"suicide",
            r"illegal.*drug",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute guardrail policy enforcement.

        Args:
            task: Agent task with content to check

        Returns:
            Validation result with any violations
        """
        try:
            content = task.context.get("content", "")
            content_type = task.context.get("content_type", "text")
            agent_name = task.context.get("source_agent", "unknown")

            violations = []

            # Check each policy
            if self.policies["phi_redaction"]["enabled"]:
                phi_violations = self._check_phi_exposure(content)
                violations.extend(phi_violations)

            if self.policies["unsafe_content"]["enabled"]:
                unsafe_violations = self._check_unsafe_content(content)
                violations.extend(unsafe_violations)

            if self.policies["medical_advice_disclaimer"]["enabled"]:
                disclaimer_violations = self._check_disclaimer(content)
                violations.extend(disclaimer_violations)

            # Apply redaction to content
            redacted_content = self._apply_guardrails(content, violations)

            # Determine if content should be blocked
            should_block = any(v["severity"] == "critical" for v in violations)

            return self.create_success_result(
                task_id=task.task_id,
                response={
                    "passed": len(violations) == 0,
                    "should_block": should_block,
                    "violations": violations,
                    "redacted_content": redacted_content,
                    "original_length": len(content),
                    "redacted_length": len(redacted_content)
                },
                confidence=1.0,
                metadata={
                    "source_agent": agent_name,
                    "policies_checked": len(self.policies)
                }
            )

        except Exception as e:
            self.logger.error(f"Guardrail agent failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"Guardrail enforcement failed: {str(e)}"
            )

    def _check_phi_exposure(self, content: str) -> List[Dict[str, Any]]:
        """Check for PHI/PII exposure."""
        violations = []

        # Check for common PHI patterns
        phi_patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "date_of_birth": r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        }

        for phi_type, pattern in phi_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                violations.append({
                    "policy": "phi_redaction",
                    "violation_type": f"phi_exposure_{phi_type}",
                    "severity": "critical",
                    "description": f"Found {len(matches)} instances of {phi_type}",
                    "action": "redact"
                })

        return violations

    def _check_unsafe_content(self, content: str) -> List[Dict[str, Any]]:
        """Check for unsafe content."""
        violations = []

        for pattern in self.unsafe_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append({
                    "policy": "unsafe_content",
                    "violation_type": "harmful_content",
                    "severity": "high",
                    "description": f"Content matches unsafe pattern: {pattern}",
                    "action": "block"
                })

        return violations

    def _check_disclaimer(self, content: str) -> List[Dict[str, Any]]:
        """Check if medical advice has appropriate disclaimer."""
        violations = []

        # Keywords that indicate medical advice
        medical_keywords = ["diagnos", "treat", "prescri", "medicati", "therap"]

        contains_medical_advice = any(
            keyword in content.lower() for keyword in medical_keywords
        )

        disclaimer_keywords = ["not a substitute", "consult", "healthcare provider", "medical professional"]
        has_disclaimer = any(
            keyword in content.lower() for keyword in disclaimer_keywords
        )

        if contains_medical_advice and not has_disclaimer:
            violations.append({
                "policy": "medical_advice_disclaimer",
                "violation_type": "missing_disclaimer",
                "severity": "medium",
                "description": "Medical advice without appropriate disclaimer",
                "action": "append_disclaimer"
            })

        return violations

    def _apply_guardrails(
        self,
        content: str,
        violations: List[Dict[str, Any]]
    ) -> str:
        """
        Apply guardrail actions to content.

        Args:
            content: Original content
            violations: List of violations

        Returns:
            Modified content with guardrails applied
        """
        modified_content = content

        # Apply redaction for PHI violations
        if any(v["action"] == "redact" for v in violations):
            modified_content = redact_phi(modified_content)

        # Block content if critical violations
        if any(v["severity"] == "critical" and v["action"] == "block" for v in violations):
            return "[CONTENT BLOCKED: Policy violation detected]"

        # Append disclaimer if needed
        if any(v["action"] == "append_disclaimer" for v in violations):
            disclaimer = (
                "\n\n[Disclaimer: This information is not a substitute for professional medical advice. "
                "Always consult with a qualified healthcare provider for medical decisions.]"
            )
            modified_content += disclaimer

        return modified_content

    def validate_agent_output(
        self,
        agent_name: str,
        output: Any
    ) -> Dict[str, Any]:
        """
        Validate agent output against policies.

        Args:
            agent_name: Name of the source agent
            output: Agent output to validate

        Returns:
            Validation result
        """
        # Convert output to string for analysis
        if isinstance(output, dict):
            output_str = str(output)
        else:
            output_str = str(output)

        # Check policies
        violations = []

        if self.policies["phi_redaction"]["enabled"]:
            violations.extend(self._check_phi_exposure(output_str))

        if self.policies["unsafe_content"]["enabled"]:
            violations.extend(self._check_unsafe_content(output_str))

        return {
            "agent": agent_name,
            "passed": len(violations) == 0,
            "violations": violations
        }

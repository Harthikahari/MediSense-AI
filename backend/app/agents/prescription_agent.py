"""
Prescription Generation Agent for creating validated e-prescriptions.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from .base_agent import BaseAgent, AgentTask, AgentResult


class PrescriptionAgent(BaseAgent):
    """
    Prescription generation agent for drafting e-prescriptions with validation.
    Includes drug interaction checking and provenance tracking.
    """

    def __init__(self):
        """Initialize prescription agent."""
        super().__init__("prescription_agent")

        # Simple drug interaction database (in production, use comprehensive drug DB)
        self.drug_interactions = {
            ("warfarin", "aspirin"): "Increased bleeding risk",
            ("metformin", "alcohol"): "Risk of lactic acidosis",
            ("lisinopril", "potassium"): "Risk of hyperkalemia",
        }

        # Common medications database
        self.medications_db = {
            "amoxicillin": {
                "generic": "amoxicillin",
                "brand": "Amoxil",
                "category": "antibiotic",
                "common_dosages": ["250mg", "500mg"]
            },
            "metformin": {
                "generic": "metformin",
                "brand": "Glucophage",
                "category": "diabetes",
                "common_dosages": ["500mg", "850mg", "1000mg"]
            },
            "lisinopril": {
                "generic": "lisinopril",
                "brand": "Prinivil",
                "category": "blood_pressure",
                "common_dosages": ["5mg", "10mg", "20mg"]
            }
        }

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute prescription generation.

        Args:
            task: Agent task with diagnosis and patient info

        Returns:
            Generated prescription with validation
        """
        try:
            patient_id = task.user_id
            diagnosis = task.context.get("diagnosis")
            symptoms = task.context.get("symptoms", [])
            allergies = task.context.get("allergies", [])
            current_medications = task.context.get("current_medications", [])

            if not diagnosis:
                return self.create_error_result(
                    task_id=task.task_id,
                    error="Missing required parameter: diagnosis"
                )

            # Generate medication recommendations
            medications = self._recommend_medications(diagnosis, symptoms)

            # Check for drug interactions
            interactions = self._check_interactions(
                medications,
                current_medications
            )

            # Check for contraindications based on allergies
            contraindications = self._check_contraindications(
                medications,
                allergies
            )

            # Filter medications if contraindications found
            if contraindications:
                medications = [m for m in medications if m["name"] not in contraindications]

            # Generate prescription
            prescription_id = f"rx_{uuid.uuid4().hex[:12]}"

            prescription = {
                "prescription_id": prescription_id,
                "patient_id": patient_id,
                "diagnosis": diagnosis,
                "medications": medications,
                "instructions": self._generate_instructions(medications),
                "prescriber_id": task.context.get("prescriber_id", 1),
                "date_prescribed": datetime.utcnow().isoformat(),
                "interactions_checked": True,
                "interactions_found": interactions,
                "contraindications": contraindications,
                "valid_until": None,  # Would calculate expiration date
                "refills_allowed": 2
            }

            # Build provenance
            provenance = [{
                "type": "prescription_generation",
                "prescription_id": prescription_id,
                "diagnosis": diagnosis,
                "medications_count": len(medications),
                "interactions_checked": True
            }]

            return self.create_success_result(
                task_id=task.task_id,
                response=prescription,
                confidence=0.9 if not contraindications else 0.7,
                provenance=provenance
            )

        except Exception as e:
            self.logger.error(f"Prescription agent failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"Prescription generation failed: {str(e)}"
            )

    def _recommend_medications(
        self,
        diagnosis: str,
        symptoms: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Recommend medications based on diagnosis.

        Args:
            diagnosis: Patient diagnosis
            symptoms: List of symptoms

        Returns:
            List of recommended medications
        """
        diagnosis_lower = diagnosis.lower()

        # Simple rule-based recommendation (in production, use clinical decision support system)
        medications = []

        if "infection" in diagnosis_lower or "bacterial" in diagnosis_lower:
            medications.append({
                "name": "amoxicillin",
                "dosage": "500mg",
                "frequency": "3 times daily",
                "duration": "10 days",
                "instructions": "Take with food to reduce stomach upset"
            })

        if "diabetes" in diagnosis_lower or "hyperglycemia" in diagnosis_lower:
            medications.append({
                "name": "metformin",
                "dosage": "500mg",
                "frequency": "2 times daily",
                "duration": "ongoing",
                "instructions": "Take with meals"
            })

        if "hypertension" in diagnosis_lower or "high blood pressure" in diagnosis_lower:
            medications.append({
                "name": "lisinopril",
                "dosage": "10mg",
                "frequency": "once daily",
                "duration": "ongoing",
                "instructions": "Take in the morning"
            })

        # If no specific medications, add symptomatic treatment
        if not medications:
            medications.append({
                "name": "acetaminophen",
                "dosage": "500mg",
                "frequency": "as needed",
                "duration": "short-term",
                "instructions": "For pain or fever. Do not exceed 4000mg per day"
            })

        return medications

    def _check_interactions(
        self,
        new_medications: List[Dict[str, Any]],
        current_medications: List[str]
    ) -> List[str]:
        """
        Check for drug interactions.

        Args:
            new_medications: New medications to prescribe
            current_medications: Current medications

        Returns:
            List of interaction warnings
        """
        interactions_found = []

        for new_med in new_medications:
            new_drug = new_med["name"].lower()
            for current_drug in current_medications:
                current_drug = current_drug.lower()

                # Check both directions
                interaction = (
                    self.drug_interactions.get((new_drug, current_drug)) or
                    self.drug_interactions.get((current_drug, new_drug))
                )

                if interaction:
                    interactions_found.append(
                        f"Interaction between {new_drug} and {current_drug}: {interaction}"
                    )

        return interactions_found

    def _check_contraindications(
        self,
        medications: List[Dict[str, Any]],
        allergies: List[str]
    ) -> List[str]:
        """
        Check for contraindications based on allergies.

        Args:
            medications: Medications to check
            allergies: Patient allergies

        Returns:
            List of contraindicated medications
        """
        contraindications = []

        for med in medications:
            med_name = med["name"].lower()
            med_info = self.medications_db.get(med_name, {})
            category = med_info.get("category", "")

            for allergy in allergies:
                allergy_lower = allergy.lower()

                # Check direct allergy match
                if allergy_lower in med_name or med_name in allergy_lower:
                    contraindications.append(med_name)

                # Check category-based contraindications
                if category == "antibiotic" and "penicillin" in allergy_lower:
                    if "cillin" in med_name:  # amoxicillin, etc.
                        contraindications.append(med_name)

        return list(set(contraindications))

    def _generate_instructions(self, medications: List[Dict[str, Any]]) -> str:
        """
        Generate general prescription instructions.

        Args:
            medications: List of medications

        Returns:
            General instructions string
        """
        instructions = []

        instructions.append("Take medications as prescribed by your healthcare provider.")
        instructions.append("Complete the full course of any antibiotics even if you feel better.")
        instructions.append("Contact your doctor if you experience side effects or symptoms worsen.")
        instructions.append("Store medications as directed on the label.")

        return " ".join(instructions)

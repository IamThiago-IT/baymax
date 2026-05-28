from __future__ import annotations

from dataclasses import dataclass


EMERGENCY_KEYWORDS = (
    "chest pain",
    "trouble breathing",
    "difficulty breathing",
    "can't breathe",
    "cannot breathe",
    "severe bleeding",
    "passed out",
    "fainted",
    "stroke",
    "one side",
    "suicidal",
    "kill myself",
)

MEDICAL_DIAGNOSIS_KEYWORDS = (
    "what disease do i have",
    "diagnose me",
    "what is my diagnosis",
    "prescribe",
    "which medicine should i take",
)


@dataclass(frozen=True)
class SafetyResult:
    level: str
    message: str


def assess_message(message: str) -> SafetyResult:
    normalized = message.lower().strip()

    if any(keyword in normalized for keyword in EMERGENCY_KEYWORDS):
        return SafetyResult(
            level="emergency",
            message=(
                "This could be urgent. Call local emergency services now or go to the nearest emergency department. "
                "If possible, have someone stay with you while you get help."
            ),
        )

    if any(keyword in normalized for keyword in MEDICAL_DIAGNOSIS_KEYWORDS):
        return SafetyResult(
            level="restricted",
            message=(
                "I can help with general health guidance and symptom triage, but I can't diagnose or prescribe. "
                "If you share your main symptoms, I can suggest safe next steps."
            ),
        )

    return SafetyResult(level="safe", message="")

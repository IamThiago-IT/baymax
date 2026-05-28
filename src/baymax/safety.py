from __future__ import annotations

from dataclasses import dataclass

from .i18n import t


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


def assess_message(message: str, language: str = "eng") -> SafetyResult:
    normalized = message.lower().strip()

    if any(keyword in normalized for keyword in EMERGENCY_KEYWORDS):
        return SafetyResult(
            level="emergency",
            message=t(
                language,
                "urgent_fallback",
            ),
        )

    if any(keyword in normalized for keyword in MEDICAL_DIAGNOSIS_KEYWORDS):
        return SafetyResult(
            level="restricted",
            message=(
                "I can help with general health guidance and symptom triage, but I can't diagnose or prescribe. "
                "If you share your main symptoms, I can suggest safe next steps."
            )
            if language == "eng"
            else (
                "Posso ajudar com orientações gerais de saúde e triagem de sintomas, mas não posso diagnosticar nem prescrever. "
                "Se você me disser os principais sintomas, posso sugerir próximos passos seguros."
            ),
        )

    return SafetyResult(level="safe", message="")

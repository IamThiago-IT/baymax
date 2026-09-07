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
    # PT-BR
    "dor no peito",
    "dificuldade para respirar",
    "não consigo respirar",
    "sangramento grave",
    "desmaiei",
    "suicida",
    "me matar",
)

MEDICAL_DIAGNOSIS_KEYWORDS = (
    "what disease do i have",
    "diagnose me",
    "what is my diagnosis",
    "prescribe",
    "which medicine should i take",
    # PT-BR
    "que doença eu tenho",
    "me diagnostique",
    "qual é o meu diagnóstico",
    "prescrever",
    "qual remédio devo tomar",
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
            message=t(language, "urgent_fallback"),
        )

    if any(keyword in normalized for keyword in MEDICAL_DIAGNOSIS_KEYWORDS):
        return SafetyResult(
            level="restricted",
            message=t(language, "restricted_message"),
        )

    return SafetyResult(level="safe", message="")

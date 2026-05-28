from __future__ import annotations

from dataclasses import dataclass, field

from .i18n import t
from .safety import SafetyResult, assess_message


def _extract_symptom_prompt(message: str) -> str:
    normalized = message.lower()

    if any(keyword in normalized for keyword in ("fever", "temperature")):
        return "fever"

    if any(keyword in normalized for keyword in ("cough", "sore throat", "throat")):
        return "cough"

    if any(keyword in normalized for keyword in ("headache", "migraine")):
        return "headache"

    if any(keyword in normalized for keyword in ("stomach", "nausea", "vomit", "diarrhea")):
        return "stomach"

    return "default_symptom"


@dataclass
class AssistantResponse:
    text: str
    safety: SafetyResult


@dataclass
class BaymaxAssistant:
    user_name: str | None = None
    language: str = "eng"
    history: list[tuple[str, str]] = field(default_factory=list)

    def greet(self) -> str:
        return t(self.language, "greeting")

    def respond(self, message: str) -> AssistantResponse:
        self.history.append(("user", message))

        safety = assess_message(message, self.language)
        if safety.level != "safe" and safety.message:
            reply = safety.message
        else:
            symptom_key = _extract_symptom_prompt(message)
            reply = (
                t(self.language, "general_reply", prompt=t(self.language, symptom_key), urgent=t(self.language, "urgent_fallback"))
            )

        self.history.append(("assistant", reply))
        return AssistantResponse(text=reply, safety=safety)

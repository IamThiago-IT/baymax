from __future__ import annotations

from dataclasses import dataclass, field

from .safety import SafetyResult, assess_message


def _extract_symptom_prompt(message: str) -> str:
    normalized = message.lower()

    if any(keyword in normalized for keyword in ("fever", "temperature")):
        return "How high is the fever, and how long has it been going on?"

    if any(keyword in normalized for keyword in ("cough", "sore throat", "throat")):
        return "Is the cough dry or productive, and do you have trouble breathing or swallowing?"

    if any(keyword in normalized for keyword in ("headache", "migraine")):
        return "Is the headache sudden or severe, and do you have vision changes, weakness, or vomiting?"

    if any(keyword in normalized for keyword in ("stomach", "nausea", "vomit", "diarrhea")):
        return "Are you able to keep fluids down, and do you have severe pain or blood in the vomit or stool?"

    return "Can you share your main symptom, how long it has been happening, and what makes it better or worse?"


@dataclass
class AssistantResponse:
    text: str
    safety: SafetyResult


@dataclass
class BaymaxAssistant:
    user_name: str | None = None
    history: list[tuple[str, str]] = field(default_factory=list)

    def greet(self) -> str:
        return (
            "Hello, I am Baymax. I can help with general health guidance, symptom triage, and safe next steps. "
            "Type 'exit' to leave the conversation."
        )

    def respond(self, message: str) -> AssistantResponse:
        self.history.append(("user", message))

        safety = assess_message(message)
        if safety.level != "safe" and safety.message:
            reply = safety.message
        else:
            reply = (
                f"I hear you. {_extract_symptom_prompt(message)} "
                "If symptoms are severe, worsening, or new chest pain or breathing trouble appears, seek urgent care."
            )

        self.history.append(("assistant", reply))
        return AssistantResponse(text=reply, safety=safety)

from __future__ import annotations

from dataclasses import dataclass, field

from .i18n import t
from .safety import SafetyResult, assess_message


# Keywords organized by symptom category and language.
# Each language key maps to a tuple of trigger phrases.
SYMPTOM_KEYWORDS: dict[str, dict[str, tuple[str, ...]]] = {
    "fever": {
        "eng": ("fever", "temperature"),
        "ptbr": ("febre", "temperatura"),
    },
    "cough": {
        "eng": ("cough", "sore throat", "throat"),
        "ptbr": ("tosse", "garganta", "catarro"),
    },
    "headache": {
        "eng": ("headache", "migraine"),
        "ptbr": ("dor de cabeça", "enxaqueca", "cefaleia"),
    },
    "stomach": {
        "eng": ("stomach", "nausea", "vomit", "diarrhea"),
        "ptbr": ("estômago", "náusea", "vômito", "diarreia", "barriga", "enjoo"),
    },
}


def _extract_symptom_prompt(message: str, language: str = "eng") -> str:
    """Return the symptom key that best matches *message* in *language*."""
    normalized = message.lower()
    for symptom_key, lang_keywords in SYMPTOM_KEYWORDS.items():
        keywords = lang_keywords.get(language) or lang_keywords.get("eng", ())
        if any(keyword in normalized for keyword in keywords):
            return symptom_key
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
    # Tracks which symptom categories have already been asked about so the
    # assistant can use the "follow_up" template instead of repeating itself.
    _seen_symptoms: set[str] = field(default_factory=set, init=False, repr=False)

    def greet(self) -> str:
        return t(self.language, "greeting")

    def respond(self, message: str) -> AssistantResponse:
        self.history.append(("user", message))

        safety = assess_message(message, self.language)
        if safety.level != "safe" and safety.message:
            reply = safety.message
        else:
            symptom_key = _extract_symptom_prompt(message, self.language)
            # Use a follow-up template when the symptom was already discussed.
            template_key = "follow_up" if symptom_key in self._seen_symptoms else "general_reply"
            self._seen_symptoms.add(symptom_key)
            reply = t(
                self.language,
                template_key,
                prompt=t(self.language, symptom_key),
                urgent=t(self.language, "urgent_fallback"),
            )

        self.history.append(("assistant", reply))
        return AssistantResponse(text=reply, safety=safety)

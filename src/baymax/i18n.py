from __future__ import annotations

import locale
import os

SUPPORTED_LANGUAGES = {"eng", "ptbr"}

STRINGS: dict[str, dict[str, str]] = {
    "eng": {
        "greeting": (
            "Hello, I am Baymax. I can help with general health "
            "guidance, symptom triage, and safe next steps. "
            "Type 'exit' to leave the conversation."
        ),
        "prompt": "You: ",
        "assistant_prefix": "Baymax: ",
        "exit": "Baymax: Take care. If symptoms worsen, get medical help promptly.",
        "urgent_fallback": (
            "If symptoms are severe, worsening, or new chest pain "
            "or breathing trouble appears, seek urgent care."
        ),
        "fever": "How high is the fever, and how long has it been going on?",
        "cough": (
            "Is the cough dry or productive, and do you have trouble "
            "breathing or swallowing?"
        ),
        "headache": (
            "Is the headache sudden or severe, and do you have vision "
            "changes, weakness, or vomiting?"
        ),
        "stomach": (
            "Are you able to keep fluids down, and do you have severe "
            "pain or blood in the vomit or stool?"
        ),
        "default_symptom": (
            "Can you share your main symptom, how long it has been "
            "happening, and what makes it better or worse?"
        ),
        "general_reply": "I hear you. {prompt} {urgent}",
        "follow_up": "Thanks for the update. {prompt} {urgent}",
        "restricted_message": (
            "I can help with general health guidance and symptom triage, "
            "but I can't diagnose or prescribe. "
            "If you share your main symptoms, I can suggest safe next steps."
        ),
        "farewell_check": (
            "Before you go, I want to make sure you're okay. "
            "Are you feeling alright?"
        ),
        "farewell_thanks": (
            "I'm glad to hear that. Take care, and don't hesitate to come "
            "back if you need anything. Goodbye! 💙"
        ),
        "farewell_stay": (
            "I'm here whenever you need me. What else can I help you with?"
        ),
    },
    "ptbr": {
        "greeting": (
            "Olá, eu sou o Baymax. Posso ajudar com orientações gerais de "
            "saúde, triagem de sintomas e próximos passos seguros. "
            "Digite 'exit' para sair da conversa."
        ),
        "prompt": "Você: ",
        "assistant_prefix": "Baymax: ",
        "exit": (
            "Baymax: Se cuida. Se os sintomas piorarem, procure atendimento "
            "médico rapidamente."
        ),
        "urgent_fallback": (
            "Se os sintomas forem graves, estiverem piorando, ou surgir dor "
            "no peito ou dificuldade para respirar, procure atendimento urgente."
        ),
        "fever": "Qual é a temperatura e há quanto tempo isso começou?",
        "cough": (
            "A tosse é seca ou com secreção? Você tem dificuldade para "
            "respirar ou engolir?"
        ),
        "headache": (
            "A dor de cabeça é súbita ou forte? Você tem alteração na visão, "
            "fraqueza ou vômitos?"
        ),
        "stomach": (
            "Você consegue manter líquidos? Tem dor forte ou sangue no vômito "
            "ou nas fezes?"
        ),
        "default_symptom": (
            "Pode me dizer qual é o principal sintoma, há quanto tempo ele "
            "acontece e o que melhora ou piora?"
        ),
        "general_reply": "Entendi. {prompt} {urgent}",
        "follow_up": "Obrigado pela atualização. {prompt} {urgent}",
        "restricted_message": (
            "Posso ajudar com orientações gerais de saúde e triagem de sintomas, "
            "mas não posso diagnosticar nem prescrever. "
            "Se você me disser os principais sintomas, posso sugerir próximos "
            "passos seguros."
        ),
        "farewell_check": (
            "Antes de ir, quero me certificar de que você está bem. "
            "Você está se sentindo bem?"
        ),
        "farewell_thanks": (
            "Fico feliz em saber disso. Se cuide, e não hesite em voltar se "
            "precisar de algo. Até logo! 💙"
        ),
        "farewell_stay": (
            "Estou aqui sempre que precisar. No que mais posso te ajudar?"
        ),
    },
}


def _normalize_locale(value: str | None) -> str:
    if not value:
        return ""

    normalized = value.strip().lower().replace("-", "_")

    if normalized.startswith(("pt", "portuguese")):
        return "ptbr"

    if normalized.startswith(("en", "english")):
        return "eng"

    return ""


def detect_language() -> str:
    candidates = [
        os.environ.get("BAYMAX_LANG"),
        os.environ.get("LANG"),
        os.environ.get("LC_ALL"),
        os.environ.get("LC_MESSAGES"),
    ]

    try:
        candidates.append(locale.getlocale()[0])
    except (ValueError, TypeError):
        candidates.append(None)

    for candidate in candidates:
        normalized = _normalize_locale(candidate)
        if normalized in SUPPORTED_LANGUAGES:
            return normalized

    return "eng"


def t(language: str, key: str, **kwargs: str) -> str:
    """Return the translated string for *key* in *language*.

    Falls back to English if the language is unsupported or the key is
    missing, and returns a safe placeholder instead of raising ``KeyError``.
    """
    selected_language = language if language in SUPPORTED_LANGUAGES else "eng"
    template = STRINGS[selected_language].get(key) or STRINGS["eng"].get(key)
    if template is None:
        return f"[missing: {key}]"
    return template.format(**kwargs)

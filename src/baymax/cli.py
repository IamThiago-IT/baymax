from __future__ import annotations

from .assistant import BaymaxAssistant
from .i18n import SUPPORTED_LANGUAGES, detect_language, t

# Respostas consideradas afirmativas por idioma.
# Verificadas por substring para cobrir variações naturais de frase.
_AFFIRMATIVE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "eng": (
        "yes",
        "yeah",
        "yep",
        "yup",
        "fine",
        "okay",
        "ok",
        "good",
        "great",
        "alright",
        "well",
        "better",
        "i'm fine",
        "i'm ok",
        "i'm okay",
        "i'm well",
        "i am fine",
        "i am ok",
        "feeling good",
        "feeling better",
    ),
    "ptbr": (
        "sim",
        "tudo bem",
        "tudo bom",
        "estou bem",
        "me sinto bem",
        "ok",
        "ok",
        "ótimo",
        "ótima",
        "bom",
        "bem",
        "melhor",
        "estou ótimo",
        "estou ótima",
        "tô bem",
        "me sinto ótimo",
    ),
}


def _is_affirmative(response: str, language: str) -> bool:
    """Return True if *response* expresses that the user is feeling okay."""
    normalized = response.lower().strip()
    lang = language if language in SUPPORTED_LANGUAGES else "eng"
    return any(kw in normalized for kw in _AFFIRMATIVE_KEYWORDS[lang])


def main() -> int:
    language = detect_language()
    assistant = BaymaxAssistant(language=language)
    prefix = t(language, "assistant_prefix")
    print(assistant.greet())

    while True:
        try:
            message = input(t(language, "prompt")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not message:
            continue

        if message.lower() in {"exit", "quit", "q"}:
            # Pergunta se a pessoa está bem antes de encerrar.
            print(f"{prefix}{t(language, 'farewell_check')}")
            try:
                wellbeing = input(t(language, "prompt")).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return 0

            if _is_affirmative(wellbeing, language):
                print(f"{prefix}{t(language, 'farewell_thanks')}")
                return 0

            # Pessoa não confirmou que está bem — continua o atendimento.
            print(f"{prefix}{t(language, 'farewell_stay')}")
            continue

        response = assistant.respond(message)
        print(f"{prefix}{response.text}")


if __name__ == "__main__":
    raise SystemExit(main())

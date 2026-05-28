from __future__ import annotations

from .assistant import BaymaxAssistant
from .i18n import detect_language, t


def main() -> int:
    language = detect_language()
    assistant = BaymaxAssistant(language=language)
    print(assistant.greet())

    while True:
        try:
            message = input(t(language, "prompt")).strip()
        except EOFError:
            print()
            return 0

        if not message:
            continue

        if message.lower() in {"exit", "quit", "q"}:
            print(t(language, "exit"))
            return 0

        response = assistant.respond(message)
        print(f"{t(language, 'assistant_prefix')}{response.text}")


if __name__ == "__main__":
    raise SystemExit(main())

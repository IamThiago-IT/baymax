from __future__ import annotations

from .assistant import BaymaxAssistant


def main() -> int:
    assistant = BaymaxAssistant()
    print(assistant.greet())

    while True:
        try:
            message = input("You: ").strip()
        except EOFError:
            print()
            return 0

        if not message:
            continue

        if message.lower() in {"exit", "quit", "q"}:
            print("Baymax: Take care. If symptoms worsen, get medical help promptly.")
            return 0

        response = assistant.respond(message)
        print(f"Baymax: {response.text}")


if __name__ == "__main__":
    raise SystemExit(main())

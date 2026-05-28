# Baymax

Baymax is a health-focused virtual assistant CLI.

It automatically chooses the interface language from the operating system locale:

- Portuguese locales use `ptbr`
- English locales use `eng`
- unknown locales fall back to English

It is designed to:

- provide calm, simple guidance for general well-being
- ask follow-up questions about symptoms
- highlight urgent warning signs
- avoid diagnosis and prescription advice

## Run locally

```bash
python -m baymax
```

## Example

```text
You: I have a fever and a sore throat
Baymax: I can help with general guidance. How high is the fever, and are you having trouble breathing or swallowing?
```

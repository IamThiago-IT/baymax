import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from baymax.assistant import BaymaxAssistant, _extract_symptom_prompt
from baymax.cli import _is_affirmative


class ExtractSymptomPromptTests(unittest.TestCase):
    # --- English ---
    def test_fever_english(self):
        self.assertEqual(_extract_symptom_prompt("I have a fever", "eng"), "fever")

    def test_temperature_english(self):
        self.assertEqual(_extract_symptom_prompt("My temperature is high", "eng"), "fever")

    def test_cough_english(self):
        self.assertEqual(_extract_symptom_prompt("I have a sore throat", "eng"), "cough")

    def test_throat_english(self):
        self.assertEqual(_extract_symptom_prompt("My throat hurts", "eng"), "cough")

    def test_headache_english(self):
        self.assertEqual(_extract_symptom_prompt("I have a headache", "eng"), "headache")

    def test_migraine_english(self):
        self.assertEqual(_extract_symptom_prompt("terrible migraine today", "eng"), "headache")

    def test_nausea_english(self):
        self.assertEqual(_extract_symptom_prompt("I feel nausea", "eng"), "stomach")

    def test_diarrhea_english(self):
        self.assertEqual(_extract_symptom_prompt("I have diarrhea", "eng"), "stomach")

    def test_default_when_unknown_english(self):
        self.assertEqual(_extract_symptom_prompt("I feel bad", "eng"), "default_symptom")

    # --- Portuguese ---
    def test_fever_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("Estou com febre", "ptbr"), "fever")

    def test_temperatura_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("minha temperatura está alta", "ptbr"), "fever")

    def test_tosse_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("Estou com tosse", "ptbr"), "cough")

    def test_garganta_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("Minha garganta dói", "ptbr"), "cough")

    def test_dor_de_cabeca_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("Estou com dor de cabeça", "ptbr"), "headache")

    def test_enxaqueca_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("Tenho enxaqueca", "ptbr"), "headache")

    def test_enjoo_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("Estou com enjoo", "ptbr"), "stomach")

    def test_diarreia_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("Tenho diarreia", "ptbr"), "stomach")

    def test_default_when_unknown_portuguese(self):
        self.assertEqual(_extract_symptom_prompt("me sinto mal", "ptbr"), "default_symptom")

    # --- Unknown language falls back to English keywords ---
    def test_falls_back_to_english_for_unknown_language(self):
        self.assertEqual(_extract_symptom_prompt("I have a headache", "fr"), "headache")


class BaymaxAssistantGreetTests(unittest.TestCase):
    def test_greet_english_contains_baymax(self):
        assistant = BaymaxAssistant(language="eng")
        self.assertIn("Baymax", assistant.greet())

    def test_greet_portuguese_contains_baymax(self):
        assistant = BaymaxAssistant(language="ptbr")
        self.assertIn("Baymax", assistant.greet())

    def test_greet_unknown_language_falls_back_to_english(self):
        assistant = BaymaxAssistant(language="fr")
        greeting = assistant.greet()
        self.assertIn("Baymax", greeting)
        self.assertIn("health", greeting.lower())


class BaymaxAssistantRespondTests(unittest.TestCase):
    def test_respond_records_user_and_assistant_in_history(self):
        assistant = BaymaxAssistant(language="eng")
        assistant.respond("I have a headache")
        self.assertEqual(len(assistant.history), 2)
        self.assertEqual(assistant.history[0], ("user", "I have a headache"))
        self.assertEqual(assistant.history[1][0], "assistant")

    def test_respond_emergency_returns_emergency_level(self):
        assistant = BaymaxAssistant(language="eng")
        response = assistant.respond("I have chest pain and trouble breathing")
        self.assertEqual(response.safety.level, "emergency")

    def test_respond_restricted_returns_restricted_level(self):
        assistant = BaymaxAssistant(language="eng")
        response = assistant.respond("Can you diagnose me?")
        self.assertEqual(response.safety.level, "restricted")
        self.assertIn("diagnose", response.text.lower())

    def test_respond_safe_returns_safe_level(self):
        assistant = BaymaxAssistant(language="eng")
        response = assistant.respond("I have a fever")
        self.assertEqual(response.safety.level, "safe")

    def test_respond_text_is_non_empty(self):
        assistant = BaymaxAssistant(language="eng")
        response = assistant.respond("I have a headache")
        self.assertIsInstance(response.text, str)
        self.assertGreater(len(response.text), 0)

    def test_respond_portuguese_safe(self):
        assistant = BaymaxAssistant(language="ptbr")
        response = assistant.respond("Estou com febre")
        self.assertEqual(response.safety.level, "safe")
        self.assertGreater(len(response.text), 0)

    def test_repeated_symptom_uses_follow_up_template(self):
        """Second mention of the same symptom should produce a different reply."""
        assistant = BaymaxAssistant(language="eng")
        first = assistant.respond("I have a fever")
        second = assistant.respond("The fever is still there")
        self.assertNotEqual(first.text, second.text)

    def test_different_symptoms_do_not_trigger_follow_up(self):
        """Two different symptoms should both use the general_reply template."""
        assistant = BaymaxAssistant(language="eng")
        r1 = assistant.respond("I have a fever")
        r2 = assistant.respond("I also have a headache")
        # Both start with "I hear you." (general_reply) not "Thanks for the update."
        self.assertIn("I hear you", r1.text)
        self.assertIn("I hear you", r2.text)


class IsAffirmativeTests(unittest.TestCase):
    # --- English affirmatives ---
    def test_yes_english(self):
        self.assertTrue(_is_affirmative("yes", "eng"))

    def test_yeah_english(self):
        self.assertTrue(_is_affirmative("yeah, I'm fine", "eng"))

    def test_fine_english(self):
        self.assertTrue(_is_affirmative("I'm fine", "eng"))

    def test_okay_english(self):
        self.assertTrue(_is_affirmative("okay", "eng"))

    def test_feeling_better_english(self):
        self.assertTrue(_is_affirmative("feeling better now", "eng"))

    # --- English negatives ---
    def test_no_english(self):
        self.assertFalse(_is_affirmative("no, still sick", "eng"))

    def test_not_well_english(self):
        self.assertFalse(_is_affirmative("not really", "eng"))

    def test_empty_english(self):
        self.assertFalse(_is_affirmative("", "eng"))

    # --- Portuguese affirmatives ---
    def test_sim_portuguese(self):
        self.assertTrue(_is_affirmative("sim", "ptbr"))

    def test_tudo_bem_portuguese(self):
        self.assertTrue(_is_affirmative("tudo bem", "ptbr"))

    def test_estou_bem_portuguese(self):
        self.assertTrue(_is_affirmative("estou bem sim", "ptbr"))

    def test_melhor_portuguese(self):
        self.assertTrue(_is_affirmative("estou melhor", "ptbr"))

    # --- Portuguese negatives ---
    def test_nao_portuguese(self):
        self.assertFalse(_is_affirmative("não, ainda com febre", "ptbr"))

    def test_empty_portuguese(self):
        self.assertFalse(_is_affirmative("", "ptbr"))

    # --- Case insensitivity ---
    def test_case_insensitive_english(self):
        self.assertTrue(_is_affirmative("YES", "eng"))

    def test_case_insensitive_portuguese(self):
        self.assertTrue(_is_affirmative("TUDO BEM", "ptbr"))

    # --- Unknown language falls back to English ---
    def test_unknown_language_fallback(self):
        self.assertTrue(_is_affirmative("yes", "fr"))


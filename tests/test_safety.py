import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from baymax.safety import assess_message


class EmergencyDetectionTests(unittest.TestCase):
    def test_chest_pain_and_breathing_english(self):
        result = assess_message("I have chest pain and trouble breathing")
        self.assertEqual(result.level, "emergency")

    def test_chest_pain_alone_english(self):
        result = assess_message("I have chest pain")
        self.assertEqual(result.level, "emergency")

    def test_suicidal_english(self):
        result = assess_message("I feel suicidal")
        self.assertEqual(result.level, "emergency")

    def test_fainted_english(self):
        result = assess_message("I just fainted")
        self.assertEqual(result.level, "emergency")

    def test_dor_no_peito_portuguese(self):
        result = assess_message("Estou com dor no peito", language="ptbr")
        self.assertEqual(result.level, "emergency")

    def test_suicida_portuguese(self):
        result = assess_message("Me sinto suicida", language="ptbr")
        self.assertEqual(result.level, "emergency")

    def test_emergency_message_is_non_empty(self):
        result = assess_message("I have chest pain")
        self.assertTrue(len(result.message) > 0)

    def test_emergency_message_english_contains_urgent(self):
        result = assess_message("I have chest pain", language="eng")
        self.assertIn("urgent", result.message.lower())

    def test_emergency_message_ptbr_contains_urgente(self):
        result = assess_message("Estou com dor no peito", language="ptbr")
        self.assertIn("urgente", result.message.lower())


class DiagnosisRestrictionTests(unittest.TestCase):
    def test_diagnose_me_english(self):
        result = assess_message("Can you diagnose me?")
        self.assertEqual(result.level, "restricted")

    def test_prescribe_english(self):
        result = assess_message("Please prescribe something for me")
        self.assertEqual(result.level, "restricted")

    def test_which_medicine_english(self):
        result = assess_message("which medicine should i take?")
        self.assertEqual(result.level, "restricted")

    def test_diagnostique_portuguese(self):
        result = assess_message("me diagnostique por favor", language="ptbr")
        self.assertEqual(result.level, "restricted")

    def test_qual_remedio_portuguese(self):
        result = assess_message("qual remédio devo tomar", language="ptbr")
        self.assertEqual(result.level, "restricted")

    def test_restricted_message_english_contains_diagnose(self):
        result = assess_message("Can you diagnose me?", language="eng")
        self.assertIn("diagnose", result.message.lower())

    def test_restricted_message_ptbr_contains_diagnosticar(self):
        result = assess_message("me diagnostique", language="ptbr")
        self.assertIn("diagnosticar", result.message.lower())


class SafeMessageTests(unittest.TestCase):
    def test_regular_symptom_is_safe(self):
        result = assess_message("I have a headache")
        self.assertEqual(result.level, "safe")

    def test_safe_message_is_empty(self):
        result = assess_message("I have a fever")
        self.assertEqual(result.message, "")

    def test_empty_message_is_safe(self):
        result = assess_message("")
        self.assertEqual(result.level, "safe")

    def test_case_insensitive_detection(self):
        result = assess_message("CHEST PAIN")
        self.assertEqual(result.level, "emergency")

import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from baymax.safety import assess_message


class SafetyTests(unittest.TestCase):
    def test_emergency_detection(self):
        result = assess_message("I have chest pain and trouble breathing")

        self.assertEqual(result.level, "emergency")
        self.assertTrue(
            "urgent" in result.message.lower() or "emergency" in result.message.lower()
        )


    def test_diagnosis_request_restricted(self):
        result = assess_message("Can you diagnose me?")

        self.assertEqual(result.level, "restricted")
        self.assertIn("diagnose", result.message.lower())

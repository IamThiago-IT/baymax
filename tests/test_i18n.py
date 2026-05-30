import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from baymax.i18n import detect_language, t


class DetectLanguageTests(unittest.TestCase):
    def tearDown(self):
        for var in ("BAYMAX_LANG", "LANG", "LC_ALL", "LC_MESSAGES"):
            os.environ.pop(var, None)

    def test_detect_ptbr_from_baymax_lang(self):
        os.environ["BAYMAX_LANG"] = "pt_BR"
        self.assertEqual(detect_language(), "ptbr")

    def test_detect_english_from_baymax_lang(self):
        os.environ["BAYMAX_LANG"] = "en_US"
        self.assertEqual(detect_language(), "eng")

    def test_baymax_lang_takes_priority_over_lang(self):
        os.environ["BAYMAX_LANG"] = "pt_BR"
        os.environ["LANG"] = "en_US.UTF-8"
        self.assertEqual(detect_language(), "ptbr")

    def test_detect_ptbr_from_lang_env(self):
        os.environ["LANG"] = "pt_BR.UTF-8"
        self.assertEqual(detect_language(), "ptbr")

    def test_detect_english_from_lang_env(self):
        os.environ["LANG"] = "en_US.UTF-8"
        self.assertEqual(detect_language(), "eng")

    def test_detect_ptbr_from_lc_all(self):
        os.environ["LC_ALL"] = "pt_BR.UTF-8"
        self.assertEqual(detect_language(), "ptbr")

    def test_detect_ptbr_from_lc_messages(self):
        os.environ["LC_MESSAGES"] = "pt_BR.UTF-8"
        self.assertEqual(detect_language(), "ptbr")

    def test_unknown_locale_falls_back_to_english(self):
        # Patch locale.getlocale to ensure the OS locale doesn't interfere.
        with patch("baymax.i18n.locale.getlocale", return_value=("zh_CN", "UTF-8")):
            os.environ["BAYMAX_LANG"] = "zh_CN"
            self.assertEqual(detect_language(), "eng")

    def test_empty_locale_falls_back_to_english(self):
        # Patch locale.getlocale to ensure the OS locale doesn't interfere.
        with patch("baymax.i18n.locale.getlocale", return_value=(None, None)):
            os.environ["BAYMAX_LANG"] = ""
            self.assertEqual(detect_language(), "eng")


class TranslateTests(unittest.TestCase):
    def test_translate_prompt_ptbr(self):
        self.assertEqual(t("ptbr", "prompt"), "Você: ")

    def test_translate_prompt_eng(self):
        self.assertEqual(t("eng", "prompt"), "You: ")

    def test_translate_with_format_args(self):
        result = t("eng", "general_reply", prompt="test prompt", urgent="test urgent")
        self.assertIn("test prompt", result)
        self.assertIn("test urgent", result)

    def test_unknown_language_falls_back_to_english(self):
        result = t("fr", "prompt")
        self.assertEqual(result, "You: ")

    def test_missing_key_returns_placeholder(self):
        result = t("eng", "nonexistent_key_xyz")
        self.assertIn("missing", result)
        self.assertIn("nonexistent_key_xyz", result)

    def test_all_eng_keys_present(self):
        from baymax.i18n import STRINGS
        required_keys = {
            "greeting", "prompt", "assistant_prefix", "exit", "urgent_fallback",
            "fever", "cough", "headache", "stomach", "default_symptom",
            "general_reply", "follow_up", "restricted_message",
        }
        self.assertTrue(required_keys.issubset(STRINGS["eng"].keys()))

    def test_all_ptbr_keys_match_eng(self):
        from baymax.i18n import STRINGS
        self.assertEqual(set(STRINGS["eng"].keys()), set(STRINGS["ptbr"].keys()))

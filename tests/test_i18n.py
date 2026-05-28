import os
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from baymax.i18n import detect_language, t


class I18nTests(unittest.TestCase):
    def tearDown(self):
        os.environ.pop("BAYMAX_LANG", None)
        os.environ.pop("LANG", None)

    def test_detect_ptbr_from_env(self):
        os.environ["BAYMAX_LANG"] = "pt_BR"

        self.assertEqual(detect_language(), "ptbr")

    def test_detect_english_from_env(self):
        os.environ["BAYMAX_LANG"] = "en_US"

        self.assertEqual(detect_language(), "eng")

    def test_translate_prompt(self):
        self.assertEqual(t("ptbr", "prompt"), "Você: ")
        self.assertEqual(t("eng", "prompt"), "You: ")

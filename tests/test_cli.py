import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from baymax.cli import _is_affirmative, main


class IsAffirmativeCliTests(unittest.TestCase):
    def test_affirmative_english_yes(self):
        self.assertTrue(_is_affirmative("yes", "eng"))

    def test_non_affirmative_english(self):
        self.assertFalse(_is_affirmative("no", "eng"))

    def test_affirmative_ptbr_sim(self):
        self.assertTrue(_is_affirmative("sim", "ptbr"))

    def test_unknown_language_fallback(self):
        self.assertTrue(_is_affirmative("yes", "xx"))


class MainCliTests(unittest.TestCase):
    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=EOFError)
    def test_eof_at_first_prompt_returns_zero(
        self, _mock_input, _mock_print, _mock_lang
    ):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt_at_first_prompt_returns_zero(
        self, _mock_input, _mock_print, _mock_lang
    ):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["", EOFError])
    def test_empty_message_continues(self, _mock_input, _mock_print, _mock_lang):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["exit", "yes"])
    def test_exit_affirmative_returns_zero(self, _mock_input, mock_print, _mock_lang):
        self.assertEqual(main(), 0)
        # greeting + farewell_check + farewell_thanks at least
        self.assertGreaterEqual(mock_print.call_count, 3)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["quit", "okay"])
    def test_quit_alias_affirmative(self, _mock_input, _mock_print, _mock_lang):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["q", "yep"])
    def test_q_alias_affirmative(self, _mock_input, _mock_print, _mock_lang):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["EXIT", "YES"])
    def test_exit_case_insensitive(self, _mock_input, _mock_print, _mock_lang):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["exit", EOFError])
    def test_exit_eof_on_wellbeing_returns_zero(
        self, _mock_input, _mock_print, _mock_lang
    ):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["exit", KeyboardInterrupt])
    def test_exit_keyboard_interrupt_on_wellbeing_returns_zero(
        self, _mock_input, _mock_print, _mock_lang
    ):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["exit", "no", "I have a fever", EOFError])
    def test_exit_non_affirmative_continues_then_handles_message(
        self, _mock_input, mock_print, _mock_lang
    ):
        self.assertEqual(main(), 0)
        # Should print farewell_stay and then a response containing urgent fallback
        printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("here whenever", printed.lower())

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["I have a fever", EOFError])
    def test_normal_message_prints_response(self, _mock_input, mock_print, _mock_lang):
        self.assertEqual(main(), 0)
        printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Baymax", printed)

    @patch("baymax.cli.detect_language", return_value="ptbr")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Estou com febre", EOFError])
    def test_ptbr_normal_message(self, _mock_input, mock_print, _mock_lang):
        self.assertEqual(main(), 0)
        printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
        self.assertIn("Baymax", printed)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["exit", "  YES  "])
    def test_wellbeing_stripped_and_lowered(self, _mock_input, _mock_print, _mock_lang):
        self.assertEqual(main(), 0)

    @patch("baymax.cli.detect_language", return_value="eng")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["   ", "exit", "yes"])
    def test_whitespace_only_message_continues(
        self, _mock_input, _mock_print, _mock_lang
    ):
        self.assertEqual(main(), 0)

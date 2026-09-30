"""Negative checks for the metadata validator, not model safety evaluations."""
import importlib.util
import unittest
from unittest.mock import patch
from datetime import date
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
SPEC = importlib.util.spec_from_file_location("validate", MODULE_PATH)
validate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        validate.ERRORS.clear()

    def test_duplicate_ids_rejected(self):
        validate.index([{"id": "same"}, {"id": "same"}], "fixture")
        self.assertTrue(validate.ERRORS)

    def test_unknown_reference_rejected(self):
        validate.references(["unknown"], {"known"}, "fixture")
        self.assertTrue(validate.ERRORS)

    def test_invalid_date_rejected(self):
        validate.iso_date("2026-02-30", "fixture")
        self.assertTrue(validate.ERRORS)

    def test_future_date_rejected(self):
        validate.iso_date("2027-01-01", "fixture", date(2026, 9, 30))
        self.assertTrue(validate.ERRORS)

    def test_path_escape_rejected(self):
        validate.local_file("../README.md", "fixture")
        self.assertTrue(any("escapes" in value for value in validate.ERRORS))

    def test_valid_values_accepted(self):
        validate.index([{"id": "valid"}], "fixture")
        validate.references(["known"], {"known"}, "fixture")
        validate.iso_date("2026-09-30", "fixture", date(2026, 9, 30))
        validate.local_file("README.md", "fixture")
        self.assertEqual(validate.ERRORS, [])

    def test_non_object_json_rejected(self):
        with patch("pathlib.Path.read_text", return_value="[]"):
            self.assertEqual(validate.load_json("fixture.json"), {})
        self.assertTrue(validate.ERRORS)


if __name__ == "__main__":
    unittest.main()

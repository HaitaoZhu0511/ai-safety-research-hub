from pathlib import Path
import json
import unittest
from runtime.golden import run_suite


class ReportTests(unittest.TestCase):
    def test_stored_report_matches_fresh_run(self):
        root = Path(__file__).resolve().parents[1]
        fresh = run_suite(root / "evals/control-golden.json")
        stored = json.loads((root / "reports/offline-control-summary.json").read_text(encoding="utf-8"))
        for key in ("suite_version", "execution_type", "data_type", "model_evaluated",
                    "passed", "total", "slices"):
            self.assertEqual(stored[key], fresh[key], key)
        fields = ("id", "slice", "passed", "expected", "observed")
        normalized = [{key: row[key] for key in fields} for row in fresh["results"]]
        self.assertEqual(stored["results"], normalized)


if __name__ == "__main__":
    unittest.main()

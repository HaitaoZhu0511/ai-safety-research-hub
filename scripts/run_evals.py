"""Print JSON results to stdout; exit nonzero on any failed synthetic assertion."""
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime.golden import run_suite


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    report = run_suite(root / "evals" / "control-golden.json")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["passed"] == report["total"] else 1)

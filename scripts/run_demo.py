"""Print a synthetic read/approval/audit demo without creating files."""
from dataclasses import asdict, replace
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime.safety import Request, SafetyEngine, replay


def main():
    engine = SafetyEngine()
    request = Request("demo-export", "analyst_a", "export_records",
                      {"tenant": "tenant_a", "limit": 2, "destination": "internal://audit"})
    results = [engine.execute(request)]
    approval = engine.approve(request, "reviewer_a")
    changed = replace(request, parameters={**request.parameters, "limit": 3})
    results.append(engine.execute(changed, approval))
    results.append(engine.execute(request, approval))
    results.append(engine.execute(request, approval))
    print(json.dumps({"notice": "synthetic, no database/model/network", "outcomes": [
        asdict(result) for result in results], "execution_count": engine.execution_count,
        "audit": engine.events, "replay": replay(engine.events)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

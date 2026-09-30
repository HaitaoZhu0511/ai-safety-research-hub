"""Execute a bounded, declarative synthetic control suite; no model calls."""
from dataclasses import asdict, replace
from pathlib import Path
import json

from runtime.safety import Request, SafetyEngine, replay


def run_case(case: dict) -> dict:
    timestamp = [1000.0]
    engine = SafetyEngine(clock=lambda: timestamp[0])
    proposals = {name: Request(**payload) for name, payload in case["requests"].items()}
    tokens = {}
    outcome = None
    for action in case["actions"]:
        operation = action["operation"]
        if operation == "approve":
            tokens[action["token"]] = engine.approve(proposals[action["request"]], action["reviewer"])
        elif operation == "execute":
            outcome = engine.execute(proposals[action["request"]], tokens.get(action.get("token")))
        elif operation == "advance_clock":
            timestamp[0] += action["seconds"]
        elif operation == "kill_switch":
            engine.disabled = True
        elif operation == "policy_version":
            engine.policy = replace(engine.policy, version=action["version"])
        else:
            raise ValueError("Unknown golden action: " + operation)
    if outcome is None:
        raise ValueError("Golden case has no execution")
    audit = replay(engine.events)
    observed = {"decision": outcome.decision, "reason": outcome.reason,
                "executions": engine.execution_count,
                "risk_ids": engine.events[-1]["risk_ids"]}
    passed = observed == case["expected"]
    return {"id": case["id"], "slice": case["slice"], "risk_ids": case["risk_ids"],
            "passed": passed, "expected": case["expected"], "observed": observed,
            "audit": audit, "last_outcome": asdict(outcome)}


def run_suite(path: Path) -> dict:
    suite = json.loads(path.read_text(encoding="utf-8"))
    results = [run_case(case) for case in suite["cases"]]
    groups = {}
    for group in sorted({row["slice"] for row in results}):
        rows = [row for row in results if row["slice"] == group]
        groups[group] = {"passed": sum(row["passed"] for row in rows), "total": len(rows)}
    return {"suite_version": suite["suite_version"], "execution_type": "offline_deterministic",
            "data_type": "synthetic", "model_evaluated": False,
            "passed": sum(row["passed"] for row in results), "total": len(results),
            "slices": groups, "results": results,
            "limitation": "Assertions verify this demo only, not LLM attack success or production risk recall."}

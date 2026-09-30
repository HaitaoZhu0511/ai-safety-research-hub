"""Validate research metadata and local links; this does NOT run model evaluations."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def load_json(relative: str) -> dict:
    try:
        value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            ERRORS.append(f"{relative}: top-level JSON must be an object")
            return {}
        return value
    except (OSError, ValueError) as exc:
        ERRORS.append(f"{relative}: {exc}")
        return {}


def records(relative: str, key: str) -> list[dict]:
    data = load_json(relative).get(key, [])
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        ERRORS.append(f"{relative}: {key} must be an array of objects")
        return []
    return data


def index(rows: list[dict], label: str) -> set[str]:
    identifiers = [row.get("id") for row in rows]
    check(all(isinstance(value, str) and value for value in identifiers),
          f"{label}: missing or invalid IDs")
    valid = [value for value in identifiers if isinstance(value, str)]
    check(len(valid) == len(set(valid)), f"{label}: duplicate IDs")
    return set(valid)


def references(values: object, available: set[str], label: str) -> None:
    if not isinstance(values, list) or not values:
        ERRORS.append(f"{label}: expected nonempty reference array")
        return
    for value in values:
        check(isinstance(value, str) and value in available,
              f"{label}: unknown reference {value!r}")


def local_file(relative: object, label: str) -> None:
    if not isinstance(relative, str) or not relative:
        ERRORS.append(f"{label}: missing local path")
        return
    target = (ROOT / relative).resolve()
    check(target.is_relative_to(ROOT), f"{label}: path escapes repository")
    check(target.is_file(), f"{label}: missing file {relative}")


def iso_date(value: object, label: str, cutoff: date | None = None) -> None:
    try:
        parsed = date.fromisoformat(value) if isinstance(value, str) else None
        check(parsed is not None, f"{label}: missing date")
        if parsed and cutoff:
            check(parsed <= cutoff, f"{label}: date exceeds reviewed date")
    except ValueError:
        ERRORS.append(f"{label}: invalid ISO date {value!r}")


def golden_expectation(value: object, risk_ids: set[str], label: str) -> None:
    if not isinstance(value, dict):
        ERRORS.append(f"{label}: expected must be an object")
        return
    check(set(value) == {"decision", "reason", "executions", "risk_ids"},
          f"{label}: expected must include exactly decision/reason/executions/risk_ids")
    check(value.get("decision") in {"allow", "block", "review", "restrict"},
          f"{label}: invalid expected decision")
    check(isinstance(value.get("reason"), str) and bool(value["reason"]), f"{label}: expected reason required")
    check(type(value.get("executions")) is int and value["executions"] >= 0,
          f"{label}: invalid expected execution count")
    labels = value.get("risk_ids")
    if not isinstance(labels, list):
        ERRORS.append(f"{label}: expected risk_ids must be an array")
        return
    check(all(isinstance(item, str) and item in risk_ids for item in labels),
          f"{label}: unknown expected risk label")
    valid = [item for item in labels if isinstance(item, str)]
    check(len(valid) == len(set(valid)), f"{label}: duplicate expected risk labels")
    if value.get("decision") in {"block", "review", "restrict"}:
        check(bool(labels), f"{label}: denied/reviewed control requires a risk label")


def main() -> int:
    ERRORS.clear()
    sources_doc = load_json("catalog/sources.json")
    reviewed = sources_doc.get("reviewed_at")
    iso_date(reviewed, "sources reviewed_at")
    try:
        cutoff = date.fromisoformat(reviewed)
    except (TypeError, ValueError):
        cutoff = None

    sources = records("catalog/sources.json", "sources")
    companies = records("catalog/companies.json", "companies")
    cases = records("catalog/cases.json", "cases")
    risks = records("catalog/risks.json", "risks")
    scenarios = records("catalog/scenarios.json", "scenarios")
    news = records("catalog/news.json", "news")
    designs = records("evals/design-cases.json", "cases")
    source_ids = index(sources, "sources")
    company_ids = index(companies, "companies")
    index(cases, "cases")
    risk_ids = index(risks, "risks")
    scenario_ids = index(scenarios, "scenarios")
    index(news, "news")
    index(designs, "eval designs")
    for name, rows in (("sources", sources), ("companies", companies),
                       ("cases", cases), ("risks", risks),
                       ("scenarios", scenarios), ("news", news),
                       ("eval designs", designs)):
        check(bool(rows), f"{name}: empty catalog")

    urls: set[str] = set()
    for row in sources:
        label = f"source {row.get('id')}"
        parsed = urlsplit(row.get("url", ""))
        check(parsed.scheme == "https" and bool(parsed.netloc), f"{label}: HTTPS URL required")
        check(row.get("url") not in urls, f"{label}: duplicate URL")
        urls.add(row.get("url", ""))
        iso_date(row.get("verified_at"), label, cutoff)
        check(row.get("access_status") in {"content_retrieved", "javascript_required", "unavailable", "search_excerpt"},
              f"{label}: invalid access status")
        for key in ("title", "publisher", "type"):
            check(bool(row.get(key)), f"{label}: missing {key}")
        if row.get("access_status") != "content_retrieved":
            check(bool(row.get("note")), f"{label}: unreadable source needs limitation note")

    for row in companies:
        references(row.get("source_ids"), source_ids, f"company {row.get('id')}")
        local_file(row.get("document"), f"company {row.get('id')}")
    case_types = {"disclosed_vulnerability", "controlled_research", "controlled_simulation",
                  "real_world_experiment", "company_report", "product_application"}
    for row in cases:
        label = f"case {row.get('id')}"
        references(row.get("source_ids"), source_ids, label)
        references(row.get("company_ids"), company_ids, label)
        local_file(row.get("analysis"), label)
        check(row.get("kind") in case_types, f"{label}: invalid evidence type")
        for key in ("summary", "boundary", "lesson", "limit", "regression"):
            check(bool(row.get(key)), f"{label}: missing {key}")
        value = row.get("event_date")
        if value is not None:
            check(isinstance(value, str) and bool(re.fullmatch(r"\d{4}(?:-\d{2})?(?:-\d{2})?", value)),
                  f"{label}: invalid partial date")
            if isinstance(value, str):
                iso_date(value + "-01-01" if len(value) == 4 else
                         value + "-01" if len(value) == 7 else value, label, cutoff)
    for row in scenarios:
        references(row.get("risk_ids"), risk_ids, f"scenario {row.get('id')}")
    for row in news:
        check(row.get("source_id") in source_ids, f"news {row.get('id')}: unknown source")
        iso_date(row.get("date"), f"news {row.get('id')}", cutoff)
        check(row.get("event_type") in {"research_publication", "experiment_publication",
                                      "paper_submission", "report_release", "documentation_update", "framework_publication"},
              f"news {row.get('id')}: invalid event type")
    for row in designs:
        check(row.get("risk_id") in risk_ids, f"eval {row.get('id')}: unknown risk")
        check(row.get("scenario_id") in scenario_ids, f"eval {row.get('id')}: unknown scenario")
        check(row.get("execution_status") == "design_only", f"eval {row.get('id')}: not design-only")
        check(row.get("data_type") == "synthetic", f"eval {row.get('id')}: not synthetic")
        for key in ("input_summary", "expected", "evidence"):
            check(bool(row.get(key)), f"eval {row.get('id')}: missing {key}")

    for relative in ("README.md", "LICENSE", "CONTRIBUTING.md", ".github/workflows/validate.yml",
                     "docs/architecture.md", "docs/evaluation.md", "docs/cost-and-value.md",
                     "docs/roadmap.md", "playbooks/incident-response.md",
                     "playbooks/redteam-and-release.md", "contracts/risk-event.schema.json"):
        local_file(relative, "required file")

    golden = records("evals/control-golden.json", "cases")
    golden_ids = index(golden, "control golden")
    for row in golden:
        references(row.get("risk_ids"), risk_ids, f"golden {row.get('id')}")
        check(row.get("scenario_id") in scenario_ids, f"golden {row.get('id')}: unknown scenario")
        check(row.get("slice") in {"normal", "risky"}, f"golden {row.get('id')}: invalid slice")
        check(bool(row.get("requests")) and bool(row.get("actions")), f"golden {row.get('id')}: empty inputs")
        golden_expectation(row.get("expected"), risk_ids, f"golden {row.get('id')}")
    stored_report = load_json("reports/offline-control-summary.json")
    report_ids = index(stored_report.get("results", []), "stored control report")
    check(golden_ids == report_ids, "Control report IDs differ from golden suite")
    check(stored_report.get("model_evaluated") is False, "Control report must not claim model evaluation")
    check(stored_report.get("total") == len(golden), "Control report count mismatch")
    for row in records("catalog/source-review.json", "reviews"):
        check(row.get("source_id") in source_ids, "Source review refers to unknown source")
    for relative in ("runtime/safety.py", "runtime/golden.py", "scripts/run_demo.py",
                     "scripts/run_evals.py", "docs/offline-demo.md", "requirements-dev.txt"):
        local_file(relative, "v0.2 required file")
    for relative in ("docs/control-hardening.md", "docs/production-integration.md",
                     "contracts/archive/risk-event-0.2.schema.json"):
        local_file(relative, "v0.3 required file")

    # Parse every JSON file. Real event-schema validation is covered by test_contracts.py.
    for path in ROOT.rglob("*.json"):
        if ".git" not in path.parts and ".venv" not in path.parts:
            load_json(path.relative_to(ROOT).as_posix())

    # The repository uses inline Markdown links. Remote links and anchors are excluded.
    link_pattern = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
    markdown_count = 0
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or ".venv" in path.parts:
            continue
        markdown_count += 1
        content = path.read_text(encoding="utf-8")
        check("\ufffd" not in content, f"{path.relative_to(ROOT)}: replacement character")
        for match in link_pattern.finditer(content):
            target_text = match.group(1).strip().strip("<>")
            parsed = urlsplit(target_text)
            if parsed.scheme or target_text.startswith("#"):
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            check(target.is_relative_to(ROOT), f"{path.relative_to(ROOT)}: link escapes repository")
            check(target.exists(), f"{path.relative_to(ROOT)}: broken local link {target_text}")

    if ERRORS:
        for message in ERRORS:
            print(f"ERROR: {message}", file=sys.stderr)
        return 1
    print(f"PASS: {len(sources)} sources, {len(companies)} companies, {len(cases)} cases, "
          f"{len(scenarios)} scenarios, {len(designs)} test designs, {len(news)} news entries, "
          f"{markdown_count} Markdown files")
    print("Metadata and local-path checks only. No model evaluations or remote-link health checks executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

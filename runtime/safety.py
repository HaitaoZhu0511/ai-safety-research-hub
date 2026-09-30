"""Deterministic control demo. NOT authentication middleware or a production sandbox."""
from __future__ import annotations

import copy
import hashlib
import json
import time
import uuid
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Callable


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class Policy:
    version: str = "demo-0.2"
    allowed_tools: tuple[str, ...] = ("read_metric", "export_records")
    destinations: tuple[str, ...] = ("internal://audit",)
    max_rows: int = 100
    approval_ttl_seconds: int = 60

    def __post_init__(self):
        if not isinstance(self.version, str) or not self.version or type(self.max_rows) is not int or not 1 <= self.max_rows <= 10_000:
            raise ValueError("Invalid policy version or row limit")
        if type(self.approval_ttl_seconds) is not int or self.approval_ttl_seconds < 1:
            raise ValueError("Invalid approval TTL")
        if not isinstance(self.allowed_tools, tuple) or not isinstance(self.destinations, tuple):
            raise ValueError("Policy collections must be immutable tuples")
        if not set(self.allowed_tools) <= {"read_metric", "export_records"}:
            raise ValueError("Unregistered tool in policy")
        if not all(isinstance(value, str) and value for value in self.destinations):
            raise ValueError("Invalid destinations")


@dataclass(frozen=True)
class Identity:
    tenant: str
    role: str


@dataclass(frozen=True)
class Request:
    request_id: str
    principal: str
    tool: str
    parameters: dict


@dataclass(frozen=True)
class Outcome:
    decision: str
    reason: str
    receipt_ref: str | None = None
    result: object = None
    cached: bool = False


@dataclass(frozen=True)
class Approval:
    fingerprint: str
    reviewer: str
    expires_at: float


class SafetyEngine:
    """All IDs, metrics and exports are fictitious; state is single-process memory."""

    def __init__(self, policy: Policy | None = None, clock: Callable[[], float] = time.time):
        self.policy = policy or Policy()
        self.clock = clock
        self._identities = {
            "analyst_a": Identity("tenant_a", "analyst"),
            "analyst_b": Identity("tenant_b", "analyst"),
            "viewer_a": Identity("tenant_a", "viewer"),
            "reviewer_a": Identity("tenant_a", "reviewer"),
            "reviewer_b": Identity("tenant_b", "reviewer"),
        }
        self._metrics = {
            "tenant_a": {"dau": 1200, "retention_d7": 0.36},
            "tenant_b": {"dau": 800, "retention_d7": 0.28},
        }
        self._approvals: dict[str, Approval] = {}
        self._receipts: dict[tuple[str, str], tuple[str, Outcome]] = {}
        self._events: list[dict] = []
        self.execution_count = 0
        self.disabled = False

    @property
    def events(self) -> list[dict]:
        return copy.deepcopy(self._events)

    def _snapshot(self, request: Request) -> Request:
        # Deep-copy the proposal before validation, approval binding or execution.
        params = json.loads(json.dumps(request.parameters, allow_nan=False))
        return Request(request.request_id, request.principal, request.tool, params)

    def _guard(self, request: Request) -> str | None:
        if self.disabled:
            return "kill_switch"
        if not all(isinstance(value, str) and value for value in
                   (request.request_id, request.principal, request.tool)):
            return "invalid_request"
        identity = self._identities.get(request.principal)
        if identity is None:
            return "unknown_identity"
        if request.tool not in self.policy.allowed_tools:
            return "tool_not_allowed"
        if not isinstance(request.parameters, dict):
            return "invalid_parameters"
        required = {"tenant", "metric"} if request.tool == "read_metric" else {"tenant", "limit", "destination"}
        if set(request.parameters) != required:
            return "invalid_parameters"
        if request.parameters["tenant"] != identity.tenant:
            return "tenant_mismatch"
        if request.tool == "read_metric":
            if identity.role not in {"analyst", "viewer"}:
                return "role_denied"
            metric = request.parameters["metric"]
            if not isinstance(metric, str) or metric not in self._metrics[identity.tenant]:
                return "metric_not_allowed"
        else:
            if identity.role != "analyst":
                return "role_denied"
            limit = request.parameters["limit"]
            if type(limit) is not int or not 1 <= limit <= self.policy.max_rows:
                return "row_budget"
            if request.parameters["destination"] not in self.policy.destinations:
                return "destination_denied"
        return None

    def _fingerprint(self, request: Request) -> str:
        identity = self._identities.get(request.principal)
        return digest({"request": asdict(request), "policy": asdict(self.policy),
                       "identity": asdict(identity) if identity else None})

    def _emit(self, request: Request, outcome: Outcome, approval_ref: str | None = None) -> Outcome:
        try:
            request_digest = self._fingerprint(request)
        except (TypeError, ValueError):
            request_digest = digest({"request": "invalid_non_json_proposal"})
        risk_ids = [] if outcome.decision == "allow" else [
            "privacy" if outcome.reason == "tenant_mismatch" else "tool-authority"]
        event = {
            "schema_version": "0.2",
            "event_id": f"evt-{len(self._events) + 1:04d}",
            "timestamp": datetime.fromtimestamp(self.clock(), timezone.utc).isoformat(),
            "scenario": "data-agent",
            "identity_ref": request.principal if isinstance(request.principal, str) and request.principal else "invalid",
            "policy_version": self.policy.version,
            "intervention_point": "tool_proposal",
            "decision": outcome.decision,
            "risk_ids": risk_ids,
            "evidence_refs": ["sha256:" + request_digest],
            "approval_ref": approval_ref,
            "execution_receipt_ref": outcome.receipt_ref,
            "reason_code": outcome.reason,
            "request_digest": request_digest,
            "sequence": len(self._events) + 1,
            "previous_hash": self._events[-1]["event_hash"] if self._events else "0" * 64,
        }
        event["event_hash"] = digest(event)
        self._events.append(event)
        return copy.deepcopy(outcome)

    def approve(self, request: Request, reviewer: str) -> str:
        request = self._snapshot(request)
        failure = self._guard(request)
        if failure:
            raise ValueError("Cannot approve an invalid proposal: " + failure)
        identity = self._identities.get(reviewer)
        if identity is None or identity.role != "reviewer":
            raise PermissionError("Reviewer role required")
        if identity.tenant != request.parameters["tenant"] or reviewer == request.principal:
            raise PermissionError("Independent same-tenant reviewer required")
        if request.tool != "export_records":
            raise ValueError("This tool does not require approval")
        token = "apr-" + uuid.uuid4().hex
        self._approvals[token] = Approval(self._fingerprint(request), reviewer,
                                         self.clock() + self.policy.approval_ttl_seconds)
        self._emit(request, Outcome("allow", "approval_issued"), token)
        return token

    def execute(self, request: Request, approval_ref: str | None = None) -> Outcome:
        try:
            request = self._snapshot(request)
        except (TypeError, ValueError):
            return self._emit(request, Outcome("block", "invalid_request"))
        failure = self._guard(request)
        if failure:
            return self._emit(request, Outcome("block", failure))
        fingerprint = self._fingerprint(request)
        key = (request.principal, request.request_id)
        prior = self._receipts.get(key)
        if prior:
            if prior[0] != fingerprint:
                return self._emit(request, Outcome("block", "idempotency_conflict"))
            original = prior[1]
            return self._emit(request, Outcome("allow", "idempotent_replay",
                                              original.receipt_ref, original.result, True))
        if request.tool == "export_records":
            if approval_ref is None:
                return self._emit(request, Outcome("review", "approval_required"))
            approval = self._approvals.get(approval_ref) if isinstance(approval_ref, str) else None
            if approval is None:
                return self._emit(request, Outcome("block", "approval_unknown"))
            if approval.fingerprint != fingerprint:
                return self._emit(request, Outcome("block", "approval_mismatch"))
            if self.clock() >= approval.expires_at:
                return self._emit(request, Outcome("block", "approval_expired"))
        # No SQL, sockets, filesystem writes, production APIs or user-supplied code.
        tenant = request.parameters["tenant"]
        if request.tool == "read_metric":
            result = {"metric": request.parameters["metric"],
                      "value": self._metrics[tenant][request.parameters["metric"]],
                      "source_ref": f"synthetic://{tenant}/metrics/v1"}
        else:
            result = {"record_refs": [f"synthetic://{tenant}/record/{i + 1}"
                                      for i in range(request.parameters["limit"])],
                      "destination": request.parameters["destination"],
                      "notice": "in-memory simulation; no data transmitted"}
        self.execution_count += 1
        outcome = Outcome("allow", "executed", "rcpt-" + uuid.uuid4().hex, result)
        self._receipts[key] = (fingerprint, copy.deepcopy(outcome))
        return self._emit(request, outcome, approval_ref)


def replay(events: list[dict], expected_head: str | None = None,
           expected_count: int | None = None) -> dict:
    """Validate a supplied chain and summarize it; NEVER execute recorded tools."""
    previous = "0" * 64
    counts: Counter = Counter()
    for sequence, event in enumerate(events, 1):
        body = {key: value for key, value in event.items() if key != "event_hash"}
        if event.get("sequence") != sequence or event.get("previous_hash") != previous:
            raise ValueError("Audit order/continuity mismatch")
        if event.get("event_hash") != digest(body):
            raise ValueError("Audit hash mismatch")
        previous = event["event_hash"]
        counts[event["decision"]] += 1
    if expected_head is not None and previous != expected_head:
        raise ValueError("Audit head mismatch")
    if expected_count is not None and len(events) != expected_count:
        raise ValueError("Audit count mismatch")
    return {"event_count": len(events), "head": previous, "decisions": dict(counts),
            "notice": "hash-chain consistency only; not authenticated or durable evidence"}

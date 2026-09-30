from dataclasses import replace
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch
import copy
import time
import unittest

from runtime.golden import run_case, run_suite
from runtime.safety import Policy, Request, SafetyEngine, replay


class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.now = [1000.0]
        self.engine = SafetyEngine(clock=lambda: self.now[0])
        self.request = Request("r1", "analyst_a", "export_records",
                               {"tenant": "tenant_a", "limit": 2, "destination": "internal://audit"})

    def test_golden_suite(self):
        report = run_suite(Path(__file__).resolve().parents[1] / "evals/control-golden.json")
        self.assertEqual(report["passed"], report["total"], report)
        self.assertFalse(report["model_evaluated"])

    def test_wrong_role_cannot_approve(self):
        with self.assertRaises(PermissionError):
            self.engine.approve(self.request, "analyst_a")

    def test_wrong_tenant_cannot_approve(self):
        with self.assertRaises(PermissionError):
            self.engine.approve(self.request, "reviewer_b")

    def test_unknown_approval_fails_closed(self):
        result = self.engine.execute(self.request, "not-issued")
        self.assertEqual(result.reason, "approval_unknown")
        self.assertEqual(self.engine.execution_count, 0)

    def test_non_string_approval_fails_closed(self):
        self.assertEqual(self.engine.execute(self.request, []).reason, "approval_unknown")

    def test_invalid_proposal_cannot_be_approved(self):
        with self.assertRaises(ValueError):
            self.engine.approve(replace(self.request, parameters={}), "reviewer_a")

    def test_read_does_not_need_approval(self):
        request = Request("r2", "analyst_a", "read_metric", {"tenant": "tenant_a", "metric": "dau"})
        self.assertEqual(self.engine.execute(request).result["value"], 1200)

    def test_approval_binds_policy_content_not_only_version(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.engine.policy = replace(self.engine.policy, max_rows=50)
        self.assertEqual(self.engine.execute(self.request, token).reason, "approval_mismatch")

    def test_idempotency_does_not_return_stale_policy_result(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.engine.execute(self.request, token)
        self.engine.policy = replace(self.engine.policy, version="new")
        self.assertEqual(self.engine.execute(self.request, token).reason, "idempotency_conflict")
        self.assertEqual(self.engine.execution_count, 1)

    def test_cached_result_does_not_bypass_kill_switch(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.engine.execute(self.request, token)
        self.engine.disabled = True
        self.assertEqual(self.engine.execute(self.request, token).reason, "kill_switch")
        self.assertEqual(self.engine.execution_count, 1)

    def test_cached_retry_needs_no_new_execution_after_expiry(self):
        token = self.engine.approve(self.request, "reviewer_a")
        first = self.engine.execute(self.request, token)
        self.now[0] += 100
        second = self.engine.execute(self.request)
        self.assertTrue(second.cached)
        self.assertEqual(first.receipt_ref, second.receipt_ref)
        self.assertEqual(self.engine.execution_count, 1)

    def test_mutation_of_returned_result_does_not_change_cached_receipt(self):
        token = self.engine.approve(self.request, "reviewer_a")
        result = self.engine.execute(self.request, token)
        result.result["record_refs"].clear()
        self.assertEqual(len(self.engine.execute(self.request).result["record_refs"]), 2)

    def test_mutation_of_original_parameters_invalidates_approval(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.request.parameters["limit"] = 3
        self.assertEqual(self.engine.execute(self.request, token).reason, "approval_mismatch")

    def test_non_json_proposal_rejected(self):
        request = replace(self.request, parameters={"bad": object()})
        self.assertEqual(self.engine.execute(request).reason, "invalid_request")

    def test_nan_proposal_rejected(self):
        request = replace(self.request, parameters={**self.request.parameters, "limit": float("nan")})
        self.assertEqual(self.engine.execute(request).reason, "invalid_request")

    def test_negative_limit_rejected(self):
        request = replace(self.request, parameters={**self.request.parameters, "limit": -1})
        self.assertEqual(self.engine.execute(request).reason, "row_budget")

    def test_float_limit_rejected(self):
        request = replace(self.request, parameters={**self.request.parameters, "limit": 2.0})
        self.assertEqual(self.engine.execute(request).reason, "row_budget")

    def test_missing_field_rejected(self):
        params = copy.deepcopy(self.request.parameters)
        del params["destination"]
        self.assertEqual(self.engine.execute(replace(self.request, parameters=params)).reason, "invalid_parameters")

    def test_audit_does_not_log_raw_results_or_parameters(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.engine.execute(self.request, token)
        for event in self.engine.events:
            self.assertNotIn("parameters", event)
            self.assertNotIn("result", event)
            self.assertEqual(len(event["request_digest"]), 64)

    def test_audit_return_is_a_copy(self):
        self.engine.execute(self.request)
        self.engine.events[0]["decision"] = "allow"
        self.assertEqual(self.engine.events[0]["decision"], "review")

    def test_audit_tampering_detected(self):
        self.engine.execute(self.request)
        events = self.engine.events
        events[0]["decision"] = "allow"
        with self.assertRaises(ValueError):
            replay(events)

    def test_audit_deletion_detected_with_anchor(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.engine.execute(self.request, token)
        events = self.engine.events
        with self.assertRaises(ValueError):
            replay(events[:-1], expected_head=events[-1]["event_hash"], expected_count=len(events))

    def test_audit_reordering_detected(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.engine.execute(self.request, token)
        with self.assertRaises(ValueError):
            replay(list(reversed(self.engine.events)))

    def test_replay_is_non_executing(self):
        self.engine.execute(self.request)
        before = self.engine.execution_count
        replay(self.engine.events)
        self.assertEqual(self.engine.execution_count, before)

    def test_unregistered_policy_tool_rejected(self):
        with self.assertRaises(ValueError):
            Policy(allowed_tools=("shell",))

    def test_zero_ttl_rejected(self):
        with self.assertRaises(ValueError):
            Policy(approval_ttl_seconds=0)

    def test_concurrent_retries_execute_once_and_keep_one_receipt(self):
        token = self.engine.approve(self.request, "reviewer_a")
        barrier = Barrier(16)
        original = self.engine._run_synthetic

        def slow_simulation(request):
            time.sleep(0.01)  # Widen the old check-then-execute race, without a barrier inside the lock.
            return original(request)

        def execute_once(_):
            barrier.wait(timeout=5)
            return self.engine.execute(self.request, token)

        with patch.object(self.engine, "_run_synthetic", side_effect=slow_simulation) as simulation:
            with ThreadPoolExecutor(max_workers=16) as pool:
                outcomes = list(pool.map(execute_once, range(16)))
            self.assertEqual(simulation.call_count, 1)
        self.assertEqual(self.engine.execution_count, 1)
        self.assertEqual(len({row.receipt_ref for row in outcomes}), 1)
        self.assertEqual(sum(row.cached for row in outcomes), 15)
        self.assertTrue(all(row.decision == "allow" for row in outcomes))
        self.assertEqual(replay(self.engine.events)["event_count"], 17)

    def test_concurrent_same_id_different_parameters_cannot_both_execute(self):
        changed = replace(self.request, parameters={**self.request.parameters, "limit": 3})
        proposals = [(self.request, self.engine.approve(self.request, "reviewer_a")),
                     (changed, self.engine.approve(changed, "reviewer_a"))]
        barrier = Barrier(2)

        def execute_once(proposal):
            barrier.wait(timeout=5)
            return self.engine.execute(*proposal)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(execute_once, proposals))
        self.assertEqual({row.reason for row in outcomes}, {"executed", "idempotency_conflict"})
        self.assertEqual(self.engine.execution_count, 1)
        self.assertEqual(replay(self.engine.events)["event_count"], 4)

    def test_concurrent_approvals_keep_audit_chain_continuous(self):
        barrier = Barrier(16)

        def approve_once(index):
            barrier.wait(timeout=5)
            return self.engine.approve(replace(self.request, request_id=f"parallel-{index}"), "reviewer_a")

        with ThreadPoolExecutor(max_workers=16) as pool:
            tokens = list(pool.map(approve_once, range(16)))
        self.assertEqual(len(set(tokens)), 16)
        self.assertEqual(replay(self.engine.events)["event_count"], 16)
        self.assertEqual(self.engine.execution_count, 0)

    def test_audit_distinguishes_requester_and_reviewer(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.engine.execute(self.request, token)
        approval, execution = self.engine.events
        self.assertEqual(approval["identity_ref"], "analyst_a")
        self.assertEqual(approval["actor_ref"], "reviewer_a")
        self.assertEqual(approval["actor_role"], "reviewer")
        self.assertEqual(approval["approved_by"], "reviewer_a")
        self.assertEqual(execution["actor_ref"], "analyst_a")
        self.assertEqual(execution["actor_role"], "requester")
        self.assertEqual(execution["approved_by"], "reviewer_a")
        self.assertEqual(execution["approval_ref"], approval["approval_ref"])

    def test_cached_replay_preserves_original_approval_context(self):
        token = self.engine.approve(self.request, "reviewer_a")
        self.engine.execute(self.request, token)
        self.engine.execute(self.request)
        event = self.engine.events[-1]
        self.assertEqual(event["reason_code"], "idempotent_replay")
        self.assertEqual(event["approval_ref"], token)
        self.assertEqual(event["approved_by"], "reviewer_a")

    def test_control_reasons_have_semantic_risk_labels(self):
        proposals = [
            (replace(self.request, parameters={**self.request.parameters, "limit": 101}), "resource-abuse"),
            (replace(self.request, parameters={**self.request.parameters, "destination": "https://example.invalid"}), "privacy"),
            (replace(self.request, parameters={**self.request.parameters, "tenant": "tenant_b"}), "privacy"),
            (Request("metric", "analyst_a", "read_metric", {"tenant": "tenant_a", "metric": "raw_user_phone"}), "privacy"),
        ]
        for request, risk_id in proposals:
            with self.subTest(risk_id=risk_id, parameters=request.parameters):
                self.engine.execute(request)
                self.assertEqual(self.engine.events[-1]["risk_ids"], [risk_id])
        self.engine.disabled = True
        self.engine.execute(self.request)
        self.assertEqual(self.engine.events[-1]["risk_ids"], ["model-governance"])

    def test_golden_cannot_pass_with_wrong_event_risk_label(self):
        case = {"id": "semantic-regression", "slice": "risky", "risk_ids": ["privacy"],
                "requests": {"base": {"request_id": "r1", "principal": "analyst_a", "tool": "export_records",
                                      "parameters": {"tenant": "tenant_a", "limit": 101, "destination": "internal://audit"}}},
                "actions": [{"operation": "execute", "request": "base"}],
                "expected": {"decision": "block", "reason": "row_budget", "executions": 0,
                             "risk_ids": ["tool-authority"]}}
        result = run_case(case)
        self.assertFalse(result["passed"])
        self.assertEqual(result["observed"]["risk_ids"], ["resource-abuse"])

    def test_restart_loses_approval_and_fails_closed(self):
        token = self.engine.approve(self.request, "reviewer_a")
        restarted = SafetyEngine(clock=lambda: self.now[0])
        self.assertEqual(restarted.execute(self.request, token).reason, "approval_unknown")
        self.assertEqual(restarted.execution_count, 0)

    def test_separate_instances_do_not_share_idempotency(self):
        other = SafetyEngine(clock=lambda: self.now[0])
        for engine in (self.engine, other):
            token = engine.approve(self.request, "reviewer_a")
            self.assertEqual(engine.execute(self.request, token).reason, "executed")
        # An explicit limit regression: this is NOT a cross-process guarantee.
        self.assertEqual(self.engine.execution_count + other.execution_count, 2)

    def test_read_ignores_unrelated_caller_approval(self):
        token = self.engine.approve(self.request, "reviewer_a")
        request = Request("metric", "analyst_a", "read_metric", {"tenant": "tenant_a", "metric": "dau"})
        self.engine.execute(request, token)
        self.assertIsNone(self.engine.events[-1]["approval_ref"])
        self.assertIsNone(self.engine.events[-1]["approved_by"])

    def test_invalid_policy_replacement_rejected(self):
        with self.assertRaises(TypeError):
            self.engine.policy = "not-a-policy"

    def test_non_boolean_kill_switch_rejected(self):
        with self.assertRaises(TypeError):
            self.engine.disabled = "false"

    def test_failed_simulation_does_not_cache_success(self):
        token = self.engine.approve(self.request, "reviewer_a")
        with patch.object(self.engine, "_run_synthetic", side_effect=RuntimeError("synthetic failure")):
            with self.assertRaises(RuntimeError):
                self.engine.execute(self.request, token)
        self.assertEqual(self.engine.execution_count, 0)
        self.assertEqual(self.engine.execute(self.request, token).reason, "executed")
        self.assertEqual(self.engine.execution_count, 1)


if __name__ == "__main__":
    unittest.main()

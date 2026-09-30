from dataclasses import replace
from pathlib import Path
import copy
import unittest

from runtime.golden import run_suite
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


if __name__ == "__main__":
    unittest.main()

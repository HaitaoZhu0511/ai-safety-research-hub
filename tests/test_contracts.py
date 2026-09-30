from dataclasses import replace
from datetime import datetime
from pathlib import Path
import json
import unittest

from jsonschema import Draft202012Validator, ValidationError
from runtime.safety import Request, SafetyEngine


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "contracts/risk-event.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)

    def setUp(self):
        engine = SafetyEngine()
        request = Request("r1", "analyst_a", "export_records",
                          {"tenant": "tenant_a", "limit": 2, "destination": "internal://audit"})
        engine.execute(request)
        token = engine.approve(request, "reviewer_a")
        engine.execute(request, token)
        engine.execute(replace(request, parameters={**request.parameters, "tenant": "tenant_b"}))
        self.events = engine.events

    def test_generated_events_satisfy_contract(self):
        for event in self.events:
            self.validator.validate(event)
            timestamp = datetime.fromisoformat(event["timestamp"])
            self.assertIsNotNone(timestamp.tzinfo)

    def test_block_requires_risk(self):
        event = self.events[-1]
        event["risk_ids"] = []
        with self.assertRaises(ValidationError):
            self.validator.validate(event)

    def test_evidence_cannot_be_empty(self):
        event = self.events[0]
        event["evidence_refs"] = []
        with self.assertRaises(ValidationError):
            self.validator.validate(event)

    def test_execution_needs_receipt(self):
        event = self.events[2]
        event["execution_receipt_ref"] = None
        with self.assertRaises(ValidationError):
            self.validator.validate(event)

    def test_hash_shape(self):
        event = self.events[0]
        event["event_hash"] = "invalid"
        with self.assertRaises(ValidationError):
            self.validator.validate(event)

    def test_unknown_fields_rejected(self):
        event = self.events[0]
        event["raw_content"] = "must not be logged"
        with self.assertRaises(ValidationError):
            self.validator.validate(event)


if __name__ == "__main__":
    unittest.main()

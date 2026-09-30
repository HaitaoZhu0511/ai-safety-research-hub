import unittest
from scripts.cost_model import calculate


class CostModelTests(unittest.TestCase):
    def test_documented_hypothesis(self):
        result = calculate()
        self.assertEqual(result["net_daily_hypothetical_value"], 4200)
        self.assertEqual(result["simple_payback_days"], 72)
        self.assertFalse(result["cash_savings_validated"])

    def test_no_positive_payback(self):
        self.assertIsNone(calculate(new_rate=0.2)["simple_payback_days"])

    def test_rate_above_one(self):
        with self.assertRaises(ValueError):
            calculate(new_rate=1.1)

    def test_negative_cost(self):
        with self.assertRaises(ValueError):
            calculate(added_daily_cost=-1)

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):
            calculate(investment=float("inf"))


if __name__ == "__main__":
    unittest.main()

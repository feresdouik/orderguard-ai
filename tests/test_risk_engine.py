import unittest

import pandas as pd

from risk_engine import REQUIRED_COLUMNS, assess_order, prepare_orders


class RiskEngineTests(unittest.TestCase):
    def make_row(self, **overrides):
        values = {
            "order_id": "TEST-1",
            "customer": "Demo Customer",
            "phone": "20123456",
            "address": "Sousse",
            "total": 100,
            "previous_orders": 3,
            "notes": "",
        }
        values.update(overrides)
        return pd.Series(values)

    def test_clean_order_is_low_risk(self):
        score, level, reasons, _ = assess_order(self.make_row())
        self.assertEqual(score, 0)
        self.assertEqual(level, "Low")
        self.assertIn("No rule-based warning", reasons)

    def test_missing_phone_and_address_reach_high_risk(self):
        score, level, _, _ = assess_order(self.make_row(phone="", address=""))
        self.assertEqual(score, 55)
        self.assertEqual(level, "High")

    def test_score_is_capped_at_100(self):
        score, _, _, _ = assess_order(
            self.make_row(phone="", address="", previous_orders=0, total=500, notes="urgent cancel")
        )
        self.assertEqual(score, 100)

    def test_medium_threshold_is_inclusive(self):
        score, level, _, _ = assess_order(self.make_row(phone="", previous_orders=0))
        self.assertEqual(score, 45)
        self.assertEqual(level, "Medium")

    def test_prepare_orders_flags_invalid_numeric_data(self):
        raw = pd.DataFrame(
            [["", "", "", "", "not-a-number", "unknown", ""]],
            columns=REQUIRED_COLUMNS,
        )
        result = prepare_orders(raw)
        self.assertEqual(len(result), 1)
        self.assertIn("Missing order ID", result.iloc[0].data_issues)
        self.assertIn("Missing customer name", result.iloc[0].data_issues)
        self.assertIn("Invalid order value", result.iloc[0].data_issues)
        self.assertIn("Invalid order history", result.iloc[0].data_issues)
        self.assertEqual(float(result.iloc[0].total), 0.0)


if __name__ == "__main__":
    unittest.main()

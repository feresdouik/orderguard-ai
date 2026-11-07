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

    def test_duplicate_order_ids_are_flagged_on_both_rows(self):
        raw = pd.DataFrame(
            [
                ["DUP-1", "First", "20123456", "Sousse", 50, 1, ""],
                ["DUP-1", "Second", "22123456", "Tunis", 60, 2, ""],
            ],
            columns=REQUIRED_COLUMNS,
        )
        result = prepare_orders(raw)
        self.assertEqual(int(result.data_issues.str.contains("Duplicate order ID").sum()), 2)

    def test_negative_values_are_flagged(self):
        raw = pd.DataFrame(
            [["NEG-1", "Demo", "20123456", "Sousse", -10, -2, ""]],
            columns=REQUIRED_COLUMNS,
        )
        result = prepare_orders(raw)
        self.assertIn("Negative order value", result.iloc[0].data_issues)
        self.assertIn("Negative order history", result.iloc[0].data_issues)
        self.assertEqual(float(result.iloc[0].total), -10.0)
        self.assertEqual(float(result.iloc[0].previous_orders), -2.0)

    def test_infinite_numeric_values_are_flagged_and_safely_replaced(self):
        raw = pd.DataFrame(
            [["INF-1", "Demo", "20123456", "Sousse", float("inf"), float("-inf"), ""]],
            columns=REQUIRED_COLUMNS,
        )
        result = prepare_orders(raw)
        self.assertIn("Invalid order value", result.iloc[0].data_issues)
        self.assertIn("Invalid order history", result.iloc[0].data_issues)
        self.assertEqual(float(result.iloc[0].total), 0.0)
        self.assertEqual(float(result.iloc[0].previous_orders), 0.0)

    def test_missing_required_columns_raise_clear_error(self):
        raw = pd.DataFrame({"order_id": ["A-1"]})
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            prepare_orders(raw)

    def test_duplicate_detection_ignores_blank_ids(self):
        raw = pd.DataFrame(
            [
                ["", "First", "20123456", "Sousse", 50, 1, ""],
                ["", "Second", "22123456", "Tunis", 60, 2, ""],
            ],
            columns=REQUIRED_COLUMNS,
        )
        result = prepare_orders(raw)
        self.assertEqual(int(result.data_issues.str.contains("Duplicate order ID").sum()), 0)


if __name__ == "__main__":
    unittest.main()

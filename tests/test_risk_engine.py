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

    # --- Fix 1: NaN contact fields passed directly to assess_order ---

    def test_nan_phone_triggers_missing_phone_penalty(self):
        score, _, reasons, _ = assess_order(self.make_row(phone=float("nan")))
        self.assertEqual(score, 30)
        self.assertIn("Phone number is missing", reasons)

    def test_nan_address_triggers_missing_address_penalty(self):
        score, _, reasons, _ = assess_order(self.make_row(address=float("nan")))
        self.assertEqual(score, 25)
        self.assertIn("Delivery address is missing", reasons)

    # --- Fix 2: invalid previous_orders must not inflate the risk score ---

    def test_invalid_previous_orders_does_not_trigger_no_history_penalty(self):
        """An unparseable previous_orders value must NOT add the +15 no-history penalty."""
        raw = pd.DataFrame(
            [["BAD-1", "Demo", "20123456", "Sousse", 100, "unknown", ""]],
            columns=REQUIRED_COLUMNS,
        )
        result = prepare_orders(raw)
        self.assertIn("Invalid order history", result.iloc[0].data_issues)
        self.assertNotIn("No previous successful orders recorded", result.iloc[0].risk_reasons)

    def test_valid_zero_previous_orders_still_triggers_penalty(self):
        """A genuine previous_orders=0 (valid zero) must still add +15."""
        score, _, reasons, _ = assess_order(self.make_row(previous_orders=0))
        self.assertEqual(score, 15)
        self.assertIn("No previous successful orders recorded", reasons)

    def test_previous_orders_one_does_not_trigger_penalty(self):
        score, _, _, _ = assess_order(self.make_row(previous_orders=1))
        self.assertEqual(score, 0)

    # --- Individual suspicious note keywords ---

    def test_note_keyword_urgent_triggers_penalty(self):
        _, _, reasons, _ = assess_order(self.make_row(notes="urgent delivery"))
        self.assertIn("Order note needs manual review", reasons)

    def test_note_keyword_cancel_triggers_penalty(self):
        _, _, reasons, _ = assess_order(self.make_row(notes="please cancel this"))
        self.assertIn("Order note needs manual review", reasons)

    def test_note_keyword_fake_triggers_penalty(self):
        _, _, reasons, _ = assess_order(self.make_row(notes="fake address"))
        self.assertIn("Order note needs manual review", reasons)

    def test_note_keyword_change_address_triggers_penalty(self):
        _, _, reasons, _ = assess_order(self.make_row(notes="please change address"))
        self.assertIn("Order note needs manual review", reasons)

    def test_benign_note_does_not_trigger_penalty(self):
        score, _, _, _ = assess_order(self.make_row(notes="confirmed size and color"))
        self.assertEqual(score, 0)

    # --- total boundary values: 249 / 250 / 251 ---

    def test_total_below_threshold_does_not_trigger_high_value_penalty(self):
        score, _, _, _ = assess_order(self.make_row(total=249))
        self.assertEqual(score, 0)

    def test_total_at_threshold_triggers_high_value_penalty(self):
        score, _, reasons, _ = assess_order(self.make_row(total=250))
        self.assertEqual(score, 10)
        self.assertIn("Order value is relatively high", reasons)

    def test_total_above_threshold_triggers_high_value_penalty(self):
        score, _, _, _ = assess_order(self.make_row(total=251))
        self.assertEqual(score, 10)

    # --- Output sort order ---

    def test_prepare_orders_sorts_by_descending_risk_score(self):
        raw = pd.DataFrame(
            [
                ["LOW-1",  "Alice", "20123456", "Sousse",   50, 5, ""],   # score 0
                ["HIGH-1", "Bob",   "",          "Tunis",   50, 0, ""],   # score 45 (missing phone + no history)
                ["MED-1",  "Carol", "",          "Monastir", 50, 3, ""],  # score 30 (missing phone)
            ],
            columns=REQUIRED_COLUMNS,
        )
        result = prepare_orders(raw)
        scores = result["risk_score"].tolist()
        self.assertEqual(scores, sorted(scores, reverse=True))

    # --- Headers-only (zero data rows) DataFrame ---

    def test_prepare_orders_with_zero_data_rows_returns_empty_frame(self):
        raw = pd.DataFrame(columns=REQUIRED_COLUMNS)
        result = prepare_orders(raw)
        self.assertEqual(len(result), 0)
        expected_cols = set(REQUIRED_COLUMNS) | {"data_issues", "risk_score", "risk_level", "risk_reasons", "recommended_action"}
        self.assertEqual(set(result.columns), expected_cols)


if __name__ == "__main__":
    unittest.main()

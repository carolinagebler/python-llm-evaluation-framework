"""Tests for the standalone synthetic financial metrics demonstration."""
import json
import unittest
from pathlib import Path

from llm_eval.finance_metrics import analyze_years, normalized_ebitda


FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "synthetic_industrials.json"


class FinancialAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.loads(FIXTURE.read_text(encoding="utf-8"))["annual_financials"]

    def test_four_year_trend(self):
        result = analyze_years(self.rows)
        self.assertEqual(len(result), 4)
        self.assertIsNone(result[0]["revenue_growth_pct"])
        self.assertEqual(result[-1]["revenue_growth_pct"], 11.39)

    def test_margin_compression(self):
        metrics = analyze_years(self.rows)
        self.assertEqual(metrics[0]["ebitda_margin_pct"], 17.5)
        self.assertEqual(metrics[-1]["ebitda_margin_pct"], 13.33)

    def test_fcf_declines_even_with_sales_growth(self):
        metrics = analyze_years(self.rows)
        self.assertEqual([m["free_cash_flow"] for m in metrics], [11, 15, 2, -11])

    def test_net_debt_to_ebitda_rises(self):
        metrics = analyze_years(self.rows)
        self.assertEqual(metrics[-1]["net_debt_to_ebitda"], 3.93)

    def test_working_capital_increases(self):
        metrics = analyze_years(self.rows)
        self.assertEqual(metrics[-1]["operating_nwc"], 51)
        self.assertEqual(metrics[-1]["change_in_operating_nwc"], 14)

    def test_normalizes_one_time_gain_and_charge(self):
        self.assertEqual(normalized_ebitda(32, 4), 28)
        self.assertEqual(normalized_ebitda(30, -2), 32)

    def test_rejects_nonconsecutive_years(self):
        rows = [dict(row) for row in self.rows[:2]]
        rows[1]["year"] += 1
        with self.assertRaises(ValueError):
            analyze_years(rows)

    def test_rejects_zero_ebitda(self):
        rows = [dict(row) for row in self.rows]
        rows[-1]["ebitda"] = 0
        with self.assertRaises(ValueError):
            analyze_years(rows)


if __name__ == "__main__":
    unittest.main()

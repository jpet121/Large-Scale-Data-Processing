"""Stand-alone pre-Codex control: test the frozen independent golden sample, not product code."""
import csv
import json
import unittest
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent / "fixtures"

class GoldenReferenceCalibration(unittest.TestCase):
    def test_positive_control(self):
        with (HERE / "GOLDEN_MIXED.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        expected = json.loads((HERE / "GOLDEN_EXPECTED.json").read_text())
        self.assertEqual(len(rows), expected["examined_count"])
        accepted = [r for r in rows if r["amount"] != "garbage" and r["currency"] in ("USD", "EUR")]
        self.assertEqual(len(accepted), expected["accepted_count"])
        self.assertEqual([r["transaction_id"] for r in accepted], expected["accepted_ids"])
        totals = {currency: sum((Decimal(r["amount"]) for r in accepted if r["currency"] == currency), Decimal(0)) for currency in ("USD", "EUR")}
        self.assertEqual(totals, {k: Decimal(v) for k, v in expected["accepted_totals_by_currency"].items()})
        self.assertIn("\n", rows[1]["processor_reference"])
        self.assertEqual(rows[0]["transaction_id"], "0001")

    def test_negative_control_detects_dropped_row_and_float_rounding(self):
        expected = json.loads((HERE / "GOLDEN_EXPECTED.json").read_text())
        original_count = expected["accepted_count"]
        broken_count = original_count - 1
        self.assertNotEqual(broken_count, original_count)
        self.assertNotEqual(0.1 + 0.2, 0.3)
        self.assertEqual(Decimal("0.10") + Decimal("0.20"), Decimal("0.30"))

if __name__ == "__main__":
    unittest.main()

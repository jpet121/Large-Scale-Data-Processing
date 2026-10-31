"""Frozen source-derived black-box acceptance tests; execute only after Codex builds main.py.

The TEST_ONLY_SCHEMA.json is an explicit fixture policy, not a currency/format policy
that the owner supplied for financial production. No mocks or runtime patching.
"""
from __future__ import annotations
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

HERE=Path(__file__).resolve().parent
APP=HERE.parent
F=HERE / "fixtures"

class StreamingAcceptance(unittest.TestCase):
    def run_app(self, source, out_dir, *extra):
        return subprocess.run([sys.executable,str(APP/"main.py"),"--input",str(source),"--output",str(out_dir),"--schema",str(F/"TEST_ONLY_SCHEMA.json"),*extra],capture_output=True,text=True,timeout=60,check=False)

    def test_golden_mixed_exact_decimal_reconciliation_and_row_order(self):
        with tempfile.TemporaryDirectory() as td:
            res=self.run_app(F/"GOLDEN_MIXED.csv",Path(td)/"results", "--batch-size", "1")
            self.assertEqual(res.returncode,2,res.stderr)
            output=Path(td)/"results"
            self.assertTrue((output/"COMMITTED.json").is_file(),res.stderr)
            report=json.loads((output/"summary.json").read_text(encoding="utf-8"))
            expected=json.loads((F/"GOLDEN_EXPECTED.json").read_text(encoding="utf-8"))
            for key in ("examined_count","accepted_count","rejected_count","complete","status"):
                self.assertEqual(report[key],expected[key])
            self.assertEqual(report["accepted_count"]+report["rejected_count"],report["examined_count"])
            self.assertEqual(report["input_size_bytes"],(F/"GOLDEN_MIXED.csv").stat().st_size)
            self.assertEqual({k:Decimal(str(v)) for k,v in report["accepted_totals_by_currency"].items()}, {k:Decimal(v) for k,v in expected["accepted_totals_by_currency"].items()})
            self.assertTrue(report["started_at_utc"])
            self.assertTrue(report["completed_at_utc"])
            self.assertGreaterEqual(report["duration_seconds"],0)
            self.assertGreaterEqual(report["throughput_records_per_second"],0)
            with (output/"validated.csv").open(newline="",encoding="utf-8") as handle:
                accepted=list(csv.DictReader(handle))
            self.assertEqual([r["transaction_id"] for r in accepted],expected["accepted_ids"])
            self.assertEqual(accepted[0]["transaction_id"],"0001")
            self.assertEqual(accepted[0]["processor_reference"],"processor, east")
            self.assertEqual(accepted[1]["processor_reference"],'processor "west"\nsecond line')
            with (output/"rejected.csv").open(newline="",encoding="utf-8") as handle:
                rejected=list(csv.DictReader(handle))
            self.assertEqual(len(rejected),2)
            self.assertEqual({r["error_code"] for r in rejected},{"INVALID_AMOUNT","UNSUPPORTED_CURRENCY"})
            self.assertTrue(all(r["source_record_number"] for r in rejected))
            self.assertTrue(all(r["raw_record"] for r in rejected))
            self.assertNotIn("0012",res.stderr)
            self.assertNotIn("processor, east",res.stdout+res.stderr)

    def test_header_only_succeeds_with_zero_counts(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"header.csv"
            policy=json.loads((F/"TEST_ONLY_SCHEMA.json").read_text())
            with p.open("w",newline="",encoding="utf-8") as f:csv.writer(f).writerow(policy["columns"])
            out=Path(td)/"out"
            res=self.run_app(p,out)
            self.assertEqual(res.returncode,0,res.stderr)
            self.assertTrue((out/"COMMITTED.json").exists())
            summary=json.loads((out/"summary.json").read_text())
            self.assertEqual([summary["examined_count"],summary["accepted_count"],summary["rejected_count"]],[0,0,0])
            self.assertEqual(summary["status"],"SUCCESS")
            self.assertTrue(summary["complete"])

    def test_gzip_same_logical_totals_as_plain(self):
        import gzip
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"input.csv.gz"
            with gzip.open(p,"wb") as f:f.write((F/"GOLDEN_MIXED.csv").read_bytes())
            out=Path(td)/"out"
            res=self.run_app(p,out)
            self.assertEqual(res.returncode,2,res.stderr)
            summary=json.loads((out/"summary.json").read_text())
            self.assertEqual([summary["examined_count"],summary["accepted_count"],summary["rejected_count"]],[5,3,2])

if __name__ == "__main__":unittest.main()

"""Frozen negative and idempotence cases. Tests real CLI subprocesses without mocks."""
from __future__ import annotations
import csv
import json
import gzip
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
FIX=HERE/"fixtures"
APP=HERE.parent

class FailureAcceptance(unittest.TestCase):
    def invoke(self,p,out,*options):
        return subprocess.run([sys.executable,str(APP/"main.py"),"--input",str(p),"--output",str(out),"--schema",str(FIX/"TEST_ONLY_SCHEMA.json"),*options],capture_output=True,text=True,timeout=60,check=False)

    def test_truncated_gzip_never_commits(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"broken.csv.gz"
            good=gzip.compress((FIX/"GOLDEN_MIXED.csv").read_bytes())
            p.write_bytes(good[:-6])
            out=Path(td)/"out"
            result=self.invoke(p,out)
            self.assertEqual(result.returncode,1,result.stderr)
            self.assertFalse((out/"COMMITTED.json").exists())

    def test_unterminated_quote_never_commits(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"unclosed.csv"
            p.write_text(','.join(json.loads((FIX/"TEST_ONLY_SCHEMA.json").read_text())["columns"])+"\n"+'"no-quote-end,field',encoding="utf-8")
            out=Path(td)/"out"
            r=self.invoke(p,out)
            self.assertEqual(r.returncode,1,r.stderr)
            self.assertFalse((out/"COMMITTED.json").exists())

    def test_zero_byte_and_invalid_batch_size_fatal(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"empty.csv";p.write_bytes(b"")
            out=Path(td)/"out"
            self.assertEqual(self.invoke(p,out).returncode,1)
            self.assertFalse((out/"COMMITTED.json").exists())
            q=FIX/"GOLDEN_MIXED.csv"
            self.assertEqual(self.invoke(q,Path(td)/"badbatch","--batch-size","0").returncode,1)

    def test_repeated_run_never_appends(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"out";p=FIX/"GOLDEN_MIXED.csv"
            first=self.invoke(p,out)
            self.assertEqual(first.returncode,2,first.stderr)
            prior=(out/"validated.csv").read_bytes()
            second=self.invoke(p,out)
            self.assertEqual(second.returncode,1,second.stderr)
            self.assertEqual((out/"validated.csv").read_bytes(),prior)

    def test_oversized_record_fails_without_commit(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"big.csv"
            p.write_bytes((FIX/"GOLDEN_MIXED.csv").read_bytes())
            out=Path(td)/"out"
            r=self.invoke(p,out,"--max-record-bytes","30")
            self.assertEqual(r.returncode,1,r.stderr)
            self.assertFalse((out/"COMMITTED.json").exists())

if __name__ == "__main__":unittest.main()

"""Finite executable-model correspondence and real process lifecycle checks."""
import csv
from decimal import Decimal
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from streaming_csv_parser.config import Limits, load_policy
from streaming_csv_parser.orchestrator import run

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT/'tests/fixtures'


class ProtocolTests(unittest.TestCase):
    def test_finite_reconciliation_model_correspondence(self):
        policy = load_policy(FIX/'TEST_ONLY_SCHEMA.json')
        with (FIX/'GOLDEN_MIXED.csv').open(newline='') as handle:
            reader = csv.reader(handle)
            header, row = next(reader), next(reader)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index = 0
            for length in range(5):
                for decisions in itertools.product((False, True), repeat=length):
                    source = root/f'{index}.csv'
                    with source.open('w', newline='') as handle:
                        writer = csv.writer(handle)
                        writer.writerow(header)
                        for valid in decisions:
                            candidate = row.copy()
                            candidate[4] = '0.10' if valid else 'invalid'
                            writer.writerow(candidate)
                    out = root/f'out{index}'
                    report = run(source, out, policy, Limits())
                    accepted = sum(decisions)
                    self.assertEqual(report['examined_count'], length)
                    self.assertEqual(report['accepted_count'], accepted)
                    self.assertEqual(report['rejected_count'], length-accepted)
                    self.assertTrue(report['complete'])
                    self.assertTrue((out/'COMMITTED.json').exists())
                    self.assertEqual(Decimal(report['accepted_totals_by_currency'].get('USD', '0')), Decimal(accepted)/10)
                    index += 1
            self.assertEqual(index, 31)

    def test_two_processes_same_target_and_sigterm_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root/'race'
            command = [sys.executable, str(ROOT/'main.py'), '--input', str(FIX/'GOLDEN_MIXED.csv'), '--output', str(out), '--schema', str(FIX/'TEST_ONLY_SCHEMA.json')]
            children = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
            results = []
            for child in children:
                child.communicate(timeout=30)
                results.append(child.returncode)
            self.assertEqual(sorted(results), [1, 2])
            self.assertEqual(json.loads((out/'summary.json').read_text())['examined_count'], 5)
            source = root/'long.csv'
            data = (FIX/'GOLDEN_MIXED.csv').read_bytes()
            header, first, *_ = data.splitlines(keepends=True)
            with source.open('wb') as handle:
                handle.write(header)
                for _ in range(200000):
                    handle.write(first)
            target = root/'interrupted'
            command[3] = str(source)
            command[5] = str(target)
            child = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                deadline = time.monotonic()+10
                while time.monotonic() < deadline:
                    accepted = target/'validated.csv'
                    if accepted.exists() and accepted.stat().st_size > 8192:
                        break
                    self.assertIsNone(child.poll(), 'child exited before observable write')
                    time.sleep(0.005)
                else:
                    self.fail('No observable write checkpoint')
                child.terminate()
                child.wait(timeout=10)
                self.assertLess(child.returncode, 0)
                self.assertFalse((target/'COMMITTED.json').exists())
            finally:
                if child.poll() is None:
                    child.kill()
                    child.wait()
            # Replay a known input into a fresh namespace after interruption.
            command[3] = str(FIX/'GOLDEN_MIXED.csv')
            command[5] = str(root/'replayed')
            completed = subprocess.run(command, capture_output=True, timeout=30)
            self.assertEqual(completed.returncode, 2)
            self.assertTrue((root/'replayed'/'COMMITTED.json').exists())

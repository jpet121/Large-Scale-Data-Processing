"""Direct boundary tests with concrete byte streams and clocks."""
import csv
import io
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from streaming_csv_parser.accounting import Ledger
from streaming_csv_parser.config import Limits, load_policy
from streaming_csv_parser.csv_stream import records
from streaming_csv_parser.diagnostics import Progress
from streaming_csv_parser.reader import physical_lines
from streaming_csv_parser.report import build_report
from streaming_csv_parser.seams import Clock, Events
from streaming_csv_parser.validation import validate

FIX = Path(__file__).parent / 'fixtures'


class FixedClock:
    def __init__(self, value=0):
        self.value = value
    def monotonic(self):
        return self.value
    def utc(self):
        return '2026-10-30T00:00:00+00:00'


class CoreTests(unittest.TestCase):
    def test_exact_large_totals_and_scales(self):
        ledger = Ledger()
        for value in ('9999999999999999999999999999.99', '0.01', '-0.100', '+1'):
            ledger.add('USD', value)
        ledger.add('EUR', '-2')
        self.assertEqual(ledger.strings(), {'USD': '10000000000000000000000000000.900', 'EUR': '-2'})
        ledger.add('EUR', '2')
        self.assertEqual(ledger.strings()['EUR'], '0')

    def test_physical_boundaries_cr_lf_and_limits(self):
        data = b'a\r\nb\rc\nd'
        for chunk in (1, 2, 3, 64):
            self.assertEqual(list(physical_lines(io.BytesIO(data), 4, chunk)), [b'a\r\n', b'b\r', b'c\n', b'd'])
        self.assertEqual(list(physical_lines(io.BytesIO(b''), 1)), [])
        for data in (b'abcd\n', b'abcd', b'a\r\n'):
            with self.assertRaisesRegex(ValueError, 'PHYSICAL_LINE_LIMIT'):
                list(physical_lines(io.BytesIO(data), 2, 1))

    def test_logical_records_preserve_multiline_and_spans(self):
        policy = load_policy(FIX / 'TEST_ONLY_SCHEMA.json')
        with (FIX / 'GOLDEN_MIXED.csv').open('rb') as source:
            rows = list(records(source, policy, Limits()))
        self.assertEqual(len(rows), 6)
        self.assertIn('\nsecond line', rows[2].fields[-1])
        self.assertEqual(rows[2].end - rows[2].start, 1)
        self.assertEqual(rows[1].number, 1)
        self.assertTrue(rows[2].raw.endswith('\n'))
        with self.assertRaisesRegex(ValueError, 'LOGICAL_RECORD_LIMIT'):
            list(records(io.BytesIO(b'"a\nb\nc\n"\n'), policy, Limits(max_record_bytes=6)))
        with self.assertRaises(UnicodeDecodeError):
            list(records(io.BytesIO(b'\xff\n'), policy, Limits()))
        with self.assertRaises(csv.Error):
            list(records(io.BytesIO(b'"unclosed'), policy, Limits()))

    def test_validation_invalid_and_boundary_cases(self):
        policy = load_policy(FIX / 'TEST_ONLY_SCHEMA.json')
        with (FIX / 'GOLDEN_MIXED.csv').open(newline='') as handle:
            reader = csv.reader(handle)
            next(reader)
            valid = next(reader)
        self.assertIsNone(validate(valid, policy))
        self.assertEqual(validate(valid[:-1], policy), 'COLUMN_COUNT')
        for index, value, reason in [(0, '', 'MISSING_REQUIRED'), (2, 'yesterday', 'INVALID_TIMESTAMP'), (4, 'NaN', 'INVALID_AMOUNT'), (4, '1e3', 'INVALID_AMOUNT'), (4, '1.123456789', 'INVALID_AMOUNT'), (4, '1' * 31, 'INVALID_AMOUNT'), (4, ' 1.00', 'INVALID_AMOUNT'), (5, 'ZZZ', 'UNSUPPORTED_CURRENCY')]:
            row = valid.copy()
            row[index] = value
            self.assertEqual(validate(row, policy), reason)
        from dataclasses import replace
        unsigned = replace(policy, allow_sign=False)
        row = valid.copy()
        row[4] = '-1'
        self.assertEqual(validate(row, unsigned), 'INVALID_AMOUNT')
        row[4] = '1'
        self.assertIsNone(validate(row, unsigned))

    def test_reports_and_sanitized_progress(self):
        clock = FixedClock()
        sink = io.StringIO()
        progress = Progress(clock=clock, sink=sink)
        progress.emit('PROGRESS', 1)
        self.assertEqual(sink.getvalue(), '')
        clock.value = 6
        progress.emit('PROGRESS', 5)
        progress.emit('SUCCESS', 5)
        self.assertEqual(sink.getvalue(), 'PROGRESS examined=5\nSUCCESS examined=5\n')
        report = build_report({}, clock, 0, clock.utc(), 5, 3, {'BAD': 2}, {'USD': '0.30'}, True)
        self.assertEqual(report['status'], 'PARTIAL')
        self.assertEqual(report['throughput_records_per_second'], 5/6)
        self.assertEqual(build_report({}, clock, 0, clock.utc(), 0, 0, {}, {}, False)['status'], 'FAILED')
        with self.assertRaisesRegex(ValueError, 'RECONCILIATION'):
            build_report({}, clock, 0, clock.utc(), 1, 0, {}, {}, True)
        self.assertGreater(Clock().monotonic(), 0)
        self.assertIn('+00:00', Clock().utc())
        self.assertIsNone(Events().emit('PROGRESS', 1))

class CoverageToolCalibration(unittest.TestCase):
    def test_python_file_scope_and_uncovered_negative_control(self):
        import importlib.util
        import tempfile
        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location('coverage_control', root/'codex/tools/coverage_gate.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project/'tests').mkdir()
            (project/'sample.py').write_text('value = 3\n')
            (project/'tests/test_sample.py').write_text('import unittest\nimport sample\nclass Check(unittest.TestCase):\n def test_value(self):\n  self.assertEqual(sample.value, 3)\n')
            positive = module.run_gate(project, ['sample.py'])
            self.assertEqual(positive['status'], 'PASS')
            self.assertEqual(positive['line_percent'], 100)
            self.assertEqual(positive['missing_first_party_files'], [])
            (project/'sample.py').write_text('value = 3\ndef uncovered():\n return 9\n')
            negative = module.run_gate(project, ['sample.py'])
            self.assertEqual(negative['status'], 'FAIL')
            self.assertIn(3, negative['missing_lines']['sample.py'])

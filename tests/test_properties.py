"""Post-line-gate generated checks against independent CSV/Decimal oracles."""
import csv
import gzip
import io
from decimal import Decimal, localcontext
from pathlib import Path
import random
import sys
import tempfile
import unittest
from hypothesis import given, settings, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from streaming_csv_parser.accounting import Ledger
from streaming_csv_parser.config import Limits, load_policy
from streaming_csv_parser.csv_stream import records
from streaming_csv_parser.orchestrator import run
from streaming_csv_parser.reader import physical_lines

FIX = Path(__file__).parent/'fixtures'
POLICY = load_policy(FIX/'TEST_ONLY_SCHEMA.json')
TEXT = st.text(alphabet='abcXYZ012 ,"\r\n\té€', max_size=60)


class GeneratedChecks(unittest.TestCase):
    @settings(max_examples=150, deadline=None, derandomize=True)
    @given(st.lists(st.lists(TEXT, min_size=1, max_size=12), max_size=12))
    def test_csv_differential(self, rows):
        text = io.StringIO(newline='')
        csv.writer(text, lineterminator='\r\n').writerows(rows)
        raw = text.getvalue().encode()
        expected = list(csv.reader(io.StringIO(text.getvalue(), newline=''), strict=True))
        actual = [r.fields for r in records(io.BytesIO(raw), POLICY, Limits())]
        self.assertEqual(actual, expected)

    @settings(max_examples=150, deadline=None, derandomize=True)
    @given(st.lists(st.tuples(st.integers(-10**30, 10**30), st.integers(0, 8)), max_size=50))
    def test_integer_ledger_against_decimal(self, values):
        ledger = Ledger()
        with localcontext() as ctx:
            ctx.prec = 100
            expected = Decimal(0)
            for coefficient, scale in values:
                amount = str(Decimal(coefficient).scaleb(-scale))
                # Render a plain fixed-point string, never exponent syntax.
                amount = format(Decimal(amount), 'f')
                ledger.add('SYNTHETIC', amount)
                expected += Decimal(amount)
            self.assertEqual(Decimal(ledger.strings().get('SYNTHETIC', '0')), expected)

    def test_batch_row_order_and_gzip_metamorphic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root/'input.gz'
            source.write_bytes(gzip.compress((FIX/'GOLDEN_MIXED.csv').read_bytes()))
            baseline = None
            for batch in (1, 7, 10000):
                out = root/str(batch)
                report = run(source, out, POLICY, Limits(batch_size=batch))
                comparison = (report['examined_count'], report['accepted_totals_by_currency'], (out/'validated.csv').read_bytes(), (out/'rejected.csv').read_bytes())
                if baseline is None:
                    baseline = comparison
                self.assertEqual(comparison, baseline)

    def test_feynman_resource_counterexamples(self):
        # Many individually short fields and a multiline record must hit total cap.
        for raw in (b',' * 10000 + b'\n', b'"' + b'a\n' * 10000 + b'"\n'):
            with self.assertRaises(ValueError):
                list(records(io.BytesIO(raw), POLICY, Limits(max_record_bytes=512, max_line_bytes=20000)))
        # A missing physical newline must not bypass the pre-materialization cap.
        with self.assertRaises(ValueError):
            list(physical_lines(io.BytesIO(b'x' * 100000), 512))

    def test_byte_fuzz_is_bounded_and_does_not_resynchronize(self):
        rng = random.Random(730)
        for _ in range(200):
            raw = bytes(rng.randrange(256) for _ in range(rng.randrange(1, 500)))
            try:
                result = list(records(io.BytesIO(raw), POLICY, Limits(max_record_bytes=256, max_line_bytes=256)))
            except (UnicodeError, csv.Error, ValueError):
                continue
            self.assertLessEqual(sum(len(r.raw.encode()) for r in result), len(raw))


class LedgerProtocol(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.ledger = Ledger()
        self.reference = 0

    @rule(cents=st.integers(-10**20, 10**20))
    def add(self, cents):
        sign = '-' if cents < 0 else ''
        amount = f'{sign}{abs(cents)//100}.{abs(cents)%100:02d}'
        self.ledger.add('TEST', amount)
        self.reference += cents

    @invariant()
    def exact_after_every_transition(self):
        with localcontext() as ctx:
            ctx.prec = 100
            assert Decimal(self.ledger.strings().get('TEST', '0')) * 100 == self.reference


LedgerProtocol.TestCase.settings = settings(max_examples=40, stateful_step_count=40, deadline=None, derandomize=True)
TestLedgerProtocol = LedgerProtocol.TestCase

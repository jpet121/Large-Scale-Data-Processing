"""Developer unit tests; supplied acceptance sources remain untouched."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from streaming_csv_parser.config import Limits, load_policy

FIX = Path(__file__).parent / 'fixtures'


class ConfigTests(unittest.TestCase):
    def test_valid_policy_and_limits(self):
        policy = load_policy(FIX / 'TEST_ONLY_SCHEMA.json')
        self.assertEqual(policy.allowed_currencies, ('USD', 'EUR'))
        self.assertEqual(policy.max_scale, 8)
        self.assertEqual(len(policy.identity), 64)
        self.assertEqual(Limits().batch_size, 10000)
        for value in (0, -1, True, 67108865):
            with self.assertRaises(ValueError):
                Limits(batch_size=value)

    def test_explicit_policy_rejects_invalid_configuration(self):
        base = json.loads((FIX / 'TEST_ONLY_SCHEMA.json').read_text())
        variants = [[], dict(base, schema_version=2), dict(base, columns=[]), dict(base, columns=['amount']), dict(base, columns=base['columns'] * 2), dict(base, required_fields=['invented']), dict(base, allowed_currencies=[]), dict(base, timestamp_format=''), dict(base, strict_csv=False), dict(base, doublequote='yes'), dict(base, delimiter='\n'), dict(base, quotechar=','), dict(base, encoding='utf-16')]
        for key, value in [('allow_exponent', True), ('allow_nonfinite', True), ('allow_sign', 1), ('max_digits', 0), ('max_scale', -1)]:
            d = copy.deepcopy(base)
            d['decimal_policy'][key] = value
            variants.append(d)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'policy.json'
            for data in variants:
                with self.subTest(data=data):
                    path.write_text(json.dumps(data))
                    with self.assertRaises(ValueError):
                        load_policy(path)
            path.write_bytes(b' ' * 1048577)
            with self.assertRaisesRegex(ValueError, 'POLICY_SIZE'):
                load_policy(path)

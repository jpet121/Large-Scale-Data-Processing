"""Real adapters plus explicit library ports; no framework-generated doubles."""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from streaming_csv_parser.cli import main
from streaming_csv_parser.config import Limits, load_policy
from streaming_csv_parser.orchestrator import run

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / 'tests/fixtures'


class IntegrationTests(unittest.TestCase):
    def test_library_golden_real_marker_hashes_and_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'out'
            summary = run(FIX/'GOLDEN_MIXED.csv', out, load_policy(FIX/'TEST_ONLY_SCHEMA.json'), Limits(batch_size=1))
            self.assertEqual(summary['accepted_totals_by_currency'], {'USD': '0.30', 'EUR': '8.00'})
            marker = json.loads((out/'COMMITTED.json').read_text())
            for name, metadata in marker['artifacts'].items():
                data = (out/name).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), metadata['sha256'])
                self.assertEqual(len(data), metadata['size_bytes'])
                self.assertEqual((out/name).stat().st_mode & 0o777, 0o600)
            self.assertEqual(out.stat().st_mode & 0o777, 0o700)
            self.assertEqual(summary['examined_count'], 5)
            self.assertEqual(marker['complete'], True)

    def test_header_rejection_stop_decode_and_gzip_failures(self):
        import gzip
        policy = load_policy(FIX/'TEST_ONLY_SCHEMA.json')
        data = (FIX/'GOLDEN_MIXED.csv').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = [b'', b'bad,header\n', data+b'\xff\n', b'"unclosed\n']
            for index, raw in enumerate(cases):
                source = root/f'bad{index}.csv'
                source.write_bytes(raw)
                out = root/f'out{index}'
                with self.assertRaises(Exception):
                    run(source, out, policy, Limits())
                self.assertFalse((out/'COMMITTED.json').exists())
                report = json.loads((out/'failure.json').read_text())
                self.assertFalse(report['complete'])
                self.assertEqual(report['status'], 'FAILED')
            out = root/'stop'
            with self.assertRaisesRegex(Exception, 'RECORD_ERROR_STOP'):
                run(FIX/'GOLDEN_MIXED.csv', out, policy, Limits(), on_record_error='stop')
            report = json.loads((out/'failure.json').read_text())
            self.assertEqual(report['examined_count'], report['accepted_count']+report['rejected_count'])
            source = root/'valid.gz'
            source.write_bytes(gzip.compress(data))
            self.assertEqual(run(source, root/'gz', policy, Limits())['examined_count'], 5)

    def test_cli_and_source_entrypoint(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main([]), 1)
            self.assertEqual(main(['--input', 'secret', '--output', 'out', '--schema', 'absent']), 1)
        with tempfile.TemporaryDirectory() as tmp:
            args = ['--input', str(FIX/'GOLDEN_MIXED.csv'), '--output', str(Path(tmp)/'out'), '--schema', str(FIX/'TEST_ONLY_SCHEMA.json')]
            with contextlib.redirect_stderr(io.StringIO()) as log:
                self.assertEqual(main(args), 2)
            self.assertNotIn('0012', log.getvalue())
            # Root entrypoint is exercised in-process as well as frozen subprocesses.
            entry = runpy.run_path(str(ROOT/'main.py'))
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(entry['main']([]), 1)
        with contextlib.redirect_stdout(io.StringIO()) as help_text:
            with self.assertRaises(SystemExit) as ex:
                main(['--help'])
        self.assertEqual(ex.exception.code, 0)
        self.assertIn('--max-record-bytes', help_text.getvalue())

    def test_synthetic_generator_independent_reference(self):
        spec = importlib.util.spec_from_file_location('synthetic', ROOT/'tools/generate_synthetic.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        policy = load_policy(FIX/'TEST_ONLY_SCHEMA.json')
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'generated.csv'
            expected = module.generate(source, policy, 123)
            actual = run(source, Path(tmp)/'out', policy, Limits(batch_size=7))
            self.assertEqual(actual['accepted_count'], 123)
            self.assertEqual(actual['accepted_totals_by_currency'], expected['accepted_totals_by_currency'])
            self.assertEqual(expected['accepted_totals_by_currency'], {'USD': '12.30'})
            with self.assertRaises(FileExistsError):
                module.generate(source, policy, 1)
            with self.assertRaises(ValueError):
                module.generate(Path(tmp)/'invalid.csv', policy, -1)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                module.main(['--output', str(Path(tmp)/'zero.csv'), '--schema', str(FIX/'TEST_ONLY_SCHEMA.json'), '--rows', '0'])
            self.assertEqual(json.loads(output.getvalue())['accepted_count'], 0)

class EntrypointTests(unittest.TestCase):
    def test_entrypoint_execution_rejects_unrecognized_runner_arguments(self):
        # runpy inherits unittest's real arguments; no process-global patching.
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ex:
                runpy.run_path(str(ROOT/'main.py'), run_name='__main__')
            self.assertEqual(ex.exception.code, 1)
            with self.assertRaises(SystemExit) as ex:
                runpy.run_path(str(ROOT/'tools/generate_synthetic.py'), run_name='__main__')
            self.assertEqual(ex.exception.code, 2)

    def test_gzip_generator_and_byte_budget(self):
        spec = importlib.util.spec_from_file_location('synthetic_gzip', ROOT/'tools/generate_synthetic.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        policy = load_policy(FIX/'TEST_ONLY_SCHEMA.json')
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'synthetic.csv.gz'
            module.generate(source, policy, 17)
            summary = run(source, Path(tmp)/'out', policy, Limits())
            self.assertEqual(summary['accepted_totals_by_currency'], {'USD': '1.70'})
            self.assertEqual(summary['accepted_count'], 17)
            with self.assertRaisesRegex(ValueError, 'LOGICAL_RECORD_LIMIT'):
                run(source, Path(tmp)/'capped', policy, Limits(batch_bytes=20))

class BenchmarkHarnessTests(unittest.TestCase):
    def test_kernel_measurements_success_failure_and_timeout(self):
        spec = importlib.util.spec_from_file_location('benchmark_tool', ROOT/'tools/benchmark.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = module.benchmark(FIX/'GOLDEN_MIXED.csv', root/'ok', FIX/'TEST_ONLY_SCHEMA.json')
            self.assertEqual(report['child_exit_code'], 2)
            self.assertTrue(report['complete'])
            self.assertGreater(report['peak_rss_kib'], 0)
            self.assertEqual(report['summary']['accepted_count'], 3)
            self.assertEqual(report['input_size_bytes'], (FIX/'GOLDEN_MIXED.csv').stat().st_size)
            invalid = module.benchmark(FIX/'GOLDEN_MIXED.csv', root/'ok', FIX/'TEST_ONLY_SCHEMA.json')
            self.assertEqual(invalid['child_exit_code'], 1)
            self.assertFalse(invalid['complete'])
            self.assertIsNone(invalid['summary'])
            stopped = module.benchmark(FIX/'GOLDEN_MIXED.csv', root/'stopped', FIX/'TEST_ONLY_SCHEMA.json', timeout_seconds=0)
            self.assertLess(stopped['child_exit_code'], 0)
            self.assertFalse(stopped['complete'])
            with self.assertRaisesRegex(ValueError, 'BENCHMARK_LIMIT'):
                module.benchmark(FIX/'GOLDEN_MIXED.csv', root/'bad', FIX/'TEST_ONLY_SCHEMA.json', memory_limit_mb=1)
            with contextlib.redirect_stdout(io.StringIO()) as text:
                module.main(['--input', str(FIX/'GOLDEN_MIXED.csv'), '--output', str(root/'cli'), '--schema', str(FIX/'TEST_ONLY_SCHEMA.json')])
            self.assertEqual(json.loads(text.getvalue())['summary']['examined_count'], 5)
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                runpy.run_path(str(ROOT/'tools/benchmark.py'), run_name='__main__')

class ProvenanceAndIntegrityTests(unittest.TestCase):
    def test_crc_corruption_and_wrong_headers_never_commit(self):
        import gzip
        policy = load_policy(FIX/'TEST_ONLY_SCHEMA.json')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            corrupted = bytearray(gzip.compress((FIX/'GOLDEN_MIXED.csv').read_bytes()))
            corrupted[-8] ^= 1
            source = root/'crc.gz'
            source.write_bytes(corrupted)
            with self.assertRaises(gzip.BadGzipFile):
                run(source, root/'crc-out', policy, Limits())
            self.assertFalse((root/'crc-out'/'COMMITTED.json').exists())
            for i, header in enumerate((list(reversed(policy.columns)), list(policy.columns[:-1]), list(policy.columns)+['unknown'], [policy.columns[0]]*len(policy.columns))):
                source = root/f'header{i}.csv'
                with source.open('w',newline='') as handle:
                    csv.writer(handle).writerow(header)
                out = root/f'header-out{i}'
                with self.assertRaisesRegex(Exception, 'INVALID_HEADER'):
                    run(source,out,policy,Limits())
                self.assertFalse((out/'COMMITTED.json').exists())

    def test_exact_rejected_multiline_raw_record_and_location(self):
        policy = load_policy(FIX/'TEST_ONLY_SCHEMA.json')
        fields = ['0001','sensitive-account','2026-01-01T00:00:00+0000','synthetic','not-money','USD','synthetic','line one\r\nline two']
        body = io.StringIO(newline='')
        csv.writer(body,lineterminator='\r\n').writerow(fields)
        header = io.StringIO(newline='')
        csv.writer(header,lineterminator='\r\n').writerow(policy.columns)
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'input.csv'
            source.write_bytes((header.getvalue()+body.getvalue()).encode())
            out = Path(tmp)/'out'
            report=run(source,out,policy,Limits())
            self.assertEqual(report['rejected_count'],1)
            with (out/'rejected.csv').open(newline='') as handle:
                rejected=list(csv.DictReader(handle))
            self.assertEqual(rejected[0]['raw_record'],body.getvalue())
            self.assertEqual(rejected[0]['source_record_number'],'1')
            self.assertEqual(rejected[0]['physical_line_start'],'2')
            self.assertEqual(rejected[0]['physical_line_end'],'3')
            self.assertEqual(rejected[0]['error_code'],'INVALID_AMOUNT')

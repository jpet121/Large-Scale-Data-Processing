"""Handwritten failure adapters and actual filesystem collision defenses."""
import errno
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from streaming_csv_parser.commit import Files, directory_fd
from streaming_csv_parser.config import Limits, load_policy
from streaming_csv_parser.orchestrator import run

FIX = Path(__file__).parent / 'fixtures'


class FullDiskFiles(Files):
    def create(self, name):
        raise OSError(errno.ENOSPC, 'no space')


class InterruptedWriter:
    def __init__(self, files, policy):
        raise KeyboardInterrupt()


class FailureTests(unittest.TestCase):
    def test_write_failure_never_publishes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'out'
            with self.assertRaises(OSError) as failure:
                run(FIX/'GOLDEN_MIXED.csv', out, load_policy(FIX/'TEST_ONLY_SCHEMA.json'), Limits(), files_factory=FullDiskFiles)
            self.assertEqual(failure.exception.errno, errno.ENOSPC)
            self.assertFalse((out/'COMMITTED.json').exists())

    def test_interruption_records_incomplete_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'out'
            with self.assertRaises(KeyboardInterrupt):
                run(FIX/'GOLDEN_MIXED.csv', out, load_policy(FIX/'TEST_ONLY_SCHEMA.json'), Limits(), writers_factory=InterruptedWriter)
            self.assertFalse((out/'COMMITTED.json').exists())
            self.assertFalse(json.loads((out/'failure.json').read_text())['complete'])

    def test_symlink_components_and_existing_target_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'link').symlink_to(root, target_is_directory=True)
            with self.assertRaises(OSError):
                Files(root/'link'/'out')
            with self.assertRaises(FileNotFoundError):
                directory_fd(root/'absent')
            (root/'out').mkdir()
            with self.assertRaises(FileExistsError):
                Files(root/'out')
            (root/'target').write_text('unchanged')
            files = Files(root/'private')
            try:
                (root/'private'/'validated.csv').symlink_to(root/'target')
                with self.assertRaises(FileExistsError):
                    files.create('validated.csv')
                self.assertEqual((root/'target').read_text(), 'unchanged')
            finally:
                files.close()

from streaming_csv_parser.commit import Publication


class FailedPublication(Publication):
    def __init__(self, phase):
        self.phase = phase
    def rename(self, fd):
        if self.phase == 'rename':
            raise OSError(errno.EIO, 'rename failed')
        super().rename(fd)
    def sync(self, fd):
        raise OSError(errno.EIO, 'directory sync failed')


class ChangingSource:
    def __init__(self, path):
        self.path = path
        self.source = path.open('rb')
    def __enter__(self):
        return self.source
    def __exit__(self, *exc):
        self.source.close()
        with self.path.open('ab') as handle:
            handle.write(b'changed')


class FailingEvents:
    def emit(self, code, examined):
        raise OSError(errno.EIO, 'diagnostic unavailable')


class PublicationTests(unittest.TestCase):
    def test_failed_publication_revokes_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            for phase in ('rename', 'sync'):
                out = Path(tmp)/phase
                def factory(path):
                    return Files(path, publication=FailedPublication(phase))
                with self.assertRaises(OSError):
                    run(FIX/'GOLDEN_MIXED.csv', out, load_policy(FIX/'TEST_ONLY_SCHEMA.json'), Limits(), files_factory=factory)
                self.assertFalse((out/'COMMITTED.json').exists())
                self.assertEqual(json.loads((out/'failure.json').read_text())['status'], 'FAILED')

    def test_changed_input_and_failed_diagnostics_do_not_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'input.csv'
            source.write_bytes((FIX/'GOLDEN_MIXED.csv').read_bytes())
            policy = load_policy(FIX/'TEST_ONLY_SCHEMA.json')
            with self.assertRaisesRegex(Exception, 'INPUT_CHANGED'):
                run(source, Path(tmp)/'changed', policy, Limits(), source_factory=ChangingSource)
            self.assertFalse((Path(tmp)/'changed'/'COMMITTED.json').exists())
            with self.assertRaises(OSError):
                run(FIX/'GOLDEN_MIXED.csv', Path(tmp)/'log', policy, Limits(), events=FailingEvents())
            self.assertFalse((Path(tmp)/'log'/'COMMITTED.json').exists())
            with self.assertRaisesRegex(ValueError, 'INVALID_ERROR_POLICY'):
                run(source, Path(tmp)/'invalid', policy, Limits(), on_record_error='invent')

class RealPermissionTests(unittest.TestCase):
    def test_actual_unwritable_output_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)/'readonly'
            parent.mkdir(mode=0o500)
            try:
                with self.assertRaises(PermissionError):
                    Files(parent/'out')
                self.assertFalse((parent/'out'/'COMMITTED.json').exists())
            finally:
                parent.chmod(0o700)

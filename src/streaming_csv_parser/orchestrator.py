"""Pipeline coordination; real file adapters are the defaults."""
from .errors import RunFailure


def require_header(record, policy):
    if record is None or record.fields != list(policy.columns):
        raise RunFailure('INVALID_HEADER')

from collections import Counter
from pathlib import Path
from .accounting import Ledger
from .commit import Files
from .csv_stream import records
from .reader import open_source
from .report import build_report
from .seams import Clock, Events
from .validation import validate
from .writer import Writers


def run(input_path, output, policy, limits, *, on_record_error='reject', clock=None, events=None, files_factory=Files, source_factory=open_source, writers_factory=Writers):
    clock = clock or Clock()
    events = events or Events()
    started_at, start = clock.utc(), clock.monotonic()
    if on_record_error not in ('reject', 'stop'):
        raise ValueError('INVALID_ERROR_POLICY')
    path = Path(input_path)
    stat = path.stat()
    identity = dict(input_filename=path.name, input_size_bytes=stat.st_size, input_mtime_ns=stat.st_mtime_ns, input_inode=stat.st_ino, policy_sha256=policy.identity, format_version=1)
    examined = accepted = 0
    reasons = Counter()
    ledger = Ledger()
    files = files_factory(output)
    try:
        writers = writers_factory(files, policy)
        with source_factory(path) as source:
            stream = records(source, policy, limits)
            try:
                require_header(next(stream, None), policy)
                for record in stream:
                    reason = validate(record.fields, policy)
                    # Count only after the corresponding CSV write succeeds.
                    if reason:
                        writers.reject(record, reason)
                        reasons[reason] += 1
                    else:
                        writers.accept(record)
                        row = dict(zip(policy.columns, record.fields))
                        ledger.add(row['currency'], row['amount'])
                        accepted += 1
                    examined += 1
                    if examined % limits.batch_size == 0:
                        events.emit('PROGRESS', examined)
                    if reason and on_record_error == 'stop':
                        raise RunFailure('RECORD_ERROR_STOP')
            finally:
                stream.close()
        after = path.stat()
        if (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns) != (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns):
            raise RunFailure('INPUT_CHANGED')
        summary = build_report(identity, clock, start, started_at, examined, accepted, reasons, ledger.strings(), True)
        events.emit('FINALIZING', examined)
        files.publish(summary)
        return summary
    except (Exception, KeyboardInterrupt):
        failed = build_report(identity, clock, start, started_at, examined, accepted, reasons, ledger.strings(), False)
        try:
            files.json('failure.json', failed)
            files.sync()
        except OSError:
            pass
        raise
    finally:
        files.close()

"""Unattended local CLI; no raw exception text or record data is logged."""
import argparse
import sys
from .config import Limits, load_policy
from .diagnostics import Progress
from .orchestrator import run


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError('ARGUMENTS')


def main(argv=None):
    parser = Parser(description='Stream local CSV/gzip with explicit operator schema.')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--schema', required=True)
    parser.add_argument('--batch-size', type=int, default=10000)
    parser.add_argument('--max-record-bytes', type=int, default=1048576)
    parser.add_argument('--max-line-bytes', type=int, default=1048576)
    parser.add_argument('--batch-bytes', type=int, default=8388608)
    parser.add_argument('--on-record-error', choices=('reject', 'stop'), default='reject')
    try:
        args = parser.parse_args(argv)
        policy = load_policy(args.schema)
        limits = Limits(args.batch_size, args.max_record_bytes, args.max_line_bytes, args.batch_bytes)
        summary = run(args.input, args.output, policy, limits, on_record_error=args.on_record_error, events=Progress())
        return 2 if summary['status'] == 'PARTIAL' else 0
    except (Exception, KeyboardInterrupt):
        print('FAILED: configuration, input or output error; outputs require COMMITTED.json', file=sys.stderr)
        return 1

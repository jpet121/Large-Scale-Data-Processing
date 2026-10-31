"""Deterministic artificial data, using an explicit TEST policy only."""
import argparse
import csv
import gzip
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from streaming_csv_parser.config import load_policy


def generate(output, policy, count):
    if type(count) is not int or count < 0 or policy.max_scale < 2 or policy.max_digits < 3:
        raise ValueError('GENERATOR_POLICY_OR_COUNT')
    timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc).strftime(policy.timestamp_format)
    currency = policy.allowed_currencies[0]
    opener = gzip.open if str(output).endswith('.gz') else open
    with opener(output, 'xt', newline='', encoding=policy.encoding) as handle:
        writer = csv.writer(handle, delimiter=policy.delimiter, quotechar=policy.quotechar, doublequote=policy.doublequote, lineterminator='\n')
        writer.writerow(policy.columns)
        for index in range(count):
            row = {key: f'synthetic_{index:012d}' for key in policy.columns}
            row.update(amount='0.10', currency=currency, timestamp=timestamp)
            writer.writerow([row[key] for key in policy.columns])
    cents = count * 10
    return {'synthetic_only': True, 'examined_count': count, 'accepted_count': count, 'accepted_totals_by_currency': {currency: f'{cents // 100}.{cents % 100:02d}'}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schema', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--rows', type=int, required=True)
    args = parser.parse_args(argv)
    print(json.dumps(generate(args.output, load_policy(args.schema), args.rows), sort_keys=True))


if __name__ == '__main__':
    main()

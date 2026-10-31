"""Source checkout entry point; installed users can use streaming-csv-parser."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))


def main(argv=None):
    from streaming_csv_parser.cli import main as cli_main
    return cli_main(argv)


if __name__ == '__main__':
    raise SystemExit(main())

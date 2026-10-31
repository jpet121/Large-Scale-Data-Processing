# Installation and operation

Use Python 3.12+ on Linux. No services, database, secrets or network access are needed for transaction processing. Supply an operator-reviewed JSON policy; the synthetic fixture is not approved financial policy.

An offline installation from the returned ZIP is:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --no-index --no-deps distribution/streaming_csv_parser-0.1.0-py3-none-any.whl
.venv/bin/streaming-csv-parser --input /data/input.csv.gz --output /secure/existing-parent/new-run --schema /secure/policy.json
```

For the full source verification suite, install the pinned verification wheels into a Python 3.12 or 3.13 environment:

```sh
.venv/bin/python -m pip install --no-index --find-links wheelhouse 'coverage==7.13.4' 'hypothesis==6.151.9'
.venv/bin/python codex/tools/coverage_gate.py --root . --source main.py --source src/streaming_csv_parser --source tools --tests tests --json-out evidence/coverage_first.json
```

The gate measures the whole project directory internally and aggregates only the explicit application/utility source manifest, including `main.py`. It fails for missing/uncovered files, exclusions, failed/empty tests, or banned mocking APIs. It does not assert correctness merely from execution coverage. Its regression test includes a passing Python-file scope and an intentionally uncovered negative control.

## Policy and validation

Version-1 JSON policy keys are `schema_version`, ordered `columns`, `required_fields`, `timestamp_format`, `allowed_currencies`, `decimal_policy`, `encoding`, `delimiter`, `quotechar`, `doublequote`, and `strict_csv`. The amount/currency/timestamp columns must exist. The operator supplies required business fields, permitted currencies and timestamp syntax. Decimal policy explicitly supplies `allow_sign`, `allow_exponent=false`, `allow_nonfinite=false`, `max_digits` and `max_scale`. Only fixed-point ASCII decimal syntax is supported. UTF-8, ASCII and Latin-1 are supported; other encodings fail closed. Header order must match exactly. Leading zeros, original field text, timestamps, signs and duplicate transaction rows are preserved.

Policy size is capped before loading at 1 MiB. Currencies and columns each have a 1,024-entry cap; monetary precision/scale caps are 1,000 digits. Limits protect software resources rather than asserting business policy. Row validation reports one stable primary reason per rejection.

## Run state, limits and artifacts

Output parent directories must already exist. The target must be new: it is reserved exclusively with mode 0700, and files use 0600. Symlink output components are refused. Each row is written immediately to this private attempt directory; no multirow batch is retained. `--batch-size` (default 10,000) controls progress checkpoints and is the upper record-count target; effective buffering is one record. `--batch-bytes` (default 8 MiB) independently caps a buffered logical record along with `--max-record-bytes` (default 1 MiB). `--max-line-bytes` (default 1 MiB) caps physical decompressed lines before they are fully materialized. These values must be positive and at most 64 MiB. Byte bounds apply after gzip decompression. The CSV field cap is restored after processing; the library is designed for one synchronous worker, not concurrent threaded parsing.

Exit 0 means SUCCESS, exit 2 means fully read PARTIAL with rejected rows, and exit 1 means FAILED. Help exits 0. `--on-record-error reject` continues after recoverable row errors; `stop` aborts without committing after the first rejected row. Decode errors, corrupt gzip, ambiguous CSV, record overflow, unknown headers, source changes and output errors stop the run. No guessed quote-boundary resynchronization occurs.

`validated.csv` preserves accepted logical field values. `rejected.csv` contains logical record number (first transaction is 1), inclusive physical line span, error code, and bounded exact decoded raw record. `summary.json` contains input identity and size, policy SHA-256, counts, reasons, exact per-currency totals as strings, processing timestamps, duration and row rate. Duration is sampled at summary construction; the benchmark's outer duration includes artifact finalization. `failure.json` is best-effort and explicitly incomplete.

Completion requires `COMMITTED.json`, written only after data/summary flush, fsync, reconciliation and successful file closes. It binds all three artifact sizes/hashes. Files or directories alone are not completion signals. Verify those marker hashes before downstream use. Progress goes to stderr at bounded intervals with codes/counters only. Diagnostic failure before publication aborts; publication failures revoke any marker in the running filesystem. Power-loss and faulty-storage behavior beyond tested syscall failure cases requires target-system review.

## Synthetic data and benchmarking

```sh
python3 tools/generate_synthetic.py --schema tests/fixtures/TEST_ONLY_SCHEMA.json --output /tmp/synthetic.csv.gz --rows 100000
python3 tools/benchmark.py --input /tmp/synthetic.csv.gz --output /tmp/new-benchmark-run --schema tests/fixtures/TEST_ONLY_SCHEMA.json --memory-limit-mb 128
```

Synthetic identifiers are invented, amounts are 0.10, and reference counts/totals are computed with integer arithmetic independently of parser accounting. Generator policy must support that artificial amount. It emits plain CSV or streaming gzip by suffix and refuses existing files. Gzip payloads are deterministic, though gzip archive metadata can vary between runs.

Benchmarking uses real files, SHA-256, Linux wait4 peak RSS, sampled `/proc` RSS (retaining at most the latest 4,096 samples), wall time, child exit status and an address-space cap. A process cap is not a claim that the host has that RAM. Preserve inputs or generator recipe, policy, command, evidence and output hashes. Actual measured results and unmet target conditions are in `docs/benchmarks.md`.

## Reproducing builds and formal checks

Install the other pinned verification wheels to build offline. Two wheel builds were byte-identical using:

```sh
SOURCE_DATE_EPOCH=1767225600 python3 -m build --wheel --sdist --no-isolation
```

The Lean source `tests/reconciliation.lean` was checked with official Lean 4.19.0. With that version available, run `lean tests/reconciliation.lean`. Its proof covers the abstract count equation and commit Boolean prerequisites; the Python correspondence test exhausts 31 classification sequences up to length four. It does not prove Python, gzip, filesystem durability or monetary implementation correctness. The large Lean toolchain is not bundled in the return ZIP; its source URL/version and observed digest are recorded.

Update after original implementation release: 100 GB and 150 GB physical-file workload tests succeeded in Ubuntu on WSL2 configured for approximately 8 GB RAM, and an independent reviewer checked compact receipts and reran frozen tests. See verification/ for the current audit. These results do not certify dedicated physical 8 GB Linux server hardware. Production still requires operator-approved business policy, target-host review, and explicit human release authorization.

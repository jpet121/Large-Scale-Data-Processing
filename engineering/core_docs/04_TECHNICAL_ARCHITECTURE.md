# 04 Technical Architecture — Streaming CSV Transaction Parser

## Architecture and data flow
Single-worker synchronous pipeline: `main.py` -> CLI/config validation -> bounded input byte iterator (`.csv` or gzip) -> decoding and physical-line tracker -> strict standard-library CSV tokenizer -> schema validator -> exact monetary ledger -> staged accepted/rejected writers -> summary and commit-marker publisher. A committed output directory contains `validated.csv`, `rejected.csv`, `summary.json` and `COMMITTED.json`. The marker is the only completion signal; directory/file existence alone has no approval meaning. Output writes stream as rows arrive and the writer never stores a whole result set.

## Modules, responsibility boundaries and dependency direction
`config.py` exclusively validates supplied policy; `reader.py` opens files and streams decompression; `csv_stream.py` captures bounded raw records, line spans and strict quote behavior; `validation.py` applies policy without altering original string values; `accounting.py` aggregates exact currency totals; `writer.py` handles streaming CSV; `commit.py` manages stage/flush/fsync/publish; `report.py` emits truthful status; `cli.py` maps to exit codes and sanitized messages; `orchestrator.py` coordinates these pure/injectable ports. Domain validation does not depend on filesystem or CLI libraries. No database or network service is necessary.

## Failure handling and rejected alternatives
Fatal source/stream or I/O errors cannot be converted into rejects when record boundaries are untrustworthy. A separate private staging area avoids exposing partial CSV as authorized output; a final marker is written only after checks. On a failed marker write, existing files are not approved. Reject loading pandas DataFrames, copying entire gzip to disk, unbounded ThreadPool queues, ambiguous CSV-sniffer guessing and ad hoc regex parsing; those would undermine P39/P42/P43/P64. A single worker makes ordering/recovery testable; parallelism only after measurable proof.

## Technology basis
Python 3.12 `csv.reader` supports multiline quoting with `newline=''` and a strict dialect; `gzip.open` streams and can raise `BadGzipFile`, `EOFError` or zlib errors; `Decimal` requires explicit precision review to avoid silent context rounding. External documentation is corroboration, not higher authority: https://docs.python.org/3.12/library/csv.html and https://docs.python.org/3.12/library/gzip.html. Source authority: P23, P42, P64, P80, P84, P107, P149 and T_DESIGN/T_STREAM/T_WRITE.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

## Adversarial resource-boundary and early-gate note
The 10,000-row default is a record-count target, **not** permission to buffer 10,000 maximum-sized records. Implement independent configurable batch-byte/whole-logical-record/physical-line limits, enforce them on fixed-size decompressed byte chunks *before* materializing a huge line, and reject premature statements of 100% coverage while any frozen end-to-end tests remain failing. Do not skip, rewrite or narrow acceptance tests to obtain a passing report. Continue source work, report failed intermediate gates, and execute extended assurance only after a genuine full-source line-coverage PASS.

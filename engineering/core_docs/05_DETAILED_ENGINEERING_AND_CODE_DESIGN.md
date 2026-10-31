# 05 Detailed Engineering And Code Design — Streaming CSV Transaction Parser

## Proposed repository and type contracts
`main.py` is a real entrypoint on the root; `src/streaming_csv_parser/{config,models,seams,reader,csv_stream,validation,accounting,errors,writer,commit,report,orchestrator,cli,diagnostics}.py`; `tools/generate_synthetic.py`, `tools/benchmark.py`; `tests/` contains immutable acceptance tests and future developer-authored unit/integration tests; `docs/` covers recovery and measurements. Use dataclasses/frozen config and explicit protocols for ByteSource, FileSystem, Clock, EventSink and StreamingCsvWriter. Use a `ValidatedRow` carrying the original source string fields, `RejectedRow` with reason/line span/raw bounded record and `Ledger` with exact totals.

## Bounded streaming algorithm
Validate policy and output target before touching inputs; open binary or gzip bytes, limit decompressed physical line, logical record bytes and number of columns before a huge field or cumulative small fields consumes memory. Decode with explicitly configured encoding and strict errors. Use a strict CSV lexer over a bounded physical-line iterator, retain only the current logical record/raw capture and a finite batch. If quote/encoding/size state becomes unreliable, stop file-level processing; if the record is well-formed with invalid business fields, stream it to the reject sink. After each classified logical record, increment examined then accepted/rejected, write immediately or flush finite batch and release references.

## Exact money and integrity
Parse amount from original text without float; reject NaN/Infinity and unsupported syntax. To avoid Decimal default-precision rounding on a large total, use an exact coefficient-and-decimal-exponent integer accumulator per currency, or trap all Inexact/Rounded operations with sufficient proven precision and set a documented cap. Convert back to decimal strings with no fabricated quantization. Preserve leading zero identifiers and input timestamp text. No implicit deduplication. A footer/trailer gzip error is fatal even when all logical records appear parsed.

## State, seams and completion
Writer abstraction supports real Linux file operations plus concrete in-memory and deliberately failing-writer implementations. Under failures, flush diagnostics best-effort, ensure commit marker absent, never claim a complete summary. Rerun policy refuses an existing committed output path unless explicit distinct target selected; never append. All code increments run frozen acceptance and meaningful new unit tests, then `codex/tools/coverage_gate.py` with every first-party source root; branch report reviewed. No `unittest.mock`/patch or pytest monkeypatch.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

## Adversarial resource-boundary and early-gate note
The 10,000-row default is a record-count target, **not** permission to buffer 10,000 maximum-sized records. Implement independent configurable batch-byte/whole-logical-record/physical-line limits, enforce them on fixed-size decompressed byte chunks *before* materializing a huge line, and reject premature statements of 100% coverage while any frozen end-to-end tests remain failing. Do not skip, rewrite or narrow acceptance tests to obtain a passing report. Continue source work, report failed intermediate gates, and execute extended assurance only after a genuine full-source line-coverage PASS.

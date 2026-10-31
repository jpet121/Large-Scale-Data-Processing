# 11 Codex Master Implementation Instructions — Streaming CSV Transaction Parser

## Binding instructions to Codex
Read the immutable XML and requirement index first, then the engineered contract and ALL 22 documents. Implement the selected architecture without changing source XML, protected acceptance tests, pre-Codex gate result or the packaged coverage enforcement tool. Write production Python 3.12+ with root `main.py`, modular `src/streaming_csv_parser`, deterministic synthetic generator and executable benchmark apparatus. Schema/allowlist/timestamp rules must be explicit operator inputs; the test-only schema does not authorize production use.

## Dependency-ordered build and safe seams
Execute TASK-01 through TASK-12 using `codex/CODEX_TASKS.json` prerequisites. T01 config and typed seams; T02 bounded CSV/gzip reader; T03 exact validator/ledger; T04 record-versus-fatal errors; T05 staged writers; T06 reconciliation; T07 CLI/logging; T08 generator; T09 meaningful tests; T10 advanced checks after early line gate; T11 100/150GB target-host benchmarks; T12 docs and exact archive recheck. Add `unittest` tests continuously and inject concrete clock, source, event or writer objects at deliberate ports. Never use unittest.mock, Mock, MagicMock, patch, monkeypatch or equivalent patch libraries.

## Coverage-first per code increment
Run `python codex/tools/coverage_gate.py --root . --source main.py --source src/streaming_csv_parser --source tools/generate_synthetic.py --source tools/benchmark.py --tests tests --json-out evidence/coverage_first.json` once files exist; if the tool's source-root API requires directories, pass the actual full first-party package/file scope in a format it supports and document coverage of ALL files. The gate must report 100% executed first-party lines, a nonempty meaningful unit suite, and branch coverage for manual review. No silent exclusions, pragma no cover or fake tests. Increments cannot advance to advanced assurance before real PASS. A unit test that asserts only that a function returns is insufficient if it fails to challenge the contract.

## Completion, blockers and return
Run frozen black-box scenarios, fault injection, counterexamples, independence checks, target-host benchmarks and clean installs. For a missing required production policy, implement explicit config rather than invent values; if owner business semantics cannot be delegated, stop that decision specifically. For inaccessible 8 GB benchmark hardware, do not certify production acceptance. Return one source/receipt/evidence ZIP; include actual hashes and logs; preserve human release approval NOT_GRANTED. No third-party deployment or upload of financial data.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

## Adversarial resource-boundary and early-gate note
The 10,000-row default is a record-count target, **not** permission to buffer 10,000 maximum-sized records. Implement independent configurable batch-byte/whole-logical-record/physical-line limits, enforce them on fixed-size decompressed byte chunks *before* materializing a huge line, and reject premature statements of 100% coverage while any frozen end-to-end tests remain failing. Do not skip, rewrite or narrow acceptance tests to obtain a passing report. Continue source work, report failed intermediate gates, and execute extended assurance only after a genuine full-source line-coverage PASS.

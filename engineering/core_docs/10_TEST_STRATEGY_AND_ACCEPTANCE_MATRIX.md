# 10 Test Strategy And Acceptance Matrix — Streaming CSV Transaction Parser

## Verification sequencing and hard gates
Before CodeX: freeze independent source-derived acceptance cases, verify fixture self-check and audited documents. During EACH Python implementation increment: run meaningful `unittest` with explicit injected concrete seams and `codex/tools/coverage_gate.py` over the entire executable first-party source scope (`main.py`, `src/streaming_csv_parser`, `tools/generate_synthetic.py` and `tools/benchmark.py` once created). The gate requires 100% executable line coverage and actual nonempty passing unit tests. Review branch coverage without mandating universally 100%. No `unittest.mock`, `patch`, `MagicMock`, `monkeypatch`, or equivalent dynamic mock framework. Altering code invalidates former coverage evidence.

## Frozen acceptance plan
The 27 cases A01–A27 in analysis/ENGINEERING_REVIEW.json are authoritative requirements-to-observation mappings. Runnable prewritten tests: `tests/test_acceptance_contract.py` covers five-row golden, gzip and header-only; `tests/test_fatal_and_replay.py` covers corrupted gzip, broken quoting, empty, invalid batch, oversized and repeat. `tests/test_oracle_selfcheck.py` calibrates goldens independently and is the only target-free runnable test now. `tests/fixtures/GOLDEN_MIXED.csv` uses quotes, comma and multiline; golden totals USD=0.30, EUR=8.00 and 5=3+2. These fixtures are not derived from candidate code.

## Future advanced stage
After early coverage PASS: Hypothesis data/stateful generators, CSV versus trusted csv.reader differential checks, independent decimal accounting, mutations dropping rows or bypassing commit, Feynman counterexample hunts, injected I/O faults, Lean reconciliation model/correspondence if feasible, adversarial gzip and size fuzz, compatibility, clean wheel and security verification. LIGO-style injected known positives/negatives are a methodology analogy only, not a detector certification. The 21-discipline register records each as READY_NOT_EXECUTED until run.

## Large-file pass/fail evidence
Measurements must include actual input size, RSS peak, resource samples over time, row rate, elapsed time, host RAM, Python version, digest and exception logs. Passing 100 GB+ on 8 GB is mandatory, as is credible support at >=150 GB; preferred <512MB is reported independently. A missing real environment or insufficient disk is recorded as unverified and blocks production acceptance, not a green pass. Final independent exact-returned-ZIP replay and human approval are separate gates.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

## Adversarial resource-boundary and early-gate note
The 10,000-row default is a record-count target, **not** permission to buffer 10,000 maximum-sized records. Implement independent configurable batch-byte/whole-logical-record/physical-line limits, enforce them on fixed-size decompressed byte chunks *before* materializing a huge line, and reject premature statements of 100% coverage while any frozen end-to-end tests remain failing. Do not skip, rewrite or narrow acceptance tests to obtain a passing report. Continue source work, report failed intermediate gates, and execute extended assurance only after a genuine full-source line-coverage PASS.

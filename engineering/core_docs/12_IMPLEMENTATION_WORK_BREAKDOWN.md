# 12 Implementation Work Breakdown — Streaming CSV Transaction Parser

## Dependency graph and phases
The source XML explicitly orders design -> stream/parse -> errors -> writer -> summary and makes tests dependent on CLI/writer/error/integrity, benchmarks dependent on the synthetic generator and final acceptance dependent on tests, benchmarks and docs. Follow the more granular machine-readable TASK-01 through TASK-12 graph; its `depends_on` is acyclic and `done_when` references exact acceptance IDs. Do not implement broad test-only shortcuts that bypass real integration semantics.

## Foundations, domain and interfaces
TASK-01 establishes Python 3.12 packaging, policy schema and dependency ports; verifies A02/A19/A21/A24. TASK-02 creates strict bounded gzip/plain CSV streaming with line spans and resource limits (A01/A03/A07/A14). TASK-03 validates field types and computes exact multi-currency sums; preserves original source strings and checks header structure (A02/A04/A25/A23). TASK-04 establishes fatal versus recoverable record semantics and provenance; tests broken quoting and reason codes (A05/A06/A26).

## Implementation, integration and verification
TASK-05 builds staged writers plus commit barrier (A09/A10/A11/A16); TASK-06 generates exact JSON and complete/failed state (A15/A27); TASK-07 adds CLI and confidential progress (A12/A13/A20). TASK-08 makes synthetic deterministic generator (A17). TASK-09 runs meaningful unit and real integration suites without any mock/patch library (A18/A22/A21). Every code increment reruns first-party 100% line gate; no later stage may inherit stale evidence.

## Assurance, packaging and delivery
TASK-10 executes applicable Feynman, Hypothesis, differential, faults, mutation, Lean correspondence and security checks ONLY after valid early coverage (A22/A04/A08). TASK-11 measures actual progressive and target 100/150 GB 8 GB Linux runs (A01/A18). TASK-12 seals packages, operating manuals and the exact-hash independent return audit (A19/A22). Report blocked physical-resource evidence, not estimated throughput; no release without human approval.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

## Adversarial resource-boundary and early-gate note
The 10,000-row default is a record-count target, **not** permission to buffer 10,000 maximum-sized records. Implement independent configurable batch-byte/whole-logical-record/physical-line limits, enforce them on fixed-size decompressed byte chunks *before* materializing a huge line, and reject premature statements of 100% coverage while any frozen end-to-end tests remain failing. Do not skip, rewrite or narrow acceptance tests to obtain a passing report. Continue source work, report failed intermediate gates, and execute extended assurance only after a genuine full-source line-coverage PASS.

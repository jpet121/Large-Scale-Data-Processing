# Method Selection Record — Streaming CSV Transaction Parser

## Characteristics
Requirements are extensive and compiled to 77 binding propositions; no material existing-code baseline was attached. High cost of late changes to financial records, low tolerance for partial success, untrusted source files, no network dependency, measurable outputs, high testability with bounded I/O seams. Novelty mainly in failure semantics under enormous files, not in CSV parsing itself.

## Selected lifecycle
BUILD/HIGH_ASSURANCE with a requirements-driven, incremental test/coverage gate and subsequent adversarial assurance. Design explicit schema policy and commit protocol first, then implement the smallest auditable stage. Freeze black-box oracles before Codex. Use `unittest` + `coverage.py` early, no framework patching/mocking; require 100% first-party executable line coverage at each increment and review branch coverage without a 100% branch threshold. After the line gate, run application-relevant fuzz/mutation/injected failures and independent exact-artifact rerun.

## Reconsider criteria
Revisit architecture when measured 8 GB host RSS grows with record count, at 100/150GB file sizes or when adding parallelism risks writer atomicity. Never change source data semantics to hit throughput. Missing physical benchmark evidence blocks production claims, not the preparation of a CodeX handoff. Source P175/P198 and PEHAVOS 1.2 policy.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

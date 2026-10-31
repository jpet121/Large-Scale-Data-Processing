# 13 Build Packaging Deployment Release — Streaming CSV Transaction Parser

## Environment and build
Support Python 3.12+ and an 8 GB Linux server, preferably with filesystem space sufficient for the largest input, staging outputs, diagnostics and replays. Package as a usable Python source/wheel with a real root `main.py`; use only justified runtime dependencies. `unittest` is routine baseline and `coverage.py` is mandatory early verification tooling. Record exact interpreter and dependency versions in a lock/evidence report. No network required by product processing.

## Distribution and reproducibility
Codex must return package with implementation source, `pyproject.toml`, synthetic generator, benchmark tools, documents, frozen tests, SHA-256 manifest, actual coverage and advanced evidence, `IMPLEMENTATION_RECEIPT.json`. Fresh extraction on an isolated verifier must rehash immutable source and fixtures and recreate required dependencies offline when feasible. Build a wheel and run the CLI from the installed package using non-sensitive test files. Do not ship production financial data in the release.

## Release safety and rollback
A completed output run requires a verified final COMMITTED marker, not just files. An interrupted run stays in staging and is quarantined until operator recovery; reruns must not append to committed output. Output-format or schema changes require policy/version changes and replay tests. Production release criteria: every required clause traced, 100% covered first-party executable lines with evidence, applicable external verification complete, test oracle positive/negative controls, 100 GB+/8GB real benchmark, support >=150GB, integrity review, security/signoff and explicit human acceptance. Prefer peak <512MB but disclose not meeting preference separately.

## Current status
This deliverable is solely a source-frozen pre-Codex handoff. Implementation binaries, deployed application, 100/150GB measurements and genuine production release approval do not exist here. Source P183–P190, P194–P198 and PEHAVOS v1.2 coverage policy.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

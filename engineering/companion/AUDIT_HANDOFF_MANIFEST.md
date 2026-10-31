# Audit Handoff Manifest — Streaming CSV Transaction Parser

## Identity and authority
Original application XML is in `source/contract.xml` with SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e. `source/EXTRACTED_CONTRACT.json`, `source/REQUIREMENT_INDEX.json` and `source/JOB_IDENTITY.json` identify the same exact input. No matching compiler receipt exists; this is explicitly NOT a receipt-certified COMPILE_RELEASED claim. The OS v1.2 policy and tools are used without changing the universal Compiler/Runner.

## Evidence inventory for handoff auditor
`analysis/ENGINEERING_REVIEW.json` holds 77 source-to-requirement entries, 27 acceptance cases, 12 Codex task dependencies and all 21 planned disciplines. `documents/core_docs/` has 15 authored documents and `documents/companion/` has seven. `tests/test_oracle_selfcheck.py` and immutable fixture inputs form a target-free oracle calibration. Frozen black-box tests are in `tests/test_acceptance_contract.py` and `tests/test_fatal_and_replay.py`. All hashes must be recorded in `analysis/AUDITOR_REVIEW.json` after review of exact saved bytes.

## Limitations and audit boundaries
The Challenger pass is a separate role in this same ChatGPT host, not an institutionally independent second auditor. Handoff structural verification is machine executable; semantic claims remain human/design responsibilities. No target Python app, 100/150 GB benchmark, live currency policy, external credentials or owner release approval exists. Audit must reject document stubs, trace gaps, forged coverage or a claim that application tests passed before Codex.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

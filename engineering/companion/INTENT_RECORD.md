# Intent Record — Streaming CSV Transaction Parser

## Raw intent and users
Owner wants reliable Python 3.12+ streaming CSV/gzip financial processing on existing 8 GB Linux servers, up to and beyond 150 GB, with strict financial preservation, accepted/rejected CSV, JSON reconciliation, unattended command-line use, error safety and real benchmark evidence. Operations runs jobs; finance/reconciliation audits totals; developers maintain code and tests. P9–P23 and P194–P198 establish need and outcome.

## Authority and non-goals
The compiled contract is immutable, as is the requirement index. Source explicitly prohibits loading whole files, changing transaction values, silent loss, unnecessary PII exposure, external financial uploads and apparent success after interrupted runs. Under 512 MB is preferred, not the hard budget; 8 GB is operating host. No automatic cloud deployment, customer-data generator or additional server purchase. Human release approval is reserved.

## Missing business semantics
Gateway-specific mandatory fields, currency allowlist, timestamps and amount scales are not decided by the source. Use explicit runtime schema with a separate test-only fixture, not invented production defaults. Positive and negative test oracles come from exactly stated source obligations and disclosed design choices. Preparatory handoff proceeds without claiming live schema is approved.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

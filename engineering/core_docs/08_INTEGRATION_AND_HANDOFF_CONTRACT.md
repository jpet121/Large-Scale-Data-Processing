# 08 Integration And Handoff Contract — Streaming CSV Transaction Parser

## Producer and consumer contract
Upstream partners provide local CSV/gzip bytes and an operator-approved schema. The streaming parser must not infer gateway-specific currencies, timestamp formats or collation from the data. Downstream reconciliation accepts only output directories with a valid `COMMITTED.json` marker whose file sizes/checksums match the accepted/rejected CSV and summary. Downstream must not treat a discovered `validated.csv` as final. The marker separates prepared data from operational authority and protects the P84 false-success prohibition.

## Source boundary and traceability
The immutable compiled XML binds all required/prohibited requirements. `source/REQUIREMENT_INDEX.json` indexes clause IDs; `analysis/ENGINEERING_REVIEW.json` conserves all 77 into requirements and acceptance; `codex/CODEX_TASKS.json` gives dependency order. Codex may add implementation files and executed evidence but may not modify XML, compiled index, frozen tests or handoff status fields. Missing compiler receipt is declared; do not relabel the XML as receipt-certified.

## Versioning and replay
An operator-provided policy must identify version/allowed columns, not guessed business semantics. Each run binds input identity, byte size and policy identity in committed metadata. A repeat of an already committed output directory returns failure without append; rerun to a distinct path to avoid accidental duplicates. Changes to output formats require a format-version bump and compatibility tests; no automatic migration of potentially financial records.

## Failure and return boundary
The returned Codex ZIP must contain actual source, a meaningful `IMPLEMENTATION_RECEIPT.json`, frozen accepted tests unchanged, coverage evidence and attributable results for applicable advanced checks, plus objective memory/throughput measurements. Independent verifier must re-execute on exact final bytes when authorized, not trust developer self-assertion. Human deployment/release approval remains NOT_GRANTED. Source P66/P84/P139/P153/P157 and PEHAVOS v1.2 policy.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

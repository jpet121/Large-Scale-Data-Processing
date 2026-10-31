# 03 Domain Language Behavior Spec — Streaming CSV Transaction Parser

## Normative domain language
A **physical line** is a line read from the underlying decompressed byte stream; a **logical CSV record** may span multiple physical lines. **Examined** counts complete identifiable logical transaction records, not headers, unread data or speculative portions of corrupt CSV. **Accepted** is a complete record satisfying the explicit operator policy; **rejected** is a complete record with recoverable boundaries that violates that policy. **Fatal** means file-wide reliable parsing or required storage integrity is impossible. Design definitions refine P74–P84 and P149 without inventing transaction business values.

## Record and schema behavior
The XML says transaction ID, account ID, timestamp, type, amount, currency, status and processor reference are generally present, not that all are universally required (P49–P56 informational). A versioned schema supplied at runtime defines column order/header, required fields, allowed currencies, timestamp format, monetary syntax/scale, accepted record types if any, and encoding. No live default ISO precision, currency or validity list is assumed. Test fixtures explicitly declare a local eight-field policy, USD/EUR and a timestamp format for independently checked golden cases. Preserve all original logical values; do not trim identifiers, guess missing timestamps or de-duplicate same input transaction ID.

## Lifecycle and ordering
NEW -> CONFIG_VALIDATED -> STAGING -> STREAMING -> FINALIZING -> COMMITTED (either SUCCESS or PARTIAL when full file has rejects). At any unrecoverable parse, gzip, output, size or policy error: STAGING/STREAMING -> FAILED, complete=false; no COMMITTED marker. PARTIAL here is a fully read file with rejected rows, not a torn write; this is a documented technical status design because P137 demands distinct outcomes without prescribing codes. A termination that prevents finalization is FAILED/incomplete even if some rows were already counted.

## Invariants and negative examples
For complete files: examined=accepted+rejected; accepted values preserve each source row's fields; totals use exact arithmetic; no persisted half-result becomes authoritative. Unmatched quote cannot be reliably resynchronized and is fatal; a valid CSV record with bad amount is rejectable with provenance. Empty byte input lacks header => failure; correct header-only file => complete zero-row success. Source P64, P66, P76, P78, P80, P84, P149; acceptance A02–A08, A15 and A27.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

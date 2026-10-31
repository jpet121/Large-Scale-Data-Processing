# 09 Security Reliability Privacy Safety Performance — Streaming CSV Transaction Parser

## Threat and hazard model
High-consequence hazards are financial amount corruption, silently discarded/duplicated transactions, false completed status, gzip bombs/overlength rows exhausting memory, malformed quoting that merges records, unsanitized diagnostic exposure, and malicious filesystem paths. Inputs are untrusted partner files; policy is privileged operator data. Build on Python 3.12 stdlib CSV/gzip; fail closed on decode or gzip CRC/trailer errors. No network transmission or remote diagnostic service is allowed. Protect output files by restrictive permissions and avoid following symlinks in output paths.

## Financial correctness
Do not convert amounts through floats. Decimal is exact at construction, but decimal context precision can round arithmetic; enforce no rounding with an integer coefficient/exponent ledger or proven high-precision traps. Compare against independent `Decimal` reference fixture. No implicit currency conversion, timezone rewriting, duplicate ID removal or field trimming; validation policy decides allowable syntax. Preserve original raw rejected data only in locally permissioned rejected CSV, never logs.

## Resource and failure safety
Enforce a maximum total logical record bytes as well as per-field cap; count bytes after gzip decompression and across multiline records. A finite default batch of 10,000 is not itself an RSS proof; dynamic row-size variation must be tested. Target host 8 GB RAM, preferred peak process under 512 MB on ordinary workloads. Measure RSS with a real Linux 8 GB process and cases 100 GB and >=150 GB. Extra-large record or corrupted gzip errors stop without a committed marker. Simulated ENOSPC and interruption demonstrate failure integrity. Do not claim fsync is successful until errors have been observed/handled.

## Privacy and CSV formula risk
Store sensitive data locally only, with clear operator access and retention expectations. Warn downstream spreadsheet consumers that formulas embedded in untrusted raw fields could be interpreted as commands; do not silently mutate source text with spreadsheet-specific prefixing because P66/P145 prohibit value changes. Compliance certifications such as PCI DSS are not claimed without actual scope/policy/evidence. Source P39/P43/P62/P66/P80/P84/P145/P147/P151/P153/P175.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

## Adversarial resource-boundary and early-gate note
The 10,000-row default is a record-count target, **not** permission to buffer 10,000 maximum-sized records. Implement independent configurable batch-byte/whole-logical-record/physical-line limits, enforce them on fixed-size decompressed byte chunks *before* materializing a huge line, and reject premature statements of 100% coverage while any frozen end-to-end tests remain failing. Do not skip, rewrite or narrow acceptance tests to obtain a passing report. Continue source work, report failed intermediate gates, and execute extended assurance only after a genuine full-source line-coverage PASS.

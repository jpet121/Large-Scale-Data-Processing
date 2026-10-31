# Failure Class Record — Streaming CSV Transaction Parser

## Failure classes and earliest detection
F1: whole-file collection -> rising RSS/OOM on large file; detect via source review and progressive peak RSS measurement, remedy iterator/bounded buffers. F2: malformed quote or corrupted gzip -> undefined logical record boundary; detect strict CSV/gzip decode and negative fixtures, remedy file-level FAILED without guessed recovery. F3: overflow/Decimal rounding -> financial totals mismatch; detect independent decimal oracle plus mutations, remedy exact integer coefficient/exponent or trapped Decimal arithmetic. F4: disk full/forced termination -> staged partial files misread as complete; detect injected I/O faults/termination and marker check, remedy commit barrier and no authoritative status without marker.

## Additional classes
F5: unexpected header/unsupported currency -> hidden reinterpretation; detect explicit schema validation and reject/abort policy. F6: logged identifiers/amount -> privacy breach; detect sentinel strings in stdout/stderr and security review. F7: rerun append -> duplicate totals; detect repeat golden fixture and collision policy. F8: oversized multiline record -> memory explosion; detect maximum whole-record byte tests, including many small fields. All are currently *anticipated* classes, not observed failures in a built target app.

## Regression and evidence
A05/A06/A07/A09/A10/A11/A14/A15/A23/A25/A27 are essential adversarial regressions. Actual failure injection, mutation and benchmark results remain unexecuted; no high-assurance application claim can be made from this preparatory record.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

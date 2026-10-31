# Expert Council Record — Streaming CSV Transaction Parser

## Disciplines selected and decisions
| Perspective | Material check | Authority |
|---|---|---|
| Financial reconciliation expert | Decimal precision, same input record counted once, exact per-currency totals | Advises; does not invent bank business policy |
| Python I/O engineer | Strict CSV/gzip, multiline, bounded buffers and UTF-8 decoder | Engineering choice under XML |
| Linux reliability engineer | fsync, atomic marker, ENOSPC, kill/retry behavior and filesystem permissions | Engineering choice; owner release reserved |
| Test/oracle specialist | Frozen golden, reject-all counterexample, mutation and differential checks | Independent verification role |
| Security/privacy reviewer | No external transmission, no PII console logs, local file safety | Review and veto critical defects |
| Operations scheduler | Exit/status contract, diagnostics, run identity and repetition | Acceptance owner for scheduler integration |

## Conflicts and resolution
Speed versus correctness: prioritize correctness (P143). Partial with rejects versus torn run: distinguish complete PARTIAL (exit 2) from FAILED incomplete (exit 1); published only when full input reliably parsed. Currency policy not specified: leave runtime schema caller-owned; fixture USD/EUR is testing only. No expert can grant financial schema authority or production release. Escalation only for changes that require new human business semantics, credentials or deployment permissions.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

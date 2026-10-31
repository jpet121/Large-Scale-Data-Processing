# 06 Input Output Artifact Contracts — Streaming CSV Transaction Parser

## Accepted inputs and policy document
Required CLI input: a local readable `.csv` or `.csv.gz` path, output directory not equal to an input path, and explicit versioned JSON schema policy. Policy declares exact expected header/column order, required fields, permitted currencies, timestamp format, amount syntax/limits, encoding, CSV delimiter/quoting, and record limits. `tests/fixtures/TEST_ONLY_SCHEMA.json` is only a test fixture. No default business policy is inferred from common transactions. A validation failure in config occurs before output creation.

## Committed outputs
`validated.csv`: schema header and one row per accepted complete logical transaction, values logically equal to original fields. `rejected.csv`: `source_record_number,physical_line_start,physical_line_end,error_code,raw_record` (plus optional safely encoded details) with raw source record when bounded and recoverable. `summary.json`: `input_filename,input_size_bytes,started_at_utc,completed_at_utc,examined_count,accepted_count,rejected_count,rejection_counts_by_type,accepted_totals_by_currency,duration_seconds,throughput_records_per_second,status,complete`. Counts use integers; amounts use strings representing exact decimals; no binary float amounts. `COMMITTED.json`: final record referring to the other three files, recording sizes/hashes and `complete=true`. These filenames and keys are explicit implementation interface choices, not source-mandated spellings.

## Integrity and atomicity
Files are written to a private attempt/staging namespace with no public successful status, then flushed, fsynced, reconciled and moved to target, with a commit marker created last and fsynced. Do not claim a single atomic rename covers four files; interruption after one promotion leaves uncommitted files, which consumers must ignore. Verify marker-linked hashes. Empty CSV without header fails; header-only succeeds with empty outputs. A fully read rejected-record input has status PARTIAL (with complete=true), whereas a failed/incomplete parse has status FAILED (complete=false) and no marker. Reruns never append to existing results.

## Golden artifact
For the explicitly configured five-record golden fixture: 5 examined, 3 accepted, 2 rejected; exact USD total `0.30`, EUR total `8.00`; input ID `0001` stays `0001`, a quoted embedded line break stays inside one transaction. This is an independent test policy and expected value, not an operator's actual transaction mandate. Source P90–P105/P139/P145/P149; A04/A05/A15/A16.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

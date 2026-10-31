# 14 Developer And Operations Guide — Streaming CSV Transaction Parser

## Installation and first run (future application)
Use a verified Python 3.12+ Linux installation and install the returned package into a clean virtual environment. Prepare an operator-reviewed schema JSON separate from test fixtures, check input readability and target output free space, and create private output directories. Illustrative command: `python main.py --input /data/bank.csv.gz --output /secure/out/run-a --schema /secure/policies/bank_v1.json --batch-size 10000`. Run `--help` after implementation; a source-handoff cannot promise currently runnable application behavior.

## Operations and reconciliation
Observe bounded progress counters and exit code. Under design policy exit 0 SUCCESS, exit 2 PARTIAL when entire input is read but some rows were rejected, exit 1 FAILED on incomplete parsing/storage. Read outputs only if COMMITTED marker validates hashes. Reconcile summary examined = accepted+rejected; inspect accepted totals by currency using independent accounting, not floats. Do not open untrusted raw CSV directly in spreadsheet applications that can interpret formula-like strings.

## Troubleshooting and recovery
Malformed quoting, invalid gzip trailer, unknown source header, invalid JSON policy, record-size exceed, EIO/ENOSPC, or permission collision result in failure and no completed marker. Preserve diagnostic counts and source identity from best-effort summary; do not call it complete. Recover by fixing upstream file, policy or disk conditions, then rerun with a distinct output path. Never append to a previous committed directory. Inspect stderr only for sanitized counters, not raw PII. Rerun the exact frozen fixture before making schema changes.

## Maintenance and limitations
Measure RSS periodically in long streaming runs; document actual throughput and limits at 100 and 150 GB once tested. Record security permissions, Python upgrade regressions, schema revisions, clean install results and every new tricky CSV delimiter pattern. No service, upstream integration or policy inference is implied by this project. P127–P139/P145/P151/P153/P190 supply operating obligations.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

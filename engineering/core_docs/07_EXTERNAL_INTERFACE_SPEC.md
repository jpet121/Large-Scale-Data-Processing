# 07 External Interface Spec — Streaming CSV Transaction Parser

## Command-line interface
The proposed implementation accepts `python main.py --input ./transactions.csv --output ./results --schema ./approved_policy.json --batch-size 10000 --max-record-bytes 1048576 --on-record-error reject`. Input path, output path and schema are required. Batch/record caps are validated positive integers; defaults are implementation size-management choices and recorded in `--help`. An operator may set gzip input based on extension/magic validation, but never silently decompress it fully or reinterpret a corrupt file as uncompressed CSV. No remote endpoints, web UI or network access.

## Scheduler and status interface
Exit 0 = SUCCESS, all input logical records read with no rejected rows and complete committed outputs. Exit 2 = PARTIAL, all input records read, some invalid rows rejected, complete committed outputs. Exit 1 = FAILED, parse/config/storage/interruption prevents reliable successful completion, no authoritative commit marker. These numeric codes are a design selected to fulfill P137's requirement for distinguishable outcomes, not a specified source value. `summary.json.status` and `complete` must agree with marker and process return. Invalid CLI invocation returns nonzero failure and avoids output mutation.

## Logs and limits
Emit bounded progress to stderr at a configurable interval with input bytes/known records, elapsed time and non-sensitive counters. Never print raw account, transaction ID, amount, original rejected payload or a row dump to console. Diagnostics may include error code and location only. Output paths and schema must be validated for dangerous links/aliases and ownership; local permissions enforce access. No request/credential tokens exist. Rejection records, not stdout, preserve sensitive original data under controlled files.

## Examples and compatibility
Unattended task: `python main.py --input /data/input/2026-10-30.csv.gz --output /secure/output/run-2026-10-30 --schema /secure/policies/gateway_a_v1.json`. This command is illustrative; no asserted production policy exists. Batch choices 1, 7 and 10000 must preserve equivalent outcomes. Python 3.12+ Linux compatibility is required. Source P127/P131/P133/P135/P137; A12/A13/A24.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

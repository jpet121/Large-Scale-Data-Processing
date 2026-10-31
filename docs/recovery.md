# Recovery and handling

Consume a result only if `COMMITTED.json` is complete and all three referenced files match its SHA-256 and byte size. Directory or CSV existence is insufficient. Keep incomplete attempts quarantined with access restricted to operators.

On failure, inspect sanitized stderr and `failure.json` if available. Counts describe successfully classified/written records, not unread input. A killed process may have no failure report. Preserve the input, policy and failed attempt; fix source, policy, permissions or disk capacity and rerun into a new target. Do not append, merge, truncate financial records, automatically resume or resynchronize broken quoting. Reprocessing does not deduplicate transaction IDs.

Outputs are streamed into a private, exclusively created attempt directory. There is no in-place overwrite mode. A repeated target fails before any append. Artifact files and pending markers can survive a crash; absence of a valid final marker always means non-authoritative data. File and directory fsync are requested, but storage controllers, power loss and target filesystem semantics still need operational review. A failed syscall after publication triggers marker removal; persistent storage failure can prevent durable cleanup. Do not infer storage certification from unit coverage.

CSV fields remain untrusted text. Spreadsheet programs can execute formula-like values. The parser preserves values and does not add protective prefixes; control downstream viewing. No financial data or metrics are uploaded. Production schema policies must be reviewed separately from the synthetic fixture.

Observed failure tests cover invalid CSV/gzip, limits, decode/header errors, output collisions, symlinks, actual unwritable parent directories, injected ENOSPC/EIO, publication failure, input changes, telemetry failure, KeyboardInterrupt, real SIGTERM and replay. They do not exhaust all hardware or crash timings. Full target-host scale evidence and an independent verifier remain required before production acceptance.

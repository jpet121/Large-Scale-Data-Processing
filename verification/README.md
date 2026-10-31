# PEHAVOS verification evidence

**Disposition: engineering verification and 100 GB / 150 GB WSL2 acceptance evidence PASS within the stated scope; production release NOT APPROVED.**

The independent audit report provides precise recorded measurements and limitations. The `evidence/` subfolder retains the 18 original JSON receipts and their SHA-256 manifest from the uploaded evidence ZIP. The ZIP itself is not nested here so GitHub can display the records.

## What was independently verified

- Receipt ZIP and manifest integrity: all 18 evidence JSON files matched their recorded hashes.
- Source and frozen-test hashes: 27/27 matched the corrected implementation.
- Independently rerun frozen tests: 41/41 passed, 100% first-party line and measured branch coverage.
- Large-workload receipt consistency: original harness recorded PASS for 100 GB and 150 GB, including input/output hash and exact decimal reconciliation checks.

## What was not independently reexecuted

- The raw 100 GB and 150 GB files were *not* downloaded or independently rehashed in the final evidence audit. Original Linux acceptance harness computed those hashes and the auditor checked its compact records.
- WSL2 8 GB emulation does not replace testing on a dedicated physical 8 GB Linux host.
- The synthetic business policy is **test-only**. Production business-rule approval and formal release approval were not granted.

See [`PEHAVOS_FINAL_INDEPENDENT_VERIFICATION_REPORT.md`](PEHAVOS_FINAL_INDEPENDENT_VERIFICATION_REPORT.md) for the signed-off scope and exact measurements, and [`PEHAVOS_FINAL_INDEPENDENT_AUDIT_RECEIPT.json`](PEHAVOS_FINAL_INDEPENDENT_AUDIT_RECEIPT.json) for machine-readable status.

# PEHAVOS — Final Independent Scale Evidence Audit

**Project:** Large-Scale Data Processing / Streaming CSV Transaction Parser  
**Audit date:** 2026-10-31  
**Input evidence:** `PEHAVOS_TEST_EVIDENCE_TO_RETURN.zip`  
**Scope:** Unmodified corrected-v2 implementation, authoritative compiled application XML, frozen tests, and the 100 GB / 150 GB Linux WSL2 scale-run receipts.

## Disposition

- **Engineering and WSL2-scale evidence: PASS within the verified scope.** Both 100 GB and 150 GB workloads recorded successful application execution, count and monetary reconciliation, input/output SHA-256 equality, completion-marker integrity, and bounded memory. All receipt cross-checks performed by this auditor passed.
- **Recruiter-facing GitHub portfolio publication: READY WITH QUALIFICATIONS.** The project can be presented as a verified engineering demonstration, provided WSL2 virtualization and the remaining constraints are disclosed. This is **not** production certification.
- **Physical 8 GB Linux hardware acceptance: NOT CERTIFIED.** The runs used an actual Linux kernel through WSL2 configured for approximately 8 GB memory, not a dedicated hardware Linux machine.
- **Production financial deployment: HOLD.** Operator-approved schema, independent target-hardware review and explicit human release authorization are absent.

## Recorded scale measurements

| Test | Input bytes | Accepted records | Exact USD total | Peak RSS | Parser duration | Full benchmark duration | Receipt status |
|---|---:|---:|---:|---:|---:|---:|---|
| 100 GB | 100,000,089,504 | 762,405 | $76,240.50 | 21.62 MiB | 4,007.14 s | 5,127.15 s | PASS |
| 150 GB | 150,000,068,632 | 1,143,607 | $114,360.70 | 21.27 MiB | 6,480.26 s | 8,423.98 s | PASS |
| 10 million rows | 930,000,084 | 10,000,000 | $1,000,000.00 | 20.79 MiB | 228.89 s | 234.97 s | PASS |
| 1 million rows | 93,000,084 | 1,000,000 | $100,000.00 | 20.78 MiB | 23.89 s | 24.80 s | PASS |

The two large-file runs stayed substantially below the **512 MiB peak-process-memory budget**. For the large-file scenarios, `linux_acceptance.py` records a separate **1,024 MiB virtual-address-space cap**; this is not the same metric as RSS.

Each workload receipt contains 19 recorded correctness checks, all `true`, including input SHA-256 verification, exact financial ledger, record-count reconciliation, published-file marker verification and byte equality of accepted output with the all-valid synthetic input. The input and output bulk files themselves were **not included** in the 129 KB returned evidence archive.

## Independent verification conducted in this audit

1. Recomputed the returned evidence ZIP's SHA-256 digest and verified **18/18** file hashes in its manifest; no unexpected or duplicate members were found.
2. Recomputed the test-kit and corrected application manifest hashes: **165/165 implementation members** passed.
3. Verified byte-for-byte that the authoritative application XML is preserved inside the kit and implementation archive, with original XML digest `4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e`.
4. Matched **27/27** first-party source and frozen test hashes from the user's coverage receipt to the corrected implementation archive.
5. Independently cross-checked all five workload receipts against their benchmark reports and synthetic reference objects: byte sizes, source digest fields, exact Decimal monetary totals, counts, process exit codes, summary status, measured RSS, durations, WSL2 environment and all individual correctness flags. **No inconsistencies found.**
6. Independently extracted the corrected application into a clean Linux execution directory and re-ran the frozen test suite using **Python 3.13 as an unprivileged user**: **41/41 tests passed**, with **100% measured first-party line and branch coverage**, zero excluded lines, and no missing first-party files. The original archives were not modified.

**Original evidence ZIP SHA-256:** `a486f2437d933aa9145f5e70668a01734c6928a9da9b6a819aabf10a0f3a3931`  
**Corrected implementation ZIP SHA-256:** `6dd8b022d758a2fdf1cbca19212ddc5cc8c921029ba709dc69aec01bbf27c22b`

## Limitations that must remain visible

- **Raw large-file verification:** Current-turn audit independently validated the compact evidence and the harness's verification method, **not the contents of the raw 100 GB / 150 GB files**. Those files are retained on the user's external drive; their SHA-256 hashes and output equality were computed by the Linux test harness and attested in the receipts. Do not imply a second independent reader rehashed the 250 GB of raw inputs.
- **Target hardware:** An approximately 8 GB WSL2 Linux environment is a virtualized test, not certified physical Linux server hardware.
- **Scale profile:** Both large files contained **131,072 padding bytes per synthetic record**. This stresses byte-scale I/O and large-record handling; it does not establish hundreds of millions of transaction rows. A separate 10-million-row workload passed.
- **Data and policy:** Large-size cases contained valid synthetic records. Negative input and gzip recovery scenarios belong to the separately executed frozen suite. `TEST_ONLY_SCHEMA.json` is **not** an approved production financial policy.
- **Release governance:** No human release sign-off, independently witnessed physical-host certification, or approved production configuration is provided in the evidence.

## Portfolio-safe description

> Built and independently tested a Python streaming CSV financial-transaction parser. Processed 100 GB and 150 GB synthetic CSV workloads under Ubuntu on WSL2 configured with an approximately 8 GB memory limit, measuring peak process RSS of 21.62 MiB and 21.27 MiB respectively. Verified exact record reconciliation, financial totals, SHA-256 output integrity and completion markers. Independently reran 41 frozen tests with 100% first-party line coverage; tested a separate 10-million-record workload. Production hardware certification and business-policy approval remain out of scope.

## Next step

Keep the original 150 GB requirements unchanged. Publish the project as a **portfolio engineering demonstration** with this report, the reproducible test plan, original specification and application documentation. Do not claim production approval or hundreds-of-millions-of-records certification without additional evidence. If physical-server release is ever intended, complete the hardware witness, production-schema authorization, final requirement trace and explicit human release gate.

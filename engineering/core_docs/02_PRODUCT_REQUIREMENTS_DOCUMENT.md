# 02 Product Requirements Document — Streaming CSV Transaction Parser

## Product objective and use cases
The application reads standard CSV and gzip CSV incrementally and validates millions/hundreds of millions of logical records on an existing 8 GB Linux server. It emits accepted CSV, rejected CSV with provenance and reason, and a machine-readable JSON summary. Operators can run unattended and distinguish completed good data, completed inputs containing rejects, and fatal incomplete runs. Source: P23, P27, P31, P37, P42, P58–P105, P127–P139 and T_STREAM through T_CLI.

## Functional behavior
Configurable input path, output dir, batch size (10,000 default target), maximum physical/logical record size and error policy. Strict quoting/escaping/embedded multiline support; blank/missing columns and malformed amounts/timestamps/currencies rejected only when record boundaries are known. File-level parse ambiguity, bad gzip trailer, decode failure, exhausted disk or ambiguous header mapping stops safely without approved marker. Amount arithmetic exact, source identifiers/timestamps and row multiplicity preserved. A fully-read input must satisfy accepted + rejected = examined; totals aggregate accepted rows by currency only.

## Nonfunctional and security
Memory should remain approximately flat versus record count with given max bytes/batch configuration, and never materialize entire input/output. Measure throughput and peak RSS at progressive sizes and at >=100 GB and >=150 GB on the actual Linux 8 GB acceptance host. No logs containing raw sensitive rows, no external transmission. Operator-accessible staged output and logs must remain local and permissioned.

## Priorities and evidence
P84/P84_FATAL, P66, P147, P149 are absolute correctness/safety prohibitions. P115 under-512 MB is preferred. P143 correctness is prioritized over raw speed. Every binding proposition has a 1:1 engineering requirement in analysis/ENGINEERING_REVIEW.json and at least one acceptance case. No application tests have run. Release remains human-controlled and subject to exact final archive retest.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

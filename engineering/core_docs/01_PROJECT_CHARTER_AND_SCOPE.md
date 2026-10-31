# 01 Project Charter And Scope — Streaming CSV Transaction Parser

## Purpose and problem
Design a production-grade Python 3.12+ Streaming CSV Transaction Parser for a financial transaction processor. The existing whole-file pattern is reported by the owner to exhaust RAM on month-end inputs. A new implementation must stream input, validate each transaction, write reconcilable outputs and retain evidence sufficient to distinguish good records from incomplete runs. Owner evidence: P9–P23, P27, P31, P37 and P198; source task T_BUILD.

## Users, goals and limits
Operations personnel execute scheduled Linux command-line jobs on servers with 8 GB RAM. The input range includes a few megabytes to at least 150 GB, and a 100 GB+ acceptance run on 8 GB hardware. Correctness, exact decimals and no silently lost rows outrank throughput. The preferred ordinary-file peak process memory is below 512 MB (P115 preference), not a fabricated universal hard threshold. No cloud ingest, purchase of much larger servers, network financial-data upload, interactive UI or financial policy generation is in scope.

## Operating model
Operations supplies input/output paths and an explicit versioned, approved schema policy because the XML describes typical fields but no authoritative per-gateway schema, currencies, timezone rules or currency exponent precision. The build may define safe software interfaces and test-only policies; it must not infer financial business policy. Output is staged, checked and committed only after full parsing; a fatal run remains non-authoritative. Owner approval of deployed behavior is reserved.

## Completion and stop conditions
Preparation is complete only after requirement/acceptance design, 15+7 documents, audited tests and sealed Codex handoff. Production release requires executable source, 100% first-party line coverage, applicable advanced assurance and observed 100/150 GB Linux benchmark evidence. Any material unapproved financial schema choice or incomplete output treated as complete stops release. No target implementation is claimed at this stage.

---

**Authority and checkpoint.** source/contract.xml (immutable, SHA-256 4ead0b4d51a4ce04a3c5d3dc5ce447117337ce8b8e0add589fccba73859ed78e). Binding requirement IDs and independently stated acceptance cases: `analysis/ENGINEERING_REVIEW.json`. Application implementation and production approval have not occurred. PEHAVOS v1.2 coverage-first/no-mocking controls apply to all future Python increments; source is not the test oracle.

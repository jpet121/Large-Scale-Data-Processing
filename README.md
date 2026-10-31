
# Large-Scale Data Processing
### Streaming CSV Transaction Parser

**AI-Assisted Python Engineering & High-Assurance Software Verification**

> **What it does:** Processes very large financial-transaction CSV files one record at a time instead of loading the entire file into memory. It validates transactions, separates rejected records, preserves exact financial amounts, and produces auditable processing results.

**Why I built it:** To demonstrate requirements-driven Python engineering, human-directed AI-assisted implementation, large-scale data processing, and rigorous independent verification. The goal was not just to make the parser work on a small sample, but to test whether its behavior remained correct under extreme file sizes and realistic failure conditions.

**Under the hood:** Python 3.12+ · CSV streaming/generators · gzip · exact decimal accounting · automated unit and integration tests · Hypothesis · coverage.py · fault injection · differential testing · Lean 4 verification models · Ubuntu/WSL2

**Verification status:** **Portfolio engineering demonstration verified within its documented scope.** The audit recorded successful **100 GB and 150 GB** synthetic CSV runs, **41/41** independently rerun frozen tests, and **100% first-party line and branch coverage**. 

**Names and compatibility:** **Large-Scale Data Processing** is the portfolio-facing repository title. **Streaming CSV Transaction Parser** is the application's technical name. This documentation does not rename application modules, executable commands, or release archives.

[See the results](#measured-performance-at-scale) · [Understand the design](#how-it-works) · [Review the testing](#how-the-engineering-was-verified) · [Try it yourself](#try-it-yourself-ubuntu-or-wsl2) · [Read the requirements](Streaming%20CSV%20Transaction%20Parser-Project%20Requirements%20%26%20Acceptance%20Criteria.MD)

## At a glance

| Question | Answer |
| --- | --- |
| **What did I build?** | A Python streaming CSV transaction parser with record validation, explicit rejection handling, incremental outputs, and processing reports. |
| **What problem does it solve?** | Traditional approaches can exhaust RAM by loading an entire large data file into memory. Streaming allows memory use to remain bounded by record and buffer limits rather than overall file size. |
| **What skills does it demonstrate?** | Python architecture, streaming I/O, data integrity, precise financial calculations, command-line tooling, automated testing, fuzzing, fault injection, reproducible benchmarking, and evidence-based release decisions. |
| **How large was the test?** | Recorded successful synthetic workloads of **100 GB** and **150 GB**; a separate test processed **10 million rows**. |
| **Is this an AI model or agent?** | No. It is a Python data-engineering application developed through a human-directed, AI-assisted software-engineering and verification workflow. |

## The engineering problem

This project began with a **simulated financial-services client request**: a payment-processing operation needed to validate enormous CSV exports from payment gateways and internal systems without buying servers with substantially more memory.

The requirements called for correct transaction accounting, predictable failure handling, a command-line interface, and a target of **less than 512 MiB of peak process memory** on an approximately **8 GB Linux environment**, while processing input files as large as **150 GB**.

The central problem is straightforward: **file size should increase processing time, not cause memory usage to grow until the system crashes.** Correctness matters as much as speed. A file is not successfully processed if records are silently omitted, financial values change, or partially written output is mistaken for a complete result.

The original client-style brief is retained as [Project Requirements](Streaming%20CSV%20Transaction%20Parser-Project%20Requirements%20%26%20Acceptance%20Criteria.MD). It is a portfolio scenario, **not a claim of a real client engagement**.

## How it works

```text
Large CSV or gzip-compressed CSV
              |
              v
      Incremental file reader
              |
              v
  CSV parsing with bounded buffers
              |
              v
   Transaction schema validation
              |
      +-------+--------+
      |                |
    VALID            INVALID
      |                |
      v                v
Accepted records    Rejected records
(streamed output)   (reason + location)
      |                |
      +--------+-------+
               |
               v
    Reconciliation + exact totals
               |
               v
    JSON summary + completion status
```

The application is designed to preserve CSV quoting rules, process regular and gzip inputs incrementally, perform exact financial calculations, track accepted and rejected records, and distinguish recoverable record errors from file-level failures. Output publication and completion status are part of the integrity model: a failed or interrupted run should not look like an approved finished dataset.

### A simple example

| Input situation | Expected behavior |
| --- | --- |
| A valid transaction with complete fields | Validate and write it to the accepted-record output. |
| A transaction with an invalid amount or missing required field | Record a rejection with an explanation, rather than inventing or silently correcting a value. |
| An interrupted run or an output-write failure | Report the failure and avoid presenting incomplete output as successfully published. |

These illustrate the intended behavior; they are **not** claims that live bank transactions were processed.

## Measured performance at scale

The final independent evidence audit dated **October 31, 2026** checked the returned test receipts and benchmark reports from **Ubuntu running under WSL2**, configured with approximately **8 GB of memory**.

| Synthetic workload | Input size | Accepted records | Peak process RSS | Parser time | Recorded result |
| --- | ---: | ---: | ---: | ---: | --- |
| Large-file test | **100.0 GB** | 762,405 | **21.62 MiB** | 4,007.14 s | PASS |
| Large-file test | **150.0 GB** | 1,143,607 | **21.27 MiB** | 6,480.26 s | PASS |
| Row-count test | 930.0 MB | **10,000,000** | **20.79 MiB** | 228.89 s | PASS |
| Row-count test | 93.0 MB | 1,000,000 | 20.78 MiB | 23.89 s | PASS |

**What these measurements mean:**

- The two largest recorded runs stayed far below the **512 MiB peak-process-memory target** despite input sizes many times larger than the configured Linux memory limit.
- The 100 GB run reconciled **762,405 accepted records** and **$76,240.50** in exact synthetic USD totals; the 150 GB run reconciled **1,143,607 accepted records** and **$114,360.70**.
- The benchmark's **full duration**, including work outside the parser timing, was **5,127.15 seconds** for 100 GB and **8,423.98 seconds** for 150 GB. Parser time and end-to-end duration are different metrics.
- **File size is not the same as row count.** The two largest synthetic files used **131,072 padding bytes per record** to stress byte-scale I/O and large-record handling. The separate **10-million-row** workload tested row volume. The project does **not** claim a measured 150 GB run containing hundreds of millions of transactions.

The Linux test harness recorded 19 successful integrity/correctness checks for each workload, including record reconciliation, exact financial totals, output-completion markers, input checksums, and byte equality for the all-valid large-file cases. The independent auditor checked the receipts and their internal consistency; it **did not independently rehash the original 100 GB and 150 GB input files**.

## Why I built it this way

To demonstrate more than generating working Python code. I directed an engineering workflow from a written problem and execution contract through AI-assisted implementation, frozen-test verification, fault exploration, scale testing, and an independent evidence review.

That meant treating requirements, constraints, and acceptance evidence as first-class deliverables. In particular, a passing unit test is not evidence of bounded memory at 150 GB; and a successful large-file run does not establish correct handling of malformed input or crash recovery. Each claim needs its own test.

**My role:** Define the business problem and acceptance requirements, direct the AI-assisted engineering process, insist on adversarial verification, require the additional 150 GB workload, and retain human authority over release decisions. AI tools assisted with implementation and verification artifacts; the project is not presented as manually written code or as an autonomous AI system.

## How the engineering was verified

The final audit independently extracted the corrected implementation and reran the frozen test suite on **Python 3.13 under Linux**, as an unprivileged user. The evidence establishes the following bounded results:

| Verification method | What it checks | Recorded evidence |
| --- | --- | --- |
| **Frozen automated test suite** | Parsing, validation, reconciliation, output publication, failures, and regression behavior | **41/41 passed**, no failures |
| **First-party code coverage** | Executed application statements and measured branches in the declared scope | **100% line and 100% branch coverage**, zero excluded lines |
| **Property-based and stateful testing (Hypothesis)** | Generated variations and protocol invariants beyond a small set of hand-written examples | Included in the passing verification suite |
| **Differential and metamorphic testing** | Compare independently expressed behavior and consistency under input transformations | Included in the passing verification suite |
| **Fault and interruption testing** | Output-write failures, incomplete publication, termination, and replay behavior | Included in the passing verification suite |
| **Lean 4 modeling** | Selected formal reconciliation properties at the model level | Model-related checks recorded; **not** a proof of the full Python implementation |
| **Scale testing** | Memory usage, financial totals, record counts, and output integrity on large synthetic files | **100 GB, 150 GB, and 10-million-row** receipts passed |
| **Artifact integrity review** | Confirm that audited source, tests, and evidence match their manifests | **18/18 evidence files**, **165/165 implementation members**, and **27/27** source/test hash matches |

### The reasoning behind the verification

**Feynman-inspired falsification:** The emphasis was not merely on showing that normal inputs work, but on identifying assumptions and deliberately trying to break them.

**Hypothesis and differential tests:** Generated input cases and independent comparisons help uncover discrepancies that example-only tests may miss. A comparison oracle is valuable but not infallible.

**Mutation, fault, and interruption testing:** Verification must be capable of detecting wrong outcomes and failures, especially around file publication, financial accounting, and replay behavior. The current audit reports the frozen-suite result; it does not assign an unsupported global mutation score.

**Formal methods:** Lean 4 and model-correspondence checks support specific abstract properties. They do **not** mathematically certify the entire production application.

**Coverage discipline:** Full measured line and branch coverage indicates that the specified first-party code scope was executed. It does not establish that all possible errors, production conditions, or security threats were tested.

## Try it yourself (Ubuntu or WSL2)

The application is delivered as a **separate implementation/release archive**, not as a block of code embedded in this README. After obtaining and extracting that archive, locate the application root containing `distribution/` and `tests/`.

A recorded install-and-CLI verification used the packaged Python wheel and the included **synthetic** fixture:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ./distribution/streaming_csv_parser-0.1.0-py3-none-any.whl

streaming-csv-parser \
  --input tests/fixtures/GOLDEN_MIXED.csv \
  --output ./demo-output \
  --schema tests/fixtures/TEST_ONLY_SCHEMA.json
```

The mixed fixture deliberately includes records that may be rejected. Inspect the generated accepted/rejected outputs and processing status rather than assuming every record should pass or that a nonzero exit status always means the executable crashed. Use an unused output directory for each demonstration.

**Application archive publication:** The verified release archive and its evidence must be uploaded separately for this runnable example to be available to repository visitors. The repository README and requirements alone are not an executable installation.

## Requirements, evidence, and release boundaries

| Resource | Purpose |
| --- | --- |
| [Project Requirements](Streaming%20CSV%20Transaction%20Parser-Project%20Requirements%20%26%20Acceptance%20Criteria.MD) | Simulated client problem, technical constraints, deliverables, and acceptance criteria. |
| `PEHAVOS_FINAL_INDEPENDENT_VERIFICATION_REPORT.md` | Independent audit conclusions, recorded benchmarks, evidence hashes, and limitations (to be included with release materials). |
| Implementation/release ZIP | Source, tests, CLI, synthetic fixtures, and packaged application (published separately). |
| `PEHAVOS_TEST_EVIDENCE_TO_RETURN.zip` | Scale receipts and benchmark evidence reviewed during the final audit (published separately). |

**Current release decision:** The independent audit classified the project **ready for recruiter-facing portfolio publication with qualifications**, while explicitly withholding **production financial deployment approval**.

### Limitations that matter

- The 100 GB and 150 GB workloads ran on **Ubuntu/WSL2 with an approximately 8 GB memory configuration**-not a separately certified physical 8 GB Linux server.
- The scale files contained **synthetic data**, not actual payment processing records. The test schema (`TEST_ONLY_SCHEMA.json`) is not approved business policy.
- Large-byte workloads and large-row-count workloads are separate demonstrations; no claim is made that the 150 GB workload contained hundreds of millions of transactions.
- The independent audit validated the returned hashes, receipts, benchmark reports, and test rerun. It did not independently reread or rehash the original 100 GB and 150 GB raw files.
- No production integration, operator-approved schema, target-hardware sign-off, or final human production release authorization has been established.

---

**Focus:** Building reliable, inspectable software with clear requirements, memory-bounded algorithms, exact financial accounting, meaningful failure behavior, reproducible verification, and accountable human decisions-even when AI assists in the development process.

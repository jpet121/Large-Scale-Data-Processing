# Client Request: Streaming CSV Transaction Parser

**Client:** Financial Services / Payment Processing Company  
**Project Type:** Data Engineering, Performance Optimization, and Transaction Processing  
**Priority:** High — Production Processing Failures

## Business Problem

We are a financial transaction processing company that receives large CSV transaction files from multiple payment gateways, banking partners, and internal systems every day.

These files contain transaction records, payment confirmations, refunds, reversals, account identifiers, timestamps, and monetary amounts.

Our current Python processing application works correctly with smaller files, but it consistently fails when handling large transaction exports.

Some of our daily files exceed 50 GB, and certain month-end transaction archives can reach 150 GB or more.

The existing application attempts to load the entire CSV file into memory before validating and processing the transactions. When processing larger files, memory consumption increases until the operating system terminates the process.

This has caused missed reconciliation deadlines, incomplete processing runs, and additional manual work for our operations team.

Purchasing servers with significantly more RAM is not an acceptable long-term solution.

**We need a Python application that can reliably process massive CSV transaction files using a small, predictable amount of memory, regardless of the total file size.**

## What We Need Built

We want a production-ready Streaming CSV Transaction Parser that reads large transaction files incrementally rather than loading them entirely into RAM.

The application should use a memory-efficient streaming architecture, preferably involving Python generators, iterators, and bounded processing buffers.

Our goal is to process files containing millions or hundreds of millions of transactions without exhausting system memory.

### 1. Large File Processing

The application must:

- Process CSV files ranging from a few megabytes to at least 150 GB.
- Read transactions incrementally using streaming techniques.
- Never load an entire file into memory.
- Support configurable processing batches, with a default target of 10,000 records per batch.
- Release memory associated with completed batches.
- Support standard CSV files and gzip-compressed CSV files without first decompressing the entire archive to disk.
- Maintain approximately constant memory usage as file size increases, subject to configured batch size and record-size limits.

### 2. Transaction Parsing and Validation

Each transaction record will generally contain:

- Transaction ID
- Account ID
- Transaction timestamp
- Transaction type
- Transaction amount
- Currency
- Transaction status
- Payment processor reference

The parser must validate incoming records against a clearly defined transaction schema.

It must detect missing required fields, malformed timestamps, invalid monetary amounts, unsupported currencies, incorrect column structures, and incomplete records.

Financial amounts must be handled with exact decimal arithmetic rather than floating-point approximations.

The application must correctly handle standard CSV quoting and escaping rules, including quoted commas and embedded line breaks.

We cannot accept a system that silently changes transaction values or invents missing information.

### 3. Error Handling and Recovery

Our transaction exports are not always perfect.

Occasionally, a source system produces malformed or incomplete records.

We need the application to distinguish between individual invalid transactions and serious file-level errors.

For individual record errors, the parser should continue processing valid records while recording rejected transactions in a separate output file.

Each rejection should include the original record where recoverable, its source location or record number, and a clear explanation of why it failed.

For errors that make reliable parsing impossible, the application should stop safely, report the failure, and avoid presenting incomplete results as successful.

If a processing run fails halfway through, we need to know which file was affected, how many records were processed, and whether the output is complete.

A failed run must never leave partial output that could be mistaken for an approved, completed transaction file.

### 4. Streaming Output

The application should produce three primary outputs:

**Validated Transactions:** A clean CSV file containing successfully parsed and validated records, written incrementally.

**Rejected Transactions:** A separate CSV file containing invalid records and their rejection reasons.

**Processing Summary:** A machine-readable JSON report containing:

- Input filename and file size
- Processing start and completion timestamps
- Total records examined
- Number of accepted transactions
- Number of rejected transactions
- Rejection counts by error type
- Total monetary amount by currency for accepted transactions
- Total processing duration
- Average processing throughput
- Final processing status

The application must not accumulate all validated or rejected records in memory before writing them.

### 5. Resource and Performance Requirements

Our processing environment consists primarily of Linux servers with 8 GB of RAM.

The new application must operate within these constraints.

For standard transaction files, we would like the parser's peak memory usage to remain below **512 MB of process memory**, even when processing files larger than 100 GB.

We understand that unusually large individual records may require configurable safeguards.

Memory consumption should not grow proportionally with the number of records processed.

We also need reasonable throughput. The application should avoid unnecessary repeated parsing, excessive disk operations, and storing large intermediate datasets.

We expect the development team to benchmark the parser using progressively larger files and document actual throughput, memory consumption, and performance limitations.

### 6. Operation and Configuration

Our operations team should be able to run the application from the command line.

For example:

`python main.py --input transactions.csv --output ./results --batch-size 10000`

We need configurable input paths, output locations, batch sizes, record-size limits, and error-handling settings.

The system should provide useful progress information during execution without printing millions of transaction records to the console.

It should run unattended through our existing scheduled batch jobs and return meaningful exit codes so our monitoring system can distinguish successful, partially processed, and failed runs.

Repeated processing of the same input should not unintentionally append duplicate results to previously completed output files.

### 7. Data Integrity and Security

Because we process financial information, correctness is more important than artificially high throughput.

The system must preserve transaction values accurately, especially amounts, identifiers, and timestamps.

It must not silently discard records, truncate fields, or incorrectly combine data from separate transactions.

The accepted and rejected record counts must reconcile to the total number of records examined.

Sensitive payment or account information must not be exposed unnecessarily in console logs or diagnostic messages.

The parser should work entirely within our internal environment and must not require uploading financial data to an external service.

### 8. Testing and Acceptance Criteria

Before accepting the application, we need demonstrated evidence that it works under realistic operating conditions.

The development team should test:

- Small, medium, and very large CSV files.
- Files exceeding the available system RAM.
- Files containing millions of valid transactions.
- Malformed CSV content, broken quoting, and missing fields.
- Quoted delimiters, escaped quotes, and embedded newlines.
- Empty files and header-only files.
- Corrupted and truncated gzip archives.
- Oversized individual records.
- Simulated output-write failures and insufficient disk space.
- Repeated execution against the same input.
- Financial calculation accuracy and record-count reconciliation.

We specifically want memory measurements demonstrating that the application does not experience unbounded growth during long processing runs.

A successful test should demonstrate processing of a file significantly larger than system memory while staying within the agreed memory budget.

We also expect automated tests that verify parsing correctness, validation behavior, error handling, output integrity, and failure recovery.

## Expected Deliverables

We expect the completed project to include:

1. A working Python 3.12+ application.
2. Complete source code with clear separation between file reading, parsing, validation, and output writing.
3. A command-line interface for operations.
4. Automated unit, integration, and large-file performance tests.
5. A representative transaction-data generator for testing large workloads without using actual customer financial information.
6. Benchmark results documenting memory consumption and processing throughput.
7. Installation, configuration, and operating instructions.
8. Clear documentation of known limitations, error handling, and recovery procedures.

## Definition of Success

We will consider this project successful when we can provide the application with a 100 GB or larger transaction CSV file, run it on our existing 8 GB RAM Linux infrastructure, and receive validated transaction data, rejected-record details, and an accurate processing report without running out of memory.

The system must demonstrate bounded memory use, preserve financial accuracy, handle malformed records predictably, and provide verifiable evidence that no transactions were silently lost.

**Our primary objective is reliability at scale. We want file size to affect processing time, not cause uncontrolled memory consumption or application failure.**
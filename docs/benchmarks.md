# Measured benchmarks

The table immediately below records original pre-scale benchmarks on the implementation verification Linux host. Later 100 GB and 150 GB WSL2 scale results are documented in the separate section at the end of this file. Each child used a **128 MiB RLIMIT_AS address-space cap**; observed host RAM was approximately 33 GiB. Counts and exact monetary totals matched independently generated references.

| Rows | Format | Actual input bytes | Wall seconds | Kernel peak RSS (KiB) | Rows/second |
|---:|---|---:|---:|---:|---:|
| 1,000 | .csv | 149,084 | 0.101 | 13,440 | 9,895 |
| 100,000 | .csv | 14,900,084 | 1.412 | 13,440 | 70,834 |
| 1,000,000 | .csv | 149,000,084 | 13.834 | 13,440 | 72,284 |
| 100,000 | .csv.gz | 1,046,890 | 1.509 | 13,824 | 66,266 |

Peak RSS stayed approximately flat over this measured ladder. The million-row plain file (149,000,084 bytes) exceeded the 128 MiB process address-space cap, but did **not** exceed total host RAM. It does not establish the owner’s larger-than-host-RAM requirement. Gzip file size is the compressed physical size; rows represent the decompressed data.

Raw `/proc` samples, kernel wait4 RSS, input hashes, references, interpreter details and child logs are in `evidence/benchmarks.json`. Wall time includes process startup and final output hashing; input hashing precedes that timed region. Single runs are observations, not statistical guarantees or performance commitments.

Required 100 GB and >=150 GB physical files on an 8 GB Linux host were **NOT RUN**: available filesystem capacity is below 100 GB and the supplied host is not the specified 8 GB configuration. A source plus accepted output also requires additional storage. No sparse files, virtual byte streams or extrapolations are presented as acceptance evidence. Re-run the supplied generator/benchmark harness on the target system with sufficient source/output space before acceptance.

## Subsequent WSL2 acceptance-scale runs (2026-10-31)

Both large workloads ran in Ubuntu on WSL2 with approximately 8 GB RAM and 0 swap, using physical files on a USB external drive. The table shows full benchmark wall time, including generation and verification, which differs from parser-only elapsed time.

| Workload | Actual input bytes | Rows | Peak process RSS | Parser seconds | Full benchmark seconds | Result |
|---|---:|---:|---:|---:|---:|---|
| 100 GB CSV | 100,000,089,504 | 762,405 | 21.62 MiB | 4,007.14 | 5,127.15 | PASS |
| 150 GB CSV | 150,000,068,632 | 1,143,607 | 21.27 MiB | 6,480.26 | 8,423.98 | PASS |
| 10 million rows | 930,000,084 | 10,000,000 | 20.79 MiB | 228.89 | 234.97 | PASS |

The 100/150 GB scenarios padded each synthetic record with 131,072 bytes. Their success is evidence for byte-scale processing and memory bounds, **not** a hundred-million-row performance demonstration. The independently reviewed compact evidence contains receipt cross-checks but not the raw multi-GB files. WSL2 runs are not certification on dedicated physical 8 GB Linux hardware. Full details: [`verification/PEHAVOS_FINAL_INDEPENDENT_VERIFICATION_REPORT.md`](../verification/PEHAVOS_FINAL_INDEPENDENT_VERIFICATION_REPORT.md).

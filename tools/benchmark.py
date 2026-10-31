"""Linux real-file benchmark with kernel wait4 peak RSS and sampled RSS.

This measures the actual input file supplied; it never substitutes a streamed
virtual 100/150 GB input for the owner's physical-file acceptance obligation.
"""
import argparse
from collections import deque
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def benchmark(source, output, schema, *, memory_limit_mb=512, timeout_seconds=3600):
    if memory_limit_mb < 64 or timeout_seconds < 0:
        raise ValueError('BENCHMARK_LIMIT')
    source = Path(source).resolve()
    output = Path(output).resolve()
    schema = Path(schema).resolve()
    digest = hashlib.sha256()
    with source.open('rb') as handle:
        while chunk := handle.read(65536):
            digest.update(chunk)
    runner = "import resource,runpy; resource.setrlimit(resource.RLIMIT_AS, (" + str(memory_limit_mb*1048576) + ",)*2); runpy.run_path(" + repr(str(ROOT/'main.py')) + ",run_name='__main__')"
    command = [sys.executable, '-c', runner, '--input', str(source), '--output', str(output), '--schema', str(schema)]
    started = time.monotonic()
    samples = deque(maxlen=4096)
    sample_count = 0
    terminated = False
    with tempfile.TemporaryFile(mode='w+t') as logs:
        child = subprocess.Popen(command, stdout=logs, stderr=logs)
        while True:
            pid, status, usage = os.wait4(child.pid, os.WNOHANG)
            if pid:
                child.returncode = os.waitstatus_to_exitcode(status)
                break
            elapsed = time.monotonic()-started
            status_text = Path(f'/proc/{child.pid}/status').read_text()
            rss = next((int(line.split()[1]) for line in status_text.splitlines() if line.startswith('VmRSS:')), 0)
            samples.append({'elapsed_seconds': elapsed, 'rss_kib': rss})
            sample_count += 1
            if elapsed >= timeout_seconds and not terminated:
                child.terminate()
                terminated = True
            time.sleep(0.05)
        logs.seek(0)
        diagnostic = logs.read()
    duration = time.monotonic()-started
    summary_path = output/'summary.json'
    summary = json.loads(summary_path.read_text()) if child.returncode in (0, 2) and summary_path.exists() else None
    return dict(input_size_bytes=source.stat().st_size, input_sha256=digest.hexdigest(), duration_seconds=duration, peak_rss_kib=usage.ru_maxrss, rss_samples=list(samples), rss_sample_count=sample_count, sample_retention='latest 4096 samples', child_exit_code=child.returncode, memory_limit_mb=memory_limit_mb, memory_limit_kind='RLIMIT_AS virtual address-space cap, not host RAM', summary=summary, complete=child.returncode in (0, 2) and (output/'COMMITTED.json').exists(), diagnostic=diagnostic, python=sys.version, host_memory_kib=int(Path('/proc/meminfo').read_text().splitlines()[0].split()[1]), platform=sys.platform, command=command)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--schema', required=True)
    parser.add_argument('--memory-limit-mb', type=int, default=512)
    args = parser.parse_args(argv)
    print(json.dumps(benchmark(args.input, args.output, args.schema, memory_limit_mb=args.memory_limit_mb), indent=2))


if __name__ == '__main__':
    main()

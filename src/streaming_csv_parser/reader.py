"""Streaming binary sources and bounded universal physical lines."""
import gzip


def open_source(path):
    return gzip.open(path, 'rb') if str(path).endswith('.gz') else open(path, 'rb')


def physical_lines(source, limit, chunk_size=65536):
    line = bytearray()
    pending_cr = False
    while True:
        chunk = source.read(min(chunk_size, limit + 1))
        if not chunk:
            break
        # Split in C over each bounded chunk, retaining only one capped line.
        for part in chunk.splitlines(keepends=True):
            if pending_cr:
                if part.startswith(b'\n'):
                    line.extend(b'\n')
                    part = part[1:]
                if len(line) > limit:
                    raise ValueError('PHYSICAL_LINE_LIMIT')
                yield bytes(line)
                line.clear()
                pending_cr = False
            if not part:
                continue
            line.extend(part)
            if len(line) > limit:
                raise ValueError('PHYSICAL_LINE_LIMIT')
            if part.endswith(b'\r'):
                pending_cr = True
            elif part.endswith(b'\n'):
                yield bytes(line)
                line.clear()
    if line:
        yield bytes(line)

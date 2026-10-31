"""Strict CSV tokenizer with byte-bounded capture and physical provenance."""
import csv
from .models import Record
from .reader import physical_lines


class CapturingLines:
    def __init__(self, source, policy, limits):
        self.lines = iter(physical_lines(source, limits.max_line_bytes))
        self.encoding = policy.encoding
        self.limit = min(limits.max_record_bytes, limits.batch_bytes)
        self.line_number = 0
        self.reset()

    def reset(self):
        self.parts = []
        self.size = 0

    def __iter__(self):
        return self

    def __next__(self):
        raw = next(self.lines)
        self.size += len(raw)
        if self.size > self.limit:
            raise ValueError('LOGICAL_RECORD_LIMIT')
        text = raw.decode(self.encoding, errors='strict')
        self.parts.append(text)
        self.line_number += 1
        return text


def records(source, policy, limits):
    lines = CapturingLines(source, policy, limits)
    previous_limit = csv.field_size_limit(limits.max_record_bytes)
    try:
        reader = csv.reader(lines, delimiter=policy.delimiter, quotechar=policy.quotechar, doublequote=policy.doublequote, strict=True)
        number = 0
        while True:
            lines.reset()
            start = lines.line_number + 1
            fields = next(reader, None)
            if fields is None:
                break
            yield Record(fields, number, start, lines.line_number, ''.join(lines.parts))
            number += 1
    finally:
        csv.field_size_limit(previous_limit)

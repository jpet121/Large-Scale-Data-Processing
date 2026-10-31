"""Only stable codes and aggregate counters reach the console."""
import sys
from .seams import Clock


class Progress:
    def __init__(self, interval=5, clock=None, sink=None):
        self.clock = clock or Clock()
        self.sink = sink or sys.stderr
        self.interval = interval
        self.last = self.clock.monotonic()

    def emit(self, code, examined):
        now = self.clock.monotonic()
        if code != 'PROGRESS' or now - self.last >= self.interval:
            print(f'{code} examined={examined}', file=self.sink)
            self.last = now

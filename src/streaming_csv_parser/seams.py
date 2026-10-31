"""Small concrete adapters, replaceable through explicit constructor arguments."""
import time
from datetime import datetime, timezone


class Clock:
    def monotonic(self):
        return time.monotonic()

    def utc(self):
        return datetime.now(timezone.utc).isoformat()


class Events:
    def emit(self, code, examined):
        """Default local library event sink intentionally has no external effect."""

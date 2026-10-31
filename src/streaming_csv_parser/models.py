"""Immutable logical record with exact source provenance."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    fields: list[str]
    number: int
    start: int
    end: int
    raw: str

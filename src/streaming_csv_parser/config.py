"""Validate a versioned, explicitly supplied policy before creating output."""
import codecs
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Policy:
    columns: tuple[str, ...]
    required_fields: tuple[str, ...]
    timestamp_format: str
    allowed_currencies: tuple[str, ...]
    max_digits: int
    max_scale: int
    allow_sign: bool
    encoding: str
    delimiter: str
    quotechar: str
    doublequote: bool
    identity: str


def load_policy(path):
    import hashlib
    with Path(path).open('rb') as handle:
        raw = handle.read(1048577)
    if len(raw) > 1048576:
        raise ValueError('POLICY_SIZE')
    d = json.loads(raw)
    if not isinstance(d, dict) or d.get('schema_version') != 1:
        raise ValueError('POLICY_VERSION')
    columns = d.get('columns')
    required = d.get('required_fields')
    currencies = d.get('allowed_currencies')
    for values in (columns, required, currencies):
        if not isinstance(values, list) or not values or not all(isinstance(v, str) and v for v in values) or len(set(values)) != len(values):
            raise ValueError('POLICY_LIST')
    if len(columns) > 1024 or len(currencies) > 1024 or not set(required) <= set(columns) or not {'timestamp', 'amount', 'currency'} <= set(columns):
        raise ValueError('POLICY_COLUMNS')
    decimal = d.get('decimal_policy', {})
    if not isinstance(decimal, dict) or decimal.get('allow_exponent') is not False or decimal.get('allow_nonfinite') is not False or type(decimal.get('allow_sign')) is not bool:
        raise ValueError('POLICY_DECIMAL')
    for key, lower in (('max_digits', 1), ('max_scale', 0)):
        if type(decimal.get(key)) is not int or not lower <= decimal[key] <= 1000:
            raise ValueError('POLICY_DECIMAL_LIMIT')
    if not isinstance(d.get('timestamp_format'), str) or not d['timestamp_format']:
        raise ValueError('POLICY_TIMESTAMP')
    if d.get('strict_csv') is not True or type(d.get('doublequote')) is not bool:
        raise ValueError('POLICY_CSV')
    for key in ('delimiter', 'quotechar'):
        if not isinstance(d.get(key), str) or len(d[key]) != 1 or d[key] in '\r\n\x00':
            raise ValueError('POLICY_DIALECT')
    if d['delimiter'] == d['quotechar']:
        raise ValueError('POLICY_DIALECT')
    # Bounded byte-line framing requires an ASCII-compatible stateless encoding.
    encoding = codecs.lookup(d.get('encoding', '')).name
    if encoding not in ('utf-8', 'ascii', 'iso8859-1'):
        raise ValueError('POLICY_ENCODING')
    return Policy(tuple(columns), tuple(required), d['timestamp_format'], tuple(currencies), decimal['max_digits'], decimal['max_scale'], decimal['allow_sign'], encoding, d['delimiter'], d['quotechar'], d['doublequote'], hashlib.sha256(raw).hexdigest())


@dataclass(frozen=True)
class Limits:
    batch_size: int = 10000
    max_record_bytes: int = 1048576
    max_line_bytes: int = 1048576
    batch_bytes: int = 8388608

    def __post_init__(self):
        for value in (self.batch_size, self.max_record_bytes, self.max_line_bytes, self.batch_bytes):
            if type(value) is not int or not 1 <= value <= 67108864:
                raise ValueError('INVALID_LIMIT')

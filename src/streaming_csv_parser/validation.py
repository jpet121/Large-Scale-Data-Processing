"""Deterministic validation without normalizing source fields."""
import re
from datetime import datetime


def validate(fields, policy):
    if len(fields) != len(policy.columns):
        return 'COLUMN_COUNT'
    row = dict(zip(policy.columns, fields))
    if any(not row[key] for key in policy.required_fields):
        return 'MISSING_REQUIRED'
    try:
        datetime.strptime(row['timestamp'], policy.timestamp_format)
    except ValueError:
        return 'INVALID_TIMESTAMP'
    amount = row['amount']
    pattern = r'[+-]?[0-9]+(?:\.[0-9]+)?' if policy.allow_sign else r'[0-9]+(?:\.[0-9]+)?'
    if not re.fullmatch(pattern, amount):
        return 'INVALID_AMOUNT'
    digits = amount.lstrip('+-').replace('.', '')
    scale = len(amount.split('.')[1]) if '.' in amount else 0
    if len(digits) > policy.max_digits or scale > policy.max_scale:
        return 'INVALID_AMOUNT'
    if row['currency'] not in policy.allowed_currencies:
        return 'UNSUPPORTED_CURRENCY'
    return None

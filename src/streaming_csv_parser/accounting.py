"""Exact integer coefficient ledger; never uses Decimal context arithmetic."""
class Ledger:
    def __init__(self):
        self.totals = {}

    def add(self, currency, amount):
        scale = len(amount.split('.')[1]) if '.' in amount else 0
        coefficient = int(amount.replace('.', ''))
        old, old_scale = self.totals.get(currency, (0, scale))
        target_scale = max(scale, old_scale)
        self.totals[currency] = (old * 10 ** (target_scale - old_scale) + coefficient * 10 ** (target_scale - scale), target_scale)

    def strings(self):
        result = {}
        for currency, (coefficient, scale) in self.totals.items():
            digits = str(abs(coefficient)).zfill(scale + 1)
            value = digits[:-scale] + '.' + digits[-scale:] if scale else digits
            result[currency] = ('-' if coefficient < 0 else '') + value
        return result

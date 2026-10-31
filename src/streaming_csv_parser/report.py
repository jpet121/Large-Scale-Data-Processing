"""Status-aware reconciliation report."""
def build_report(identity, clock, start, started_at, examined, accepted, reasons, totals, complete):
    rejected = sum(reasons.values())
    if examined != accepted + rejected:
        raise ValueError('RECONCILIATION')
    duration = max(0, clock.monotonic() - start)
    return dict(identity, started_at_utc=started_at, completed_at_utc=clock.utc(), examined_count=examined, accepted_count=accepted, rejected_count=rejected, rejection_counts_by_type=dict(reasons), accepted_totals_by_currency=totals, duration_seconds=duration, throughput_records_per_second=examined / duration if duration else 0, status=('PARTIAL' if rejected else 'SUCCESS') if complete else 'FAILED', complete=complete)

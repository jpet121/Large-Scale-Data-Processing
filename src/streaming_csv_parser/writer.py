"""Immediate row writes through an injected private file adapter."""
import csv

REJECT_COLUMNS = ('source_record_number', 'physical_line_start', 'physical_line_end', 'error_code', 'raw_record')


class Writers:
    def __init__(self, files, policy):
        self.accepted = csv.writer(files.create('validated.csv'), lineterminator='\n')
        self.rejected = csv.writer(files.create('rejected.csv'), lineterminator='\n')
        self.accepted.writerow(policy.columns)
        self.rejected.writerow(REJECT_COLUMNS)

    def accept(self, record):
        self.accepted.writerow(record.fields)

    def reject(self, record, reason):
        self.rejected.writerow((record.number, record.start, record.end, reason, record.raw))

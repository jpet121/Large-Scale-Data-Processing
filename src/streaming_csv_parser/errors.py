"""Sanitized application failures; raw payloads never become diagnostics."""
class RunFailure(Exception):
    pass

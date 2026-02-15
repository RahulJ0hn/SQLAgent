"""PII filtering utilities.

The primary PII blocking is handled in sql_validator.py via sqlglot AST
inspection. This module provides additional post-execution filtering
to redact PII that might appear in query results.
"""

import re

# Patterns for common PII in result data
PII_PATTERNS = {
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
}


def redact_pii_from_results(rows: list[dict], redact_emails: bool = False) -> list[dict]:
    """Scan result rows and redact any PII patterns found in string values."""
    redacted = []
    for row in rows:
        new_row = {}
        for key, value in row.items():
            if isinstance(value, str):
                value = PII_PATTERNS["ssn"].sub("[REDACTED-SSN]", value)
                value = PII_PATTERNS["credit_card"].sub("[REDACTED-CC]", value)
                if redact_emails:
                    value = PII_PATTERNS["email"].sub("[REDACTED-EMAIL]", value)
            new_row[key] = value
        redacted.append(new_row)
    return redacted

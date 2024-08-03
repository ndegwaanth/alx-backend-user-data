#!/usr/bin/env python3
"""filtered_logger.py"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    a function called filter_datum that returns the log message obfuscated
    parameter:
    fields: (list): string rep all fields of obfuscated
    redaction: (string): rep what the fields will be obfuscate
    message: (string): rep the log line
    separator: (string): rep character separating all fields
    in the logline (message)
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)

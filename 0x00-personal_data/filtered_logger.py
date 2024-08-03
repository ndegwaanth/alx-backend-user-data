#!/usr/bin/env python3

import logging
import re
from typing import List

# Define PII_FIELDS constant
PII_FIELDS = ("name", "email", "ssn", "password", "phone")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Redact sensitive information in a log message."""
    pattern = "({})=[^{}]+".format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: "{}={}".format(m.group(1), redaction),
                  message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_message = record.getMessage()
        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        record.msg = filtered_message
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Creates and configures a logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


# Example Usage
if __name__ == "__main__":
    logger = get_logger()
    logger.info("name=John Doe;email=johndoe@example.com;ssn=123-45-6789;"
                "password=secret;phone=555-555-5555;")

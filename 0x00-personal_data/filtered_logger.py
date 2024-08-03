#!/usr/bin/env python3
"""filtered_logger.py"""
import logging
import re


def filter_datum(fields, redaction, message, separator):
    pattern = "({})=[^{}]+".format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: "{}={}".format(m.group(1), redaction),
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_message = record.getMessage()
        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        record.msg = filtered_message
        return super(RedactingFormatter, self).format(record)


# Example Usage
if __name__ == "__main__":
    message = ("name=Bob;email=bob@dylan.com;ssn=000-123-0000;password="
               "bobby2019;")
    log_record = logging.LogRecord("my_logger", logging.INFO, None, None,
                                   message, None, None)
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    print(formatter.format(log_record))

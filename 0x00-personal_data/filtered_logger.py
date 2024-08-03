#!/usr/bin/env python3
"""filterd_logs"""
import os
import logging
import re
import mysql.connector
from typing import List
from mysql.connector import Error

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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Establishes a connection to the MySQL database using credentials
    from environment variables."""
    try:
        # Get database credentials from environment variables
        user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
        password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
        host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
        database = os.getenv('PERSONAL_DATA_DB_NAME')

        if database is None:
            raise ValueError("The environment variable PERSONAL_DATA_DB_NAME"
                             " must be set.")

        # Establish a connection to the database
        connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )

        if connection.is_connected():
            print("Connection to the database established successfully.")
            return connection
        else:
            raise Exception("Failed to connect to the database.")

    except Error as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

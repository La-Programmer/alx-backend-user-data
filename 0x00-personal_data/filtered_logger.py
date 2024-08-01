#!/usr/bin/env python3
"""Function to filter data"""

import re
import logging


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def filter_datum(fields, redaction, message, separator) -> str:
    """A function that filter input data"""
    for key in fields:
        message = re.sub(f'{key}=([^;\\s]+)', f'{key}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """Get logger function"""
    my_logger = logging.Logger('user_data', logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter = formatter
    my_logger.addHandler(handler)
    return my_logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Remove sensitive information"""
        filtered = filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)
        return filtered
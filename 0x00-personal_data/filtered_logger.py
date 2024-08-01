#!/usr/bin/env python3
"""Function to filter data"""

import re
import logging


def filter_datum(fields, redaction, message, separator) -> str:
    """A function that filter input data"""
    for key in fields:
        message = re.sub(f'{key}=([^;\\s]+)', f'{key}={redaction}', message)
    return message


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
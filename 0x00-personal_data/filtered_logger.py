#!/usr/bin/env python3
"""Function to filter data"""

import logging
from mysql.connector import connect, MySQLConnection, Error
import os
import re
from typing import List


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')
username = os.environ.get('PERSONAL_DATA_DB_USERNAME') or 'root'
password = os.environ.get('PERSONAL_DATA_DB_PASSWORD') or ''
host = os.environ.get('PERSONAL_DATA_DB_HOST') or 'localhost'
db = os.environ.get('PERSONAL_DATA_DB_NAME')


def get_db() -> MySQLConnection:
    """DB initialization"""
    try:
        connection: MySQLConnection = connect(
            host=host,
            user=username,
            password=password,
            database=db
        )
        return connection
    except Error as error:
        print(error)
        return None


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """A function that filter input data"""
    for key in fields:
        message = re.sub(f'{key}=([^;\\s]+)', f'{key}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """Get logger function"""
    my_logger: logging.Logger = logging.Logger('user_data', logging.INFO)
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
        """Initialization function"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Remove sensitive information"""
        filtered = filter_datum(self.fields,
                                self.REDACTION,
                                super().format(record),
                                self.SEPARATOR)
        return filtered

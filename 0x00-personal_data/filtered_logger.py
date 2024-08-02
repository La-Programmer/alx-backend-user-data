#!/usr/bin/env python3
"""Function to filter data"""

import logging
from mysql.connector import connect, MySQLConnection, Error
import os
import re
import sys
from typing import List


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')
username = os.environ.get('PERSONAL_DATA_DB_USERNAME') or 'root'
password = os.environ.get('PERSONAL_DATA_DB_PASSWORD') or ''
host = os.environ.get('PERSONAL_DATA_DB_HOST') or 'localhost'
db = os.environ.get('PERSONAL_DATA_DB_NAME')


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """A function that filter input data"""
    for key in fields:
        message = re.sub(f'{key}=([^;\\s]+)', f'{key}={redaction}',
                         message,
                         flags=re.DOTALL)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization function"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Remove sensitive information"""
        filtered: str = filter_datum(self.fields, self.REDACTION,
                                     super().format(record),
                                     self.SEPARATOR)
        return filtered


def get_logger() -> logging.Logger:
    """Get logger function"""
    my_logger: logging.Logger = logging.Logger('user_data', logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter: logging.Formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    return my_logger


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


def main() -> None:
    """Main function"""
    db: MySQLConnection = get_db()
    cursor = db.cursor()
    logger = get_logger()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        phone: List[str] = row[2].split(' ')
        phone_str: str = ''
        for string in phone:
            phone_str += string
        message: str = (f"name={row[0]}; email={row[1]}; phone={phone_str}; "
                        f"ssn={row[3]}; password={row[4]}; ip={row[5]}; "
                        f"last_login={row[6]}; user_agent={row[7]};")
        logger.info(message)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Function to filter data"""

from typing import List
import re


def filter_datum(
        fields:List[str],
        redaction: str,
        message: str,
        separator: str
):
    """
    A function that filter input data based and
    obfuscates sensitive information
    """
    for field in fields:
        message = re.sub(f'{field}=([^;\s]+)', f'{field}={redaction}', message)
    return message

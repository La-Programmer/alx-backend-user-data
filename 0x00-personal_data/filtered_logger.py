#!/usr/bin/env python3
"""Function to filter data"""

from typing import List
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """A function that filter input data"""
    for key in fields:
        message = re.sub(f'{key}=([^;\\s]+)', f'{key}={redaction}', message)
    return message

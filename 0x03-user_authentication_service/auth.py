#!/usr/bin/env python3
""" Auth Module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password using bcrypt"""
    password = bytes(password, 'utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password

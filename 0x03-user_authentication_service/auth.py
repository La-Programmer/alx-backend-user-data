#!/usr/bin/env python3
""" Auth Module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt
    """
    try:
        hashed_password: bytes = bcrypt.hashpw(
            bytes(password, 'utf-8'),
            bcrypt.gensalt())
        return hashed_password
    except Exception as e:
        print("Password hashing failed due to: ", str(e))
        return None

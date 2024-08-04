#!/usr/bin/env python3

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password"""
    hashed: bytes = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check the validity of the password"""
    result: bool = bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password)
    return(result)

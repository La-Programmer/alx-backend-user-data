#!/usr/bin/env python3

import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """Hash a password"""
    hashed: ByteString = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check the validity of the password"""
    return(bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password))

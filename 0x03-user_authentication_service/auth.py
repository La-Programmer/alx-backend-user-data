#!/usr/bin/env python3
""" Auth Module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password using bcrypt"""
    password = bytes(password, 'utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Handle user registration
        """
        db = self._db
        if email is None or password is None:
            return None
        try:
            user = db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user: User = db.add_user(email, hashed_password)
            return new_user

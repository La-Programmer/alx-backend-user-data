#!/usr/bin/env python3
""" Auth Module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Handle user registration
        """
        db = self._db
        try:
            user: User = db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password: bytes = _hash_password(password)
            new_user: User = db.add_user(email, hashed_password)
            return new_user
        except Exception as e:
            print("User registration failed due to: ", str(e))
            return None

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user's login credentials
        """
        db = self._db
        try:
            user: User = db.find_user_by(email=email)
            user_password = user.hashed_password
            if bcrypt.checkpw(bytes(password, 'utf-8'), user_password):
                return True
            else:
                return False
        except Exception:
            return False

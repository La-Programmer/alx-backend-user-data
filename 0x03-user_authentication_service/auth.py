#!/usr/bin/env python3
""" Auth Module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt
    """
    hashed_password: bytes = bcrypt.hashpw(
        bytes(password, 'utf-8'),
        bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """Generate UUID and return its string repr"""
    generated = str(uuid.uuid4())
    return generated


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

    def create_session(self, email: str) -> str:
        """Create a user session
        """
        db = self._db
        try:
            user: User = db.find_user_by(email=email)
            user_session_id: str = _generate_uuid()
            db.update_user(user.id, session_id=user_session_id)
            return user_session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """Get a user from a the given session ID
        """
        db = self._db
        if session_id is None:
            return None
        try:
            user: User = db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """End a user's session
        """
        db = self._db
        try:
            user: User = db.find_user_by(id=user_id)
            setattr(user, 'session_id', None)
        except Exception:
            return None

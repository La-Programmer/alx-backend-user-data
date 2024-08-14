#!/usr/bin/env python3
""" Auth Module
"""

from db import DB
from typing import Union
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password using bcrypt"""
    password = bytes(password, 'utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """Generate new UUID
    """
    new_id: str = str(uuid4())
    return new_id


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login details
        """
        db = self._db
        if email is None or password is None:
            return None
        try:
            user = db.find_user_by(email=email)
            if user:
                user_password: bytes = user.hashed_password
                password = bytes(password, 'utf-8')
                if bcrypt.checkpw(password, user_password):
                    return True
                return False
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a session and return the ID
        """
        db = self._db
        if email is None:
            return None
        try:
            user: User = db.find_user_by(email=email)
            if user is not None:
                session_id: str = _generate_uuid()
                db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets the user of a session by the sessiond ID
        """
        db = self._db
        if session_id is None:
            return None
        try:
            user: User = db.find_user_by(session_id=session_id)
            if user is not None:
                return user
            return None
        except NoResultFound:
            return None

#!/usr/bin/env python3
"""Module Session Auth"""

from typing import TypeVar
from api.v1.auth.auth import Auth
from api.v1.views.users import User
import uuid


class SessionAuth(Auth):
    """Session Auth Class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a SessionID for a userID
        Return:
            - Session ID (string) or None
        """
        if user_id is None:
            return None
        elif not isinstance(user_id, str):
            return None
        else:
            session_id: str = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get a user ID based on a Session ID
        Return:
            - User ID (string) or None
        """
        if session_id is None:
            return None
        elif not isinstance(session_id, str):
            return None
        else:
            try:
                user_id = self.user_id_by_session_id.get(session_id)
            except Exception as e:
                user_id = None
                print(e)
            finally:
                return user_id

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get a user based on the cookie gotten from the request
        Returns:
            - User instance or None
        """
        if request is None:
            return None
        cookie: str = self.session_cookie(request)
        if cookie is None:
            return None
        user: str = self.user_id_for_session_id(cookie)
        if user is None:
            return None
        print("User", user)
        user_object = User.get(user)
        return user_object

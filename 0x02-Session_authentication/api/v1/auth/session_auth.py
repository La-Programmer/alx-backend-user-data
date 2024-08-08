#!/usr/bin/env python3
"""Module Session Auth"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session Auth Class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a SessionID for a userID
        """
        if user_id is None:
            return None
        elif not isinstance(user_id, str):
            return None
        else:
            session_id: str = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

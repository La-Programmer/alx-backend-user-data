#!/usr/bin/env python3
"""Auth Module holding base class for auth handling"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Class model to manage authentications
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path needs to authenticated
        Return:
            True if path requires authentication else False
        """
        if excluded_paths is None or path is None:
            return True
        if path in excluded_paths or path+'/' in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            excluded_path = excluded_path[0: len(excluded_path) - 1]
            if excluded_path in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Valid headers of incoming requests
        Return:
            Authorization value if contained in request header
            else None
        """
        if request is None:
            return None
        elif 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
        """
        return None

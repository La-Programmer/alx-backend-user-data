#!/usr/bin/env python3

from flask import request
from typing import List, TypeVar


class Auth():
    """Class model to manage authentications
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path needs to authenticated
        Return:
            False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization Header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
        """
        return None

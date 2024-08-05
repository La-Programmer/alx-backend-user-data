#!/usr/bin/env python3

from api.v1.auth.auth import Auth
from typing import List


class BasicAuth(Auth):
    """Class model to handle Basic Authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns:
            The base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        auth_array: List[str] = authorization_header.split(' ')
        if auth_array[0] != 'Basic':
            return None
        else:
            token: str = auth_array[1]
            return token

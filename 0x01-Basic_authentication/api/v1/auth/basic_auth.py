#!/usr/bin/env python3

import base64
from api.v1.auth.auth import Auth
import re
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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Returns:
            The decoded value of a Base64 string or None
        """
        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None
        elif not self.validate_base64(base64_authorization_header):
            return None
        else:
            decoded_str: bytes = base64.b64decode(base64_authorization_header)
            return decoded_str.decode('utf-8')

    def validate_base64(self, base64_string: str) -> bool:
        """
        Returns:
            True if the string is a valid base64 string
            and False if it is not
        """
        if (len(base64_string) % 4) != 0:
            return False
        elif re.match(r'^[a-zA-Z0-9+/=]*=?$', base64_string) is None:
            return False
        else:
            return True

#!/usr/bin/env python3
"""Basic Authentication module for handling Basic Auth"""

import base64
from api.v1.auth.auth import Auth
import hashlib
from models.user import User
import re
from typing import List, TypeVar


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
        elif self.validate_base64(base64_authorization_header) is False:
            return None
        else:
            decoded_str: bytes = base64.b64decode(base64_authorization_header)
            try:
                result: str = decoded_str.decode('utf-8')
            except Exception as e:
                print(str(e))
                result: str = None
            finally:
                return result

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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns user credentials or None
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        elif ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            info: List[str] = decoded_base64_authorization_header.split(
                ':',
                maxsplit=1)
            result: (str, str) = tuple(info)
            return result

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Get the stored user objec from the given credentials
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        elif user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user_from_db = User.search({'email': user_email})
        except Exception as e:
            print(str(e))
        if user_from_db is None or user_from_db == []:
            return None
        user_instance: User = user_from_db[0]
        password = hashlib.sha256(user_pwd.encode()).hexdigest().lower()
        if user_instance.password != password:
            return None
        return user_instance

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Engine method
        """
        auth_header: str = self.authorization_header(request)
        b64_header: str = self.extract_base64_authorization_header(auth_header)
        credentials: str = self.decode_base64_authorization_header(b64_header)
        decoded_cred: (str, str) = self.extract_user_credentials(credentials)
        user_object: User = self.user_object_from_credentials(
            decoded_cred[0],
            decoded_cred[1])
        return user_object

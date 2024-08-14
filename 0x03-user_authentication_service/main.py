#!/usr/bin/env python3
"""
Main file
"""
import json
import requests


base_url: str = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    url: str = base_url + '/users'
    data = {'email': email, 'password': password}
    try:
        response = requests.post(url, data=data)
        expected_message = {"email": f"{email}", "message": "user created"}
        assert response.status_code, 200
        assert response.text, expected_message
    except Exception as e:
        print("Exception occurred at register_user: ", str(e))


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login (with wrong password)"""
    url: str = base_url + '/sessions'
    data = data = {'email': email, 'password': password}
    try:
        response = requests.post(url, data=data)
        assert response.status_code, 401
    except Exception as e:
        print("Exception occurred at log_in_wrong_password: ", str(e))


def log_in(email: str, password: str) -> str:
    """Test login (with correct password)"""
    url: str = base_url + '/sessions'
    data = {'email': email, 'password': password}
    try:
        response = requests.post(url, data=data)
        session_id = response.cookies.get('session_id')
        expected_message = {"email": f"{email}", "message": "logged in"}
        assert response.text, expected_message
        assert response.status_code, 200
        return session_id
    except Exception as e:
        print("Exception occurred at log_in: ", str(e))


def profile_unlogged() -> None:
    """Test getting user profile (unauthorized)"""
    url: str = base_url + '/profile'
    try:
        response = requests.get(url)
        assert response.status_code, 403
    except Exception as e:
        print("Exception occurred at profile_unlogged: ", str(e))


def profile_logged(session_id: str) -> None:
    """Test getting user profile (authorized)"""
    url: str = base_url + '/profile'
    cookies = {'session_id': session_id}
    try:
        response = requests.get(url, cookies=cookies)
        expected_message = {"email": EMAIL}
        assert response.text, expected_message
        assert response.status_code, 200
    except Exception as e:
        print("Exception occurred at profile_logged: ", str(e))


def log_out(session_id: str) -> None:
    """Test logging out"""
    url: str = base_url + '/sessions'
    cookies = {'session_id': session_id}
    try:
        response = requests.delete(url, cookies=cookies)
        assert response.status_code, 302
    except Exception as e:
        print("Exception occurred at log_out: ", str(e))


def reset_password_token(email: str) -> str:
    """Test getting reset password token"""
    url: str = base_url + '/reset_password'
    data = {'email': email}
    try:
        response = requests.post(url, data=data)
        response_dict = json.loads(response.text)
        token: str = response_dict['reset_token']
        expected_message = {"email": email, "reset_token": token}
        assert response.status_code, 200
        assert response.text, expected_message
        return token
    except Exception as e:
        print("Exception occurred at reset_password_token: ", str(e))


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating user password"""
    url: str = base_url + '/reset_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
        }
    try:
        response = requests.put(url, data=data)
        expected_message = {"email": email, "message": "Password updated"}
        assert response.text, expected_message
        assert response.status_code, 200
    except Exception as e:
        print("Exception occurred at update_password: ", str(e))


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

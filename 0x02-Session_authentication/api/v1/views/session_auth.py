#!/usr/bin/env python3

from api.v1.views import app_views
from flask import abort, jsonify, request
from flask import session, Response
from models.user import User
from typing import List
import os


session_name = os.environ.get('SESSION_NAME')


@app_views.route(
    '/auth_session/login',
    methods=['POST'],
    strict_slashes=False)
def handle_login():
    """POST /api/v1/auth_session/login
    Handles the login functionality for users
    Return:
        - User Object
    """
    email: str = request.form.get('email')
    password: str = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    elif password is None:
        return jsonify({"error": "password missing"}), 400
    users: List[User] = User.search({"email": email})
    if users is None or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    user: User = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    auth.create_session(user.id)
    user_object = user.to_json()
    response: Response = jsonify(user_object)
    response.set_cookie(session_name, user_object['id'])
    return response

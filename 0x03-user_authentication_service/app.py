#!/usr/bin/env python3
"""Flask App module
"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Index route"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def register():
    """Handle user registration
    """
    email: str = request.form.get('email')
    password: str = request.form.get('password')
    if not email and email.strip():
        return jsonify({"error": "Email is required"}), 400
    if not password and password.strip():
        return jsonify({"error": "Password is required"}), 400
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Handle user login
    """
    email: str = request.form.get('email')
    password: str = request.form.get('password')
    if not email and email.strip():
        return jsonify({"error": "Email is required"}), 400
    if not password and password.strip():
        return jsonify({"error": "Password is required"}), 400
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response, 200
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Handle user logout
    """
    session_id: str = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            AUTH.destroy_session(user.id)
            return redirect(url_for("index"))
        else:
            abort(403)
    except Exception as e:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Get email of current logged in user
    """
    session_id: str = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            return jsonify({"email": f"{user.email}"}), 200
        else:
            abort(403)
    except Exception:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Get the token to reset password for a user
    """
    email: str = request.form.get('email')
    if email:
        try:
            token: str = AUTH.get_reset_password_token(email)
            if token is not None:
                return jsonify({"email": email, "reset_token": token}), 200
        except ValueError:
            abort(403)
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

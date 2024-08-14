#!/usr/bin/env python3
"""Flask App module
"""

from auth import Auth
from flask import Flask, jsonify, request


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

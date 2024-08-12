#!/usr/bin/env python3
""" Flask App
"""

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """Root endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """Handle user registration"""
    email: str = request.form.get('email')
    password: str = request.form.get('password')
    if email is None:
        return jsonify({"error": "Email is missing"}), 400
    elif password is None:
        return jsonify({"error": "Password is missing"}), 400
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
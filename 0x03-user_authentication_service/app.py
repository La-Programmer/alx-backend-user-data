#!/usr/bin/env python3
"""Flask App module
"""

from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    """Index route"""
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

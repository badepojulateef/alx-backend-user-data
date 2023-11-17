#!/usr/bin/env python3
"""
In this task, you will set up a basic Flask app.
Create a Flask app that has a single GET route ("/")
and use flask.jsonify to return a JSON payload of the form:
    {"message": "Bienvenue"}
"""


from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """Welcome route."""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

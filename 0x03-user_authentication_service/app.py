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


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Register a new user.

    This endpoint expects two form data fields: "email" and "password".
    If the user does not exist, it registers the user and responds with
    a JSON payload.
    If the user is already registered, it returns a JSON payload indicating
    the user is already registered.

    Returns:
        JSON: JSON response indicating the status of user registration.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # regsiter user if user does not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Check if the provided login credentials are valid.

    Args:
        email (str): The email of the user.
        password (str): The password to check.

    Returns:
        bool: True if the login is valid, False otherwise.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)

    else:
        # create a new session
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)

    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

#!/usr/bin/env python3
"""
In this task, you will implement the Auth.register_user
in the Auth class provided below
"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import Union


def _hash_password(password: str) -> str:
    """
    Hash the input password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted hash of the input password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a random UUID and return it as a string.

    Raises:
        ValueError: If there is an issue generating the UUID.

    Returns:
        str: The generated UUID as a string.
    """
    try:
        id = uuid4()
        return str(id)
    except ValueError as e:
        raise ValueError("Error generating UUID.") from e


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialize a new Auth instance with a connection to
        the authentication database.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """
        Register a new user in the authentication database.

        Args:
            email (str): The email of the user to be registered.
            password (str): The password of the user.

        Returns:
            Union[None, User]: Returns None if the registration is
            successful, otherwise raises a ValueError.

        Raises:
            ValueError: If the user with the given email already exists.
        """
        try:
            # Attempt to find the user with the given email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # If user does not exist, add user to the database
            return self._db.add_user(email, _hash_password(password))

        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided login credentials are valid.

        Args:
            email (str): The email of the user.
            password (str): The password to check.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            # find the user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        # validate the provided password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Create a session for the user and return the session ID.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID for the user, or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get the user corresponding to the given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User or None: The corresponding user, or None if not found.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None:
        else:
            return user

    def destroy_session(self, user_id: str) -> None:
        """
        Destroy the session for the user with the given user ID.

        Args:
            user_id (int): The user ID for which to destroy the session.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None

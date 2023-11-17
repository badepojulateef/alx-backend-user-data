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
        else:
            # If user already exists, raise an error
            raise ValueError('User {} already exists'.format(email))

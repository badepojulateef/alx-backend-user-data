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

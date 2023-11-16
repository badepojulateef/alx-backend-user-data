#!/usr/bin/env python3
"""
In this task you will create a SQLAlchemy model
named User for a database table named users (by
using the mapping declaration of SQLAlchemy).
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for the 'users' table.

    Attributes:
        id (int): The integer primary key.
        email (str): A non-nullable string representing the email.
        hashed_password (str): A non-nullable string representing the
        hashed password.
        session_id (str): A nullable string representing the session ID.
        reset_token (str): A nullable string representing the reset token.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

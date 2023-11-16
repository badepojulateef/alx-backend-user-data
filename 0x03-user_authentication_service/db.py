#!/usr/bin/env python3
"""
In this task, you will complete the DB class
provided below to implement the add_user method.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """
    In this task, you will complete the DB class
    provided below to implement the add_user method.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.
        In this task, you will complete the DB class
        provided below to implement the add_user method.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.In this task, you will complete
        the DB class provided below to implement the add_user method.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        In this task, you will complete the DB class provided
        below to implement the add_user method.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        # add new user and commit to database
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """_summary_

        Returns:
            User: _description_
        """
        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing
            attributes to update.

        Raises:
            ValueError: If an argument that does not correspond
            to a user attribute is passed.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
        return Noner

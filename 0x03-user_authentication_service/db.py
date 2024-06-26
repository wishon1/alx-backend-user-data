#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        save the user to the database.

        Args:
            email (str): The user email
            hashed_password (str): the hashed password

        Returns: The newly created user
        """
        new_usr = User(email=email, hashed_password=hashed_password)
        self._session.add(new_usr)
        self._session.commit()

        return new_usr

    def find_user_by(self, **kwargs) -> User:
        """
        find the user
        """
        if not kwargs:
            raise InvalidRequestError
        usr = self._session.query(User).filter_by(**kwargs).first()

        if not usr:
            raise NoResultFound
        return usr

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes and commits the changes to the
        database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the
            attributes to update.

        Raises:
            ValueError: If an attribute that does not exist on the
            user is passed.
        """
        # Find the user by ID
        user = self.find_user_by(id=user_id)

        # Update user attributes
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)

        # Commit the changes to the database
        self._session.commit()

        return None

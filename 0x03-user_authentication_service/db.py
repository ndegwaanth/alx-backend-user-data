#!/usr/bin/env python3
"""1. create user
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database and returns the User object"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user based on a set of filters

        Raises:
            NoResultFound: When no user is found.
            InvalidRequestError: When invalid query arguments are provided.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the given parameters.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        implement the DB.update_user method that takes as argument
        a required user_id integer and arbitrary keyword arguments,
        and returns None.
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"{key} attribute doesn't exist")
                setattr(user, key, value)
            self._session.commit()
        except NoResultFound:
            raise ValueError('User not found')
        except InvalidRequestError:
            raise ValueError('Invalid request')

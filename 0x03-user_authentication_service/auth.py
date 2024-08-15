#!/usr/bin/env python3
"""4. Hash password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from flask import session
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    define a _hash_password method that takes in a password string
    arguments and returns bytes.
    The returned bytes is a salted hash of the input password, hashed
    with bcrypt.hashpw.
    """
    salt = bcrypt.gensalt()
    new_pass = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(new_pass, salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    implement _generate_uuid function in the auth module
    The function should
    return a string representation of a new UUID.
    Use the uuid module.
    """
    random_uuid = str(uuid.uuid4())
    return random_uuid


class Auth(User):
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        take mandatory email and password string arguments
        and return a User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        implement the Auth.valid_login method. It should expect email
        and password required arguments and return a boolean.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        implement the Auth.create_session method. It takes an email
        string argument and returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=new_uuid)
            return new_uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
         implement the Auth.get_user_from_session_id method.
         It takes a single session_id string argument and returns
         the corresponding User or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        implement Auth.destroy_session. The method takes a single user_id
        integer argument and returns None.
        """
        try:
            sessionID = self._db.find_user_by(id=user_id)
            self._db.update_user(sessionID.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        implement the Auth.get_reset_password_token method.
        It take an email string argument and returns a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        new_uuid = _generate_uuid()
        self._db.update_user(user.id, reset_token=new_uuid)

    def update_password(self, reset_token: str, password: str) -> None:
        '''updates a user's password
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self._db.update_user(user.id, hashed_password=hashed_pw,
                             reset_token=None)

        return None

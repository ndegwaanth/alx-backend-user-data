#!/usr/bin/env python3
"""authentication of route"""
from typing import List, TypeVar
from flask import request


User = TypeVar('User')


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths where authentication is
            not required.
        Returns:
            bool: False - Authentication is not required.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from the request.

        Args:
            request (flask.Request, optional): The Flask request object.
            Defaults to None.
        Returns:
            str: None - Authorization header is not handled.
        """
        return None

    def current_user(self, request=None) -> User:
        """Returns the current user from the request.

        Args:
            request (flask.Request, optional): The Flask request object.
            Defaults to None.
        Returns:
            User: None - User is not handled.
        """
        return None

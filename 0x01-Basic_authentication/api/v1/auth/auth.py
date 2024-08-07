#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import TypeVar


class Auth:
    """Auth class init"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """authentication is required"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path_split in excluded_paths:
            path_split = path_split.strip('*')
            if path_split.startswith(path_split):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """header authorization"""
        if request is None:
            return None
        if not request.authorization
            return None
        item = request.authorization()
        return item

    def current_user(self, request=None) -> TypeVar('User'):
        """get the current_user"""
        return None

#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import TypeVar


class Auth:
    """Auth class init"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """authentication is required"""
        return False

    def authorization_header(self, request=None) -> str:
        """header authorization"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """get the current_user"""
        return None

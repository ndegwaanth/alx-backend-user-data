#!/usr/bin/env python3
'''auth module
'''
import os
from typing import List, TypeVar
from flask import request


class Auth:
    '''auth class
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''confirms if path is in exclluded paths
        '''
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for item in excluded_paths:
            # if item.startswith(path):
            item = item.strip('*')
            if path[-1] == '/':
                path = path[:-1]
            if item[-1] == '/':
                item = item[:-1]
            if path.startswith(item):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''gets the data from authorization header bit
        '''
        if request is None:
            return None
        value = request.authorization
        return value

    def current_user(self, request=None) -> TypeVar('User'):
        '''gets current user
        '''
        return None

    def session_cookie(self, request=None):
        '''returns a session_id cookie value from a request
        '''
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)

#!/usr/bin/env python3
'''auth module
'''
from typing import List, TypeVar
from flask import request


user = TypeVar('user')


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

    def current_user(self, request=None) -> user:
        '''gets current user
        '''
        return None

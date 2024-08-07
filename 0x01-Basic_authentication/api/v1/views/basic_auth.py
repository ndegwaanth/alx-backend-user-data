#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
import os
from models.user import  User

class BasicAuth(Auth):
    """basic auth"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Authorization header for a Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic'):
            return None
        for item in authorization_header:
            item = item.split('Basic')
            return item
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """decoded value of a Base64 string base64_authorization_header"""
        if base64_authorization_header == None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_value = base64.b64decode(base64_authorization_header).\
            decode('utf-8')
        except Exception:
            return None
        else:
            return decoded_value
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None \
            not in isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        data = decoded_base64_authorization_header.split(':')
        email = data[0]
        passwd = ':'.join(data[1:])
        return (email, passwd)
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        class BasicAuth that returns the User instance based
        on his email and password.
        """
        if user_email is None:
            return None
        if user_pwd is None:
            return None
        
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''gets user from creds
        '''
        if user_email is None or not isinstance(user_email, str) or\
                user_pwd is None or not isinstance(user_pwd, str):
            return None
        db_name = '.db_User.json'
        if not os.path.exists(db_name):
            return None
        user = User.search({'email': user_email})
        if len(user) == 0:
            return None
        '''user = user[0]
        if user.is_valid_password(user_pwd):
            return user
        return None'''
        # MODIFIED HERE
        usr_list = []
        for usr in user:
            if usr.is_valid_password(user_pwd):
                usr_list.append(usr)
        if len(usr_list) == 0:
            return None
        return usr_list

    def current_user(self, request=None) -> TypeVar('User'):
        '''gets current user
        '''
        header = self.authorization_header(request)
        if header is None:
            return None
        encoded = self.extract_base64_authorization_header(header)
        if encoded is None:
            return None
        decoded = self.decode_base64_authorization_header(encoded)
        if decoded is None:
            return None
        email, passwd = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(email, passwd)
        return user
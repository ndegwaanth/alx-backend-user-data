#!/usr/bin/env python3
'''basic auth module
'''
import os
from models.user import User
from typing import TypeVar
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''mimicks basic auth
    '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''extracts section of authorization header
        necesssary for authorization'''
        '''if authorization_header is None or\
                not isinstance(authorization_header, str) or\
                not authorization_header.startswith('Basic '):
            return None'''
        if authorization_header is None:
            return None
        authorization_header = str(authorization_header)
        if not authorization_header.startswith('Basic '):
            return None
        _, value = authorization_header.split('Basic ')
        return value

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        '''decodes and auth header
        '''
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_header = base64.b64decode(base64_authorization_header).\
                    decode('utf-8')
        except Exception:
            return None
        else:
            return decoded_header

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):
        '''extracts user creds for verification later on
        '''
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        # email, passwd = decoded_base64_authorization_header.split(':')
        # MODIFIED HERE
        data = decoded_base64_authorization_header.split(':')
        email = data[0]
        passwd = ':'.join(data[1:])
        return (email, passwd)

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str)\
            -> TypeVar('User'):
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

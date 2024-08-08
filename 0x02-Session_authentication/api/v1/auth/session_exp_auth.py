#!/usr/bin/env python3
'''module that expires a particular session
'''
import datetime
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''class that handles expiration
    '''
    def __init__(self):
        duration = os.getenv('SESSION_DURATION')
        if duration is None:
            self.session_duration = 0
        else:
            try:
                self.session_duration = int(duration)
            except Exception:
                self.session_duration = 0

    def create_session(self, user_id=None):
        '''creates a session
        '''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id,
                              'created_at': datetime.datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''finds user_id from session_id
        '''
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration == 0:
            return self.user_id_by_session_id[session_id].get('user_id')
        if 'created_at' not in self.user_id_by_session_id[session_id].keys():
            return None
        if self.user_id_by_session_id[session_id].get('created_at') +\
                datetime.timedelta(seconds=self.session_duration) <\
                datetime.datetime.now():
            return None
        return self.user_id_by_session_id[session_id].get('user_id')

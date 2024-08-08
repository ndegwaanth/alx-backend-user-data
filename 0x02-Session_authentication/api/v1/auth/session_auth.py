#!/usr/bin/env python3
'''session auth module
'''
import os
from flask import jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    '''session auth class
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a session using user_id
        '''
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns a user_id based on session_id
        '''
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''returns a User instance based on a cookie value:
        '''
        session_id_from_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id_from_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        '''deletes a user's session
        '''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True


"""@app_views.route('/auth_session/login',
methods=['POST'], strict_slashes=False)
def new_view_for_session_authentication():
    '''handles all routes for session authentication
    '''
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({ "error": "email missing" }), 400
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({ "error": "password missing" }), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({ "error": "no user found for this email" }), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response"""

#!/usr/bin/env python3
"""6. Basic Flask app"""
from flask import (Flask,
                   request,
                   jsonify,
                   abort, make_response, redirect, url_for)
import flask
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def index():
    """returning json payload"""
    return flask.jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'])
def user():
    """
    implement the end-point to register a user. Define a users function
    that implements the POST /users route.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """POST /sessions route to log in a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session ID
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    # Create the response
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    # Set session_id in cookie
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Handles the DELETE /sessions route for logging out."""
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect(url_for('index'))

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    '''retrieves reset token from user
    '''
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "reset_token": token})

@app.route('/reset_password', methods=['PUT'])
def reset_password():
    '''resets a user's password
    '''
    email = request.form.get('email')
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_Password")
    '''saved_request_token = AUTH.get_reset_password_token(email)
    if saved_reset_token != reset_token:
        abort(403)
    AUTH.update_password(reset_token, new_password)'''
    try:
        # user = AUTH._db.find_user_by(reset_token=reset_token, email=email)
        user = AUTH._db.find_user_by(email=email)
    except NoResultFound:
        abort(403)
    else:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})



if __name__ == '__main__':
    """Entry point"""
    app.run(host="0.0.0.0", port="5000")

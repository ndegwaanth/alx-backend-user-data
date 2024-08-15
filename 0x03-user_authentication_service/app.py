#!/usr/bin/env python3
"""6. Basic Flask app"""
from flask import (Flask,
                   request,
                   jsonify,
                   abort, make_response, redirect, url_for)
import flask
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


if __name__ == '__main__':
    """Entry point"""
    app.run(host="0.0.0.0", port="5000")

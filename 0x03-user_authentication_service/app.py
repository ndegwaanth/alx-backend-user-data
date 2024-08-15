#!/usr/bin/env python3
"""6. Basic Flask app"""
from flask import Flask, request, jsonify, abort, make_response
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
    """
    implement a login function to respond to the POST /sessions route.
    request expected to contain form data with "email" and a "password"fields.
    If the login information is incorrect, use flask.abort to respond
    with a 401 HTTP status
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        abort(401)

    if not email or not password:
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email,
                                      "message": "logged in"}))

    return response


if __name__ == '__main__':
    """Entry point"""
    app.run(host="0.0.0.0", port="5000")

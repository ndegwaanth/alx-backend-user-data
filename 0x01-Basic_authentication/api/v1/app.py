#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
import logging
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


# logging.basicConfig(level=logging.DEBUG,filename='test.log')


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """restricted to some resources (403)"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """ Filter each request before handling it
    """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.before_request
def before_request():
    '''called before any request is implemented
    '''
    auth = getenv('AUTH_TYPE')
    if auth == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth is not None:
        auth = Auth()
    if auth is not None and auth.require_auth(request.path,
                                              ['/api/v1/status/',
                                               '/api/v1/unauthorized/',
                                               '/api/v1/forbidden/']):
        header = auth.authorization_header(request)
        if header is None:
            abort(401)
        user = auth.current_user(request)
        if user is None:
            abort(403)


if __name__ == "__main__":
    # for rule  in app.url_map.iter_rules():
    #     print(rule)

    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

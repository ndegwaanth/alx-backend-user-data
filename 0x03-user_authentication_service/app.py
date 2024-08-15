#!/usr/bin/env python3
"""6. Basic Flask app"""
from flask import Flask
import flask

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    """returning json payload"""
    return flask.jsonify({"message": "Bienvenue"}), 200


if __name__ == '__main__':
    """Entry point"""
    app.run(host="0.0.0.0", port="5000")

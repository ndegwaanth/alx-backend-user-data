#!/usr/bin/env python3
"""6. Basic Flask app
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    """returning json payload"""
    return jsonify('{"message": "Bienvenue"}')


if __name__ == '__main__':
    """Entry point"""

    app.run(host="0.0.0.0", port="5000")

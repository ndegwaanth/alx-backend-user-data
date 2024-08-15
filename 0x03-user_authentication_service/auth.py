#!/usr/bin/env python3
"""4. Hash password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    define a _hash_password method that takes in a password string
    arguments and returns bytes.
    The returned bytes is a salted hash of the input password, hashed
    with bcrypt.hashpw.
        """
    salt = bcrypt.gensalt()
    new_pass = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(new_pass, salt)
    return hashed_password

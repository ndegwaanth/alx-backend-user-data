#!/usr/bin/env python3
"""bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

"""Auth

"""
from functools import wraps
import random
import re
import secrets

from flask import request, make_response, jsonify
from werkzeug import security

from pignus_api.models.user import User
from pignus_shared.utils import log


def auth_request(f):
    """Authentication decorator."""
    @wraps(f)
    def decorator(*args, **kwargs):
        data = {
            "status": "Error",
            "message": "",
        }
        # Get the Client ID
        client_id = None
        if 'client_id' in request.headers:
            client_id = request.headers['client_id']
        if not client_id:
            msg = "A valid Client ID is missing"
            data["message"] = msg
            log.warning(msg)
            return make_response(jsonify(data), 401)

        # Get the Api Key
        api_key = None
        if 'x-api-key' in request.headers:
            api_key = request.headers['x-api-key']

        # throw error if no token provided
        if not api_key:
            msg = "A valid Api Key is missing"
            data["message"] = msg
            log.warning(msg)
            return make_response(jsonify(data), 401)

        user = User()
        if not user.auth(client_id, api_key):
            log.warning(msg)
            return make_response(jsonify(data), 401)
        # Return the user information attached to the token
        return f(**kwargs)
    return decorator


def generate_api_key() -> str:
    """Generate a random api key."""
    avail_chars = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
        "s", "t", "u", "v", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
    ]
    the_secret = secrets.token_urlsafe(30)
    skip_strs = ["-", "_"]
    for skip_str in skip_strs:
        if skip_str not in the_secret:
            continue

        skips = [m.start() for m in re.finditer(skip_str, the_secret)]

        for skip in skips:
            temp = list(the_secret)
            temp[skip] = avail_chars[random.randint(0, len(avail_chars) - 1)]
            the_secret = "".join(temp)

    return the_secret


def generate_client_id() -> str:
    """Generate a random client_id.
    @todo: Create a check to make sure we don't make a duplicate client_id
    """
    avail_chars = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
        "s", "t", "u", "v", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
    ]
    the_secret = secrets.token_urlsafe(10)
    skip_strs = ["-", "_"]
    for skip_str in skip_strs:
        if skip_str not in the_secret:
            continue

        skips = [m.start() for m in re.finditer(skip_str, the_secret)]
        for skip in skips:
            temp = list(the_secret)
            temp[skip] = avail_chars[random.randint(0, len(avail_chars) - 1)]
            the_secret = "".join(temp)

    return the_secret


def generate_password_hash(plaintext_password: str) -> str:
    """Generate a password hash.
    """
    return security.generate_password_hash(plaintext_password)


# End File: pignus/src/pignus_api/utils/auth.py

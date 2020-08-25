import jwt
from time import time
import secrets # holds API Key / Secret
import http.client
import datetime
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def generateToken():
    token = jwt.encode(
        # Create a payload of the token containing API Key & exp time
        {"iss": secrets.API_KEY, "exp": time() + 5000},
        # Secret used to generate token signature
        secrets.API_SECRET,
        # Specify the hashing alg
        algorithm='HS256'
        # Converts token to utf-8
    ).decode('utf-8')

    return token

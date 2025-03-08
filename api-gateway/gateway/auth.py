import os
import jwt
from conf import settings
from .exceptions import (AuthTokenMissing, AuthTokenExpired, AuthTokenCorrupted)

def validate_access_token(authorization: str = None):
    """Validates and decodes the provided authorization token."""
    if not authorization:
        raise AuthTokenMissing('Authorization token is missing from the request headers.')

    token = authorization.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthTokenExpired('The provided authorization token has expired. Please authenticate again.')
    except jwt.exceptions.DecodeError:
        raise AuthTokenCorrupted('The provided authorization token is invalid or corrupted.')

def extract_authorization_headers(headers):
    """Extracts relevant headers from the request for processing."""
    extracted_headers = {}
    if headers.get('Device-ID'):
        extracted_headers['Device-ID'] = headers.get('Device-ID', None)
    if headers.get('authorization'):
        extracted_headers['Authorization'] = headers.get('authorization', None)
    return extracted_headers

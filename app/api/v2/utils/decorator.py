from functools import wraps
from flask import request

from ..models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = None
        if 'Authorization' in request.headers:
                auth_token = request.headers['Authorization']
        if not auth_token:
            response_object = dict(
                message='Token is missing.Please log in to continue.',
                status='Failed.'
            )

            return response_object, 401
        try:
            current_user = User()
            data = current_user.decode_jwt_token(auth_token)
            if data:
                pass

        except:

            response_object = dict(
                message='Token is invalid.',
                status='Failed.'
            )
            return response_object,  401

        return f(*args, **kwargs)
    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = None
        if 'Authorization' in request.headers:
                auth_token = request.headers['Authorization']
        if not auth_token:
            response_object = dict(
                message='Token is missing.Please log in to continue.',
                status='Failed.'
            )

            return response_object, 401
        try:
            current_user = User()
            data = current_user.decode_jwt_token(auth_token)
            if data['role'] == 'Admin':
                pass
            else:
                response = dict(
                    message="Admin Token is required.",
                    status="Failed."
                )
                return response, 403
        except:
            response_object = dict(
                message='Token is invalid..',
                status='Failed.'
            )
            return response_object,  401

        return f(*args, **kwargs)
    return decorated

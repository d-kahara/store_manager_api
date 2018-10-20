from functools import wraps
from flask import request

from ..models.user_model import User
from ....data import Data


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = None
        current_user = None

        if 'Authorization' in request.headers:
                auth_token = request.headers['Authorization']
        if not auth_token:
            response_object = dict(
                message='Token is missing.Please log in to continue.',
                status='Failed.'
            )

            return response_object, 401
        try:
            data = User.decode_jwt_token(auth_token)
            for user in Data.users:
                if user['email'] == data['email']:
                    current_user = user
                    print(current_user)
        except:

            response_object = dict(
                message='Token is invalid..',
                status='Failed.'
            )
            return response_object,  403

        return f(current_user, *args, **kwargs)
    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = None
        current_user = None
        admin_user = None

        if 'Authorization' in request.headers:
                auth_token = request.headers['Authorization']
        if not auth_token:
            response_object = dict(
                message='Token is missing.Please log in to continue.',
                status='Failed.'
            )

            return response_object, 401
        try:
            data = User.decode_jwt_token(auth_token)
            for user in Data.users:
                if user['email'] == data['email']:
                    current_user = user
                    if current_user['admin'] == True:
                        current_user = admin_user
                    else:
                        response=dict(
                            message="Admin Token is required.",
                            status="Failed."
                        )
                        return response, 401
                    
        except:

            response_object = dict(
                message='Token is invalid..',
                status='Failed.'
            )
            return response_object,  403

        return f(current_user, *args, **kwargs)
    return decorated

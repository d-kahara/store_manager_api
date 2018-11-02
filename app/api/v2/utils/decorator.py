from functools import wraps
from flask import request
from werkzeug.exceptions import Unauthorized

from ..models.user import User
from .db_helper import init_db

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

            dbconn = init_db()
            print(dbconn)
            curr = dbconn.cursor()
            curr.execute(
                "select * from blacklist where tokens = (%s);", (auth_token,))
            bad_token = curr.fetchone()
            if bad_token:
                raise Unauthorized('Token is Blacklisted.Try logging in again.')
 
            current_user = User()
            data = current_user.decode_jwt_token(auth_token)
            if data:
                current_user=data['sub']
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
            dbconn = init_db()
            curr = dbconn.cursor()
            curr.execute(
                "select * from blacklist where tokens = (%s);", (auth_token,))
            bad_token = curr.fetchone()[0]
            print(bad_token)
            if bad_token:
                print('baad')
                raise Unauthorized('Token is Blacklisted.Try logging in again.')

            current_user = User()
            data = current_user.decode_jwt_token(auth_token)
            
            if data['role'] == 'admin':
                pass
            else:
                response = dict(
                    message="Operation reserved to admin users.",
                    status="Failed."
                )
                return response, 403
        except:
            response_object = dict(
                message='Token is invalid Or has been blacklisted.Please try to log in again.',
                status='Failed.'
            )
            return response_object,  401

        return f(*args, **kwargs)
    return decorated

from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from flask import current_app

# Local Imports
from ....data import Data
from instance.config import key as secret_key

class User():
    """This class contains the functions of the user model"""
    password = ''

    def __init__(self, password, email, admin=False):
        """initialize the user model"""
 
        User.password = generate_password_hash(password)
        self.email = email
        self.registered_on = datetime.now()
        self.admin = admin

    @classmethod
    def validate_user_password(cls, password):

        """Compare the entered password with retrieved password"""

        return check_password_hash(User.password, password)

    def save_user(self):
        """Save User Object to Data"""

        new_user = dict(
            admin=self.admin,
            email=self.email,
            password=self.password,
            registered_on=self.registered_on
        )

        Data.users.append(new_user)
        return new_user

    @classmethod
    def find_user_by_email(cls, email):
        users = Data.users
        user = [user for user in users if user['email'] == email]
        if user:
            
            return user[0]
            
        return 'not found'

    def __repr__(self):
        return "<User '{}'>".format(self.email)

    @classmethod
    def encode_jwt_token(cls,email):
        """method to generate access token"""

        # Set up payload with an expiry date, issued at date and email claim
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=2, seconds=25),
                'iat': datetime.now(),
                'sub': email
            }

            return jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_jwt_token(jw_token):
        """method to decode the JSON web token"""

        try:
            payload = jwt.decode(jw_token, secret_key)
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'

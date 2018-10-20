from flask import request
from flask_restplus import Resource
import json, re
from validate_email import validate_email

from ..models.auth_model import Auth
from ..utils.dto import AuthDto
from ..models.user_model import User
user_auth = AuthDto.login
user_reg = AuthDto.user_reg

api = AuthDto.auth_ns

@api.route('/register')
class Register(Resource):
    """
    user registration resource
    """
    @api.response(201, 'User created successfully')
    @api.doc('Register a new User')
    @api.expect(user_reg, validate=True)

    def post(self):
        """Register a new user user"""
        data = json.loads(request.data.decode().replace("'", '"'))
        email = data['email']
        password = data['password']

        """validation for password """
        if password == '' or password == ' ':
            resp = dict(
                message='Password field must not be empty.',
                status='Failed'
            )
            return resp, 401

        # regex = "^[a-zA-Z0-9_ ]+$"
        # if re.match(regex, password):
        #     return password
        # else:
        #     resp = dict(
        #         message='Invalid email or password. Please try again',
        #         status='Failed'
        #     )
        #     return resp, 400

        

        is_valid = validate_email(email)
        if not is_valid:
            resp = dict(
                message="Invalid Email format.Email has to be of the form \'example@example.com\'.",
                status="Failed"
            )
            return resp, 400

        # save user in data list
        user = User(password, email)

        existing_user = User.find_user_by_email(email)
        if not existing_user == 'not found':
            resp = dict(
                message="User already exists.Please log in",
                status="Failed"
            )
            return resp, 202

        user.save_user()
        resp = dict(message="Successfully registered. You can now log in",        
                    email=email,
                    )

        return resp, 201



@api.route('/login')
class LoginEndpoint(Resource):
    """Endpoint for User Login"""

    @api.expect(user_auth, validate=True)

    def post(self):
        """login existing user"""
        data = json.loads(request.data.decode().replace("'", '"'))

        email = data['email']
        password = data['password']

        is_valid = validate_email(email)
        if not is_valid:
            resp=dict(
                message="Invalid Email format.Email has to be of the form \'example@example.com\'.",
                status="Failed"
            )
            return resp, 400
            

        # Fetch user by email to check if user exists
        existing_user = User.find_user_by_email(email)
        if existing_user == 'not found':
            resp = dict(
                message="Email does not exist.Please register"
            )
            return resp, 401
        

        try:
            if existing_user and User.validate_user_password(password):
                
                # Generate access token
                email= existing_user['email']
                authentication_token = User.encode_jwt_token(email)

                if authentication_token:
                    resp = dict(
                        status='success',
                        message='Login successful',
                        Authorization=authentication_token.decode()
                    )
                    return resp, 200
            else:
                resp = dict(
                    message='Invalid login credentials.Please try again'

                )
                return resp, 401
        except Exception as exception_message:
            resp = dict(
                message=str(exception_message)
            )
            return resp, 500


@api.route('/logout')
class Logout(Resource):

    @api.doc('logout a user')
    def post(self):
        """Endpoint for User Logout"""
        auth_token = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_token)

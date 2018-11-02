from flask import request
from flask_restplus import Resource
import json
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash
from validate_email import validate_email

from ..utils.dto import AuthDto
from ..models.user import User
user_login = AuthDto.auth_login
user_register = AuthDto.auth_register
from ..utils.decorator import admin_token_required

api = AuthDto.auth_ns

@api.route('/register')
class Register(Resource):
    """
    user registration resource
    """
    @admin_token_required
    @api.response(201, 'User created successfully')
    @api.doc(security='Auth_token')
    @api.expect(user_register, validate=True)
    def post(self):
        """Register a new user user"""
        data = json.loads(request.data.decode().replace("'", '"'))
        email = data['email']
        password = data['password']
        role = data['role']

        #password validation
        if password == '' or password == ' ':
            resp = dict(
                message='Password field must not be empty.',
                status='Failed'
            )
            return resp, 403

        is_valid = validate_email(email)
        if not is_valid:
            resp = dict(
                message="Invalid Email format.Email has to be of the form \'example@example.com\'.",
                status="Failed"
            )
            return resp, 400

        new_user = User(password, email, role)
        new_user.save_user()

        resp = dict(message="Successfully registered. You can now log in",
                    email=email,
                    )

        return resp, 201


@api.route('/login')
class Login(Resource):
    """Endpoint for User Login"""

    @api.expect(user_login, validate=True)
    def post(self):
        """login existing user"""
        data = json.loads(request.data.decode().replace("'", '"'))
        email = data['email']
        password = data['password']

        is_valid = validate_email(email)
        if not is_valid:
            resp = dict(
                message="Invalid Email format.Email has to be of the form \'example@example.com\'.",
                status="Failed"
            )
            return resp, 400

        #Use **kwargs to allow omission of role when logging in
        login_info = dict(email=email, password=password)
        user = User(**login_info)

        # Fetch user by email to check if user exists
        existing_user = user.get_user_by_email(email)
        print(existing_user[0]['email'])
        #sql returns tuples
        if not existing_user:
 
            raise Unauthorized('Your details were not found, please sign up')

        if not check_password_hash(existing_user[0]['password'], login_info["password"]):
            raise Unauthorized("Invalid login credentials.Please try again")
        try:
            if existing_user:

                # Generate access token pass the user role and email as claims in the jwt payload
                role = existing_user[0]['role']
                authentication_token = user.encode_jwt_token(email, role)

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

    @api.doc(security='Auth_token')
    def post(self):
        """Endpoint for User Logout"""
        auth_token = request.headers.get('Authorization')   
        if not auth_token:
            raise BadRequest(
                "No authorization header provided. This resource is secure.")
        
        response = User().decode_jwt_token(auth_token)
        if isinstance(response, str):
            # token is either invalid or expired
            raise Unauthorized(
                "Unauthorized.{}".format(response))
        else:
            # the token decoded succesfully
            # logout the user
            user_token = User().logout_user(auth_token)
            resp = dict(
                message='Successfully logged out.',
                token=user_token
            )
            return resp, 200

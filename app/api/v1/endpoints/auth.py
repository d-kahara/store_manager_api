from flask import request
from flask_restplus import Resource
import json
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
        data = json.loads(request.data.decode().replace("'", '"'))
        email = data['email']
        password = data['password']
        admin = data['admin']

        # save user in data list
        user = User(password, email, admin)
        user.save_user()
        resp = dict(message="success",
        
                    email=email,

                    )

        return resp, 201

@api.route('/login')
class Login(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        request_data = request.json
        return Auth.login_user(data=request_data)


@api.route('/logout')
class Logout(Resource):
    """
    User Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_token = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_token)

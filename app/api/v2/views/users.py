from flask import request
from flask_restplus import Resource
import json
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash
from validate_email import validate_email

from ..utils.dto import UserDto
from ..models.user import User
user_model = UserDto.user_model
update_user_model = UserDto.update_user_model
from ..utils.decorator import admin_token_required

api = UserDto.user_ns


@api.route('/')
class Users(Resource):

    @api.response(200, 'Success')
    @api.doc(security='Auth_token')
    @admin_token_required
    @api.marshal_list_with(user_model, envelope='users')
    def get(self):
        """Gets all users from db"""
        users = User().get_all()
        # resp = {
        #     "message": "success",
        #     "users": users
        # }
        return users


@api.route('/search')
class SingleUSer(Resource):
    @api.doc(security='Auth_token')
    @admin_token_required
    @api.param('email')
    @api.marshal_with(user_model, envelope='user')
    def get(self):
        """Gets a single  user given a user's email"""
        email = request.args['email']
        user = User()
        data = user.get_user_by_email(email)

        return data


@api.route('/<string:email>')
class UpdateUser(Resource):
    @api.doc(security='Auth_token')
    @admin_token_required
    @api.expect(update_user_model, validate=True)
    def put(self, email):
        """Updates user role"""
        user = User()
        data = json.loads(request.data.decode().replace("'", '"'))
        role = data['role'].lower()
        if role != 'attendant':
            if role != 'admin':
                raise BadRequest('Role can only be admin or attendant.')
        updated_user = user.update_role(role, email)
        resp = {
            "message": "success",
            "Updated_user": updated_user
        }
        return resp, 200

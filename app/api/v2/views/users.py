from flask import request
from flask_restplus import Resource
import json
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash
from validate_email import validate_email

from ..utils.dto import UserDto
from ..models.user import User
user_model = UserDto.user_model
from ..utils.decorator import admin_token_required

api = UserDto.user_ns


@api.route('/')
class Users(Resource):

    @api.response(200, 'Success')
    @api.doc(security='Auth_token')
    @admin_token_required
    def get(self):
        """"Gets all users from db"""
        users = User().get_all()
        resp = {
            "message": "success",
            "users": users
        }
        return resp, 200


@api.route('/search/<string:email>')
class SingleUSer(Resource):
    @api.doc(security='Auth_token')
    @admin_token_required
    @api.marshal_with(user_model, envelope='user')
    def get(self, email):
        """Gets a single  user given a user's email"""
        user = User()
        data = user.get_user_by_email(email)

        return data


@api.route('/<string:email>')
class UpdateUser(Resource):
    @api.doc(security='Auth_token')
    @admin_token_required
    @api.expect(user_model, validate=True)
    def put(self, email):
        """Updates user details"""
        user = User()
        data = json.loads(request.data.decode().replace("'", '"'))
        role = data['role']
        updated_user = user.update_role(role, email)
        resp = {
            "message": "success",
            "Updated_user": updated_user
        }
        return resp, 200

import json

# third party imports
from flask_restplus import Resource
from flask import request
from werkzeug.exceptions import NotFound, BadRequest

#local imports
from ..utils.dto import CartDto
from ..models.products import Product
api = CartDto.Cart_ns
model = CartDto().Cart_model
Carts_resp = CartDto.Carts_resp

from ..models.carts import Cart
from ..utils.decorator import token_required, admin_token_required
from ..models.user import User


@api.route('/<int:product_id>')
class PostCart(Resource):
    @api.doc(security='Auth_token')
    @api.expect(model, validate=True)
    def post(self, product_id):
        """
        Add a product to Cart
        """
        auth_token = None
        current_user_email = None
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
                current_user_email = data['sub']

        except:
            response_object = dict(
                message='Token is invalid.',
                status='Failed.'
            )

        data = json.loads(request.data.decode().replace("'", '"'))
        quantity = data['quantity']
        new_cart = Cart()

        return new_cart.post_cart(product_id, quantity, current_user_email)


@api.route('/<string:email>')
class GetSingleCart(Resource):
    @api.doc(security='Auth_token')
    @token_required
    @api.marshal_with(Carts_resp, envelope='Cart_record')
    def get(self, email):
        """Gets a single Cart given a user's email"""

        cart = Cart()
        data = cart.get_single_cart(email)

        return data


@api.route('/')
class AllCarts(Resource):
    @api.response(200, 'Success')
    @admin_token_required
    @api.marshal_with(Carts_resp, envelope='Carts')
    @api.doc(security='Auth_token')
    def get(self):
        """"Gets all products from db"""
        Carts = Cart().get_all()
        return Carts, 200

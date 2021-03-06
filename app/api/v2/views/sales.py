import json

# third party imports
from flask_restplus import Resource
from flask import request
from werkzeug.exceptions import NotFound, BadRequest

#local imports
from ..utils.dto import SaleDto
api = SaleDto.Sale_ns
model = SaleDto().sales_resp

from ..models.carts import Cart
from ..models.sales import Sale

from ..utils.decorator import token_required, admin_token_required
from ..models.user import User


@api.route('/')
class CreateSale(Resource):
    @api.doc(security='Auth_token')
    def post(self):
        """
        Create Sale Order
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
        new_sale = Sale()
        return new_sale.checkout(current_user_email)


@api.route('/<string:email>')
class GetSingleCart(Resource):
    @api.doc(security='Auth_token')
    @token_required
    @api.marshal_with(model, envelope='sales')
    def get(self, email):
        """Gets a single Sale given user Email"""

        sale = Sale()
        data = sale.get_single_sale(email)

        return data


@api.route('/')
class AllSales(Resource):
    @api.response(200, 'Success')
    @admin_token_required
    @api.marshal_with(model, envelope='sales')
    @api.doc(security='Auth_token')
    def get(self):
        """"Gets all sales from db"""
        sales = Sale().get_all()
        return sales, 200

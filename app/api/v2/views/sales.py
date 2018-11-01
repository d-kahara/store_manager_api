import json

# third party imports
from flask_restplus import Resource
from flask import request
from werkzeug.exceptions import NotFound, BadRequest

#local imports
from ..utils.dto import SaleDto
from ..models.products import Product
api = SaleDto.sale_ns
model = SaleDto().sale_model
sales_resp = SaleDto.sales_resp

from ..models.sales import Sale
from ..utils.decorator import token_required, admin_token_required
from ..models.user import User


@api.route('/<int:product_id>')
class Makesale(Resource):
    @api.doc(security='Auth_token')
    @api.expect(model, validate=True)
    def post(self, product_id):

        """
        Add a product to sale
        """
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
            current_user = User()
            data = current_user.decode_jwt_token(auth_token)
            if data:
                current_user_email = data['sub']

        except:
            response_object = dict(
                message='Token is invalid.',
                status='Failed.'
            )
        attendant = User()
        attendant = attendant.get_user_by_email(current_user_email)
        attendant_id = attendant[0]

        data = json.loads(request.data.decode().replace("'", '"'))
        quantity = data['quantity']
        new_sale = Sale()
        
        return new_sale.make_sale(product_id,quantity,attendant_id)
        

@api.route('/<int:sale_id>')
class GetSingleSale(Resource):
    @api.doc(security='Auth_token')
    @token_required
    @api.marshal_with(sales_resp, envelope='sale_record')
    def get(self, sale_id):
        """Gets a single sale given a sale ID"""

        sale = Sale()
        data = sale.get_single_sale(sale_id)

        return data


@api.route('/')
class AllSales(Resource):
    @api.response(200, 'Success')
    @token_required
    @api.marshal_with(sales_resp)
    @api.doc(security='Auth_token')
    def get(self):
        """"Gets all products from db"""
        sales = Sale().get_all()
        return sales, 200

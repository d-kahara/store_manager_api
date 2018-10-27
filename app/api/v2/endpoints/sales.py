import json

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import NotFound

#local imports
from ..utils.dto import SalesDto
from ..models.sales import Sales
api = SalesDto().sales_ns
model = SalesDto().sales_mod
sales_resp = SalesDto.sales_resp

from ..utils.decorator import token_required, admin_token_required


@api.route('/')
class Sales(Resource):
    doc = "This endpoint allows a store owner to create a new Sale."

    @api.response(201, 'Sale created successfully')
    @api.doc(security='Auth_token')
    @admin_token_required
    @api.expect(model, validate=True)
    def post(self):
        data = json.loads(request.data.decode().replace("'", '"'))
        posted_by = data['posted_by']
        cart_total = data['cart_total']
 

        sale = Sales(posted_by, cart_total)


        resp = dict(message="success",
                    posted_by=posted_by,
                    cart_total=cart_total,
                    )

        return resp, 201

    @api.response(200, 'Success')
    @api.doc(security='Auth_token')
    @token_required
    def get(self):
        sales = Sales().get_all()
        resp = {
            "message": "success",
            "Sales": sales
        }
        return resp, 200


@api.route('/<int:Sale_id>')
class OneSale(Resource):

    @api.marshal_with(sales_resp)
    def get(self, Sale_id):
        sale = Sales()
        data = sale.get_single_Sale(Sale_id)
        print(data)
        if not data:
            raise NotFound('Sale does not Exist.')
        return data

    def put(self, Sale):
        pass

    def delete(self, Sale_id):
        pass

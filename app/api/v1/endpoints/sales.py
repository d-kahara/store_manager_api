import json

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import NotFound


#local imports
from ..utils.dto import SalesDto
from ..models.sales_model import Sales
from ..utils.decorator import token_required


api = SalesDto.sales_ns
model = SalesDto().sales_mod
sales_resp = SalesDto().sales_resp


@api.route('/')
class Sale(Resource):
    @api.doc(security='Auth_token')
    @token_required
    @api.marshal_list_with(sales_resp, envelope='sales')
    def get(self):
        """Endpoint for getting  a list of sales"""

        sales = Sales.get_all_sales(self)
        if sales == []:
            raise NotFound('No sales made')

        return sales

    doc = "This endpoint allows a store attendant to make a sale."

    @api.response(201, 'Sale created successfully')
    @api.expect(model, validate=True)
    @api.doc(security='Auth_token')
    @token_required

    def post(self):
        """Endpoint for creating a new sale"""

        data = json.loads(request.data.decode().replace("'", '"'))
        cart_id = data['cart_id']
        posted_by = data['posted_by']
        cart_total = data['cart_total']

        # save product in data list
        sale = Sales(posted_by, cart_id, cart_total)
        sale.post_sale()
        resp = dict(message="success",
                    posted_by=posted_by,
                    cart_total=cart_total,
                    )

        return resp, 201


@api.route('/<sale_id>')
class OneProduct(Resource):

    @api.marshal_with(sales_resp)
    @api.doc(security='Auth_token')
    @token_required
    def get(self, sale_id):
        """Endpoint for getting a sale by its Id"""

        sale = Sales.get_single_sale(sale_id)

        if sale == 'not found':
            raise NotFound(
                'The requested sale_id was not found.Please try again with a different sale_id')
        return sale

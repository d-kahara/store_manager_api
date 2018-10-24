import json

# third party imports
from flask_restplus import Resource
from flask import request, make_response, jsonify
from werkzeug.exceptions import NotFound

# local imports
from ..utils.dto import productDto
from ..models.product_model import ProductModel
from ....data import Data
from ..utils.decorator import token_required, admin_token_required 

api = productDto().product_ns
model = productDto().product_mod
prod_resp = productDto().product_resp



@api.route('/')
class Product(Resource):

    @api.response(201, 'Product created successfully')
    @api.expect(model, validate=True)
    @api.doc(security='Auth_token')
    @admin_token_required
    def post(self):
        """Endpoint for creating a new product"""
        data = json.loads(request.data.decode().replace("'", '"'))
        name = data['name']
        stock = data['stock']
        min_q = data['min_q']
        category = data['category']

        product = ProductModel(name, stock, min_q, category)
        # save product in data list
        product.save_product()
        resp = dict(message="success",
                    name=name,
                    stock=stock,
                    )

        return resp, 201


    #@api.marshal_list_with(model, envelope='products')

    @api.doc(security='Auth_token')
    @token_required
    def get(self):
        """Endpoint for getting all products"""

        products = Data.products
        resp = [product for product in products]

        print(resp)
        if resp == []:  
            response_object = dict(
                message=[],
                status='success'
            )
            return response_object, 200
        return make_response(jsonify({
            "products":resp
        }), 200)

@api.route('/<int:product_id>')
class OneProduct(Resource):

    @api.marshal_with(prod_resp)
    @token_required
    @api.doc(security='Auth_token')

    def get(self, product_id):
        """Endpoint for getting a product by its id"""

        products = Data.products

        product = [product for product in products if int(
            product['product_id']) == int(product_id)]

        if not product:
            raise NotFound(
                'The requested product was not found in the database')

        return product

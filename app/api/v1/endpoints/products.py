import json

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import NotFound

# local imports
from ..utils.dto import productDto
from ..models.product_model import ProductModel
from ....data import Data

api = productDto().product_ns
model = productDto().product_mod
prod_resp = productDto().product_resp


@api.route('/')
class Product(Resource):
    doc = "This endpoint allows a store owner to create a new product."

    @api.response(201, 'Product created successfully')
    @api.doc(doc)
    @api.expect(model, validate=True)
    def post(self):
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

    @api.doc('list_of_all_products')
    @api.marshal_list_with(model, envelope='products')
    @api.response(200, 'Success')
    @api.response(404, 'No products added to the database')
    def get(self):
        products = Data.products
        resp = [p for p in products]

        if resp == []:
            raise NotFound('No Products have been added to the database')
        return resp


@api.route('/<int:product_id>')
class OneProduct(Resource):

    @api.marshal_with(prod_resp)
    def get(self, product_id):

        products = Data.products

        product = [product for product in products if int(
            product['product_id']) == int(product_id)]

        if not product:
            raise NotFound(
                'The requested product was not found in the database')

        return product

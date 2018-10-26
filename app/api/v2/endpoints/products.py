import json

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import NotFound

#local imports
from ..utils.dto import productDto
from ..models.products import Product
api = productDto().product_ns
model = productDto().product_mod
prod_resp = productDto().product_resp
from ..utils.decorator import token_required, admin_token_required



@api.route('/')
class Products(Resource):
    doc = "This endpoint allows a store owner to create a new product."

    @api.response(201, 'Product created successfully')
    @api.doc(security='Auth_token')
    @admin_token_required
    @api.expect(model, validate=True)
    def post(self):
        data = json.loads(request.data.decode().replace("'", '"'))
        product_name = data['product_name']
        inventory = data['inventory']
        min_quantity = data['min_quantity']
        category = data['category']

        product = Product(product_name, inventory, min_quantity, category)
        
        product.save_product()
     
        resp = dict(message="success",
                    product_name=product_name,
                    inventory=inventory,
                    )

        return resp, 201

    
    @api.response(200, 'Success')
    @api.doc(security='Auth_token')
    @token_required
    def get(self):
        products = Product().get_all()
        resp = {
            "message": "success",
            "Products": products
        }
        return resp, 200

@api.route('/<int:product_id>')
class OneProduct(Resource):

    @api.marshal_with(prod_resp)
    def get(self, product_id):
        product = Product()
        data = product.get_single_product(product_id)
        print(data)
        if not data:
            raise NotFound('Product does not Exist.')
        return data

    def put(self,product):
        pass
    def delete():
        pass

import json

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import NotFound, BadRequest

#local imports
from ..utils.dto import productDto
from ..models.products import Product
api = productDto().product_ns
model = productDto().product_mod
prod_resp = productDto().product_resp
prod_update_resp = productDto.product_update_resp
from ..utils.decorator import token_required, admin_token_required



@api.route('/')
class Products(Resource):

    @api.response(201, 'Product created successfully')
    @api.doc(security='Auth_token')
    @admin_token_required
    @api.expect(model, validate=True)
    
    def post(self):
        """Creates a new Product  (Admin Only)"""
        data = json.loads(request.data.decode().replace("'", '"'))
        product_name = data['product_name']
        inventory = data['inventory']
        min_quantity = data['min_quantity']
        category = data['category']
        price = data['price']

        product = Product(product_name, inventory,
                          min_quantity, category, price)

        product.save_product()
        
        new_product = dict(
            product_name=product_name.lower(),
            Stock_count=inventory,
            Category=category.lower(),
            Price_per_unit=price,
            Minimum_quantity=min_quantity
        )

        resp = dict(message="successfully created.",
                    new_product=new_product
                    )

        return resp, 201
            


    
    @api.response(200, 'Success')
    @api.doc(security='Auth_token')
    @token_required
    def get(self):
        """"Gets all products from db"""
        products = Product().get_all()
        resp = {
            "message": "success",
            "Products": products
        }
        return resp, 200

@api.route('/<int:product_id>')
class OneProduct(Resource):
    @api.doc(security='Auth_token')
    @token_required
    @api.marshal_with(prod_resp,envelope='product')
    def get(self, product_id):
        """Gets a single  product given a product ID""" 

        product = Product()
        data = product.get_single_product(product_id)

        return data


    @api.doc(security='Auth_token')
    @admin_token_required
    @api.expect(prod_update_resp, validate=False)
    def put(self,product_id):
        """Updates product details"""
        product = Product()
        existing_prd = Product().get_single_product(product_id)
        print(existing_prd[0]['inventory'])
        data = json.loads(request.data.decode().replace("'", '"'))
        
        inventory = existing_prd[0]['inventory']
        if 'inventory' in data:
            inventory = data['inventory']
        min_quantity = existing_prd[0]['min_quantity']
        if 'min_quantity' in data:
            min_quantity = data['min_quantity']
        price = existing_prd[0]['price']
        if 'price' in data:
            price = data['price']

        updated_product = product.update_product(
                inventory, min_quantity, price, product_id)
        resp = {
            "message": "success",
            "Updated_product": updated_product
        }
        return resp, 200


        

    @api.doc(security='Auth_token')
    @admin_token_required
    def delete(self, product_id):
        """Delete products"""
        product = Product()
        product.delete_product(product_id)
        response=dict(
            status='success',
            message='Product successfully deleted.'
        )
        return response, 200
        

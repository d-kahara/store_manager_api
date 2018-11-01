from flask_restplus import Namespace, fields


class productDto():
    product_ns = Namespace(
        'Products', description='Operations related to the Products ')

    product_mod = product_ns.model('product model', {
        'product_name': fields.String(required=True, description='products Name'),
        'inventory': fields.Integer(required=True, description='Products inventory'),
        'min_quantity': fields.Integer(required=True, description='Minimum Inventory Quantity Allowed'),
        'category': fields.String(required=True, description='Category of product'),
        'price': fields.Integer(required=True, description='Price of each product'),
    })

    product_resp = product_ns.model('Expected response for finding by id', {
        'product_name': fields.String(description='products Name'),
        'inventory': fields.Integer(description='Products inventory'),
        'min_quantity': fields.Integer(description='Minimum Inventory Quantity Allowed'),
        'category': fields.String(description='Category of product'),
        'product_id': fields.Integer(description='Unique Identification for products'),
        'price': fields.Integer(description='Price of each product'),
        'date_created': fields.String(description='Date created'),
        'date_modified': fields.String(description='Date modified'),

    })
    product_update_resp = product_ns.model('Expected response for finding by id', {
        'inventory': fields.Integer(required=True, description='Products inventory'),
        'min_quantity': fields.Integer(required=True, description='Minimum Inventory Quantity Allowed'),
        'category': fields.String(required=True, description='Category of product'),
        'date_modified': fields.String(description='Date modified'),
        'price': fields.Integer(description='Price of each product'),

    })

class AuthDto:
    auth_ns = Namespace('auth', description="Auth related Operations")
    auth_register = auth_ns.model('register_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
        'role': fields.String(required=True, description='The user\'s role')

    })
    auth_login = auth_ns.model('login_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),

    })


class SaleDto:
    sale_ns = Namespace('Sales', description='Sale related Operations')
    sale_model = sale_ns.model('Details required to add to cart', {
        'quantity': fields.Integer(required=True, description='Quantity of Item'),
    })
    sales_resp = sale_ns.model('Expected response for finding by id', {
        'product_name': fields.String(description='products Name'),
        'quantity': fields.Integer(description='Number of products sold'),
        'attendant_id': fields.Integer(description='Unique Identification for sales'),
        'price': fields.Integer(description='Total Price of products'),
        'created_at': fields.DateTime(dt_format='rfc822' ,description='Date product was created'),
        'sale_id': fields.Integer(description='Uniquely Identifies sale')
    })


class CategoryDto:
    category_ns= Namespace('Categories', description='Category related Operations')
    category_model = category_ns.model('Details required to create a category', {
        'category_name':fields.String(required=True, description='Name of the Category')
    })

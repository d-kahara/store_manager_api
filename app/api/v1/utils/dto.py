from flask_restplus import Namespace, fields


class productDto():
    product_ns = Namespace(
        'Products', description='Operations related to the Products ')

    product_mod = product_ns.model('product model', {
        'name': fields.String(description='products Name'),
        'stock': fields.Integer( description='Products stock'),
        'min_q': fields.Integer( description='Minimum Inventory Quantity Allowed'),
        'category': fields.String(description='Category of product'),
    })

    product_resp = product_ns.model('Expected response for finding by id', {
        'name': fields.String(description='products Name'),
        'stock': fields.Integer(description='Products stock'),
        'min_q': fields.Integer(description='Minimum Inventory Quantity Allowed'),
        'category': fields.String(description='Category of product'),
        'product_id': fields.Integer(description='Unique Identification for products'),
        'date_created': fields.DateTime(dt_format='rfc822', description='Date created'),
    })


class SalesDto():
    sales_ns = Namespace(
        'Sales', description='Operations related to the Sales ')
    cart_model = fields.String(description='Cart object')

    sales_mod = sales_ns.model('sales model', {
        'cart_id': fields.Integer(required=True, description='The cart where sale is being checked out from '),
        'posted_by': fields.String(required=True, description='The store attendant posting the sale'),
        'cart_total': fields.Integer(required=True, description='Total worth of goods bought'),
        'cart': fields.List(cart_model),

    })
    cart_model = fields.String(description='Cart object')
    sales_resp = sales_ns.model('Expected response for get methods on sales', {
        'sale_id': fields.Integer( description='Unique Identification for sales'),
        'cart': fields.List(cart_model),
        'posted_by': fields.String(required=True, description='The store attendant posting the sale'),
        'cart_total': fields.Integer(required=True, description='Total worth of goods bought'),
        'date_created': fields.DateTime( descriprion='Date created'),
    })

class AuthDto:
    auth_ns = Namespace('auth', description="Auth related Operations")
    auth = auth_ns.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
        'admin': fields.Boolean(default=False,required=True,description='The user\'s role')
        
    })



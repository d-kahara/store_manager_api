from flask_restplus import Namespace, fields


class productDto():
    product_ns = Namespace(
        'Products', description='Operations related to the Products ')

    product_mod = product_ns.model('product model', {
        'name': fields.String(description='products Name'),
        'stock': fields.Integer(description='Products stock'),
        'min_q': fields.Integer(description='Minimum Inventory Quantity Allowed'),
        'category': fields.String(description='Category of product'),
    })

    product_resp = product_ns.model('Expected response for finding by id', {
        'name': fields.String(description='products Name'),
        'stock': fields.Integer(description='Products stock'),
        'min_q': fields.Integer(description='Minimum Inventory Quantity Allowed'),
        'category': fields.String(description='Category of product'),
        'product_id': fields.Integer(description='Unique Identification'),
        'created_at': fields.DateTime(descriprion='Date created', dt_format='rfc822'),
    })

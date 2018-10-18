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
        'product_id': fields.Integer(description='Unique Identification for products'),
        'created_at': fields.String(descriprion='Date created'),
    })


class SalesDto():
    sales_ns = Namespace(
        'Sales', description='Operations related to the Sales ')

    sales_mod = sales_ns.model('sales model', {
        'cart_id': fields.Integer(description='The cart where sale is being checked out from '),
        'posted_by': fields.String(description='The store attendant posting the sale'),
        'cart_total': fields.Integer(description='Total worth of goods bought'),

    })

    sales_resp = sales_ns.model('Expected response for get methods on sales', {
        'sale_id': fields.Integer(description='Unique Identification for sales'),
        'cart_id': fields.Integer(description='The cart where sale is being checked out from '),
        'posted_by': fields.String(description='The store attendant posting the sale'),
        'cart_total': fields.Integer(description='Total worth of goods bought'),
        'created_at': fields.String(descriprion='Date created'),
    })

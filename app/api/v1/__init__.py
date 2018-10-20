"""" Config for registering blueprints"""


from flask_restplus import Api
from flask import Blueprint


version1 = Blueprint('version1', __name__, url_prefix="/api/v1")

from .endpoints.products import api as prod_ns
from .endpoints.sales import api as sales_ns
from .endpoints.auth import api as auth_ns


#Restplus configurations

api = Api(version1,
          title='Store  Manager Api',
          version='1.0',
          description="An implementation of a store management API")

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(prod_ns, path="/products")
api.add_namespace(sales_ns, path="/sales")

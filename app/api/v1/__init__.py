"""" Config for registering blueprints"""


from flask_restplus import Api
from flask import Blueprint


version1 = Blueprint('version1', __name__, url_prefix="/api/v1")

from .endpoints.products import api as prod_ns


#Restplus configurations

api = Api(version1,
          title='Store  Manager Api',
          version='1.0',
          description="An implementation of a store management API")

api.add_namespace(prod_ns, path="/products")

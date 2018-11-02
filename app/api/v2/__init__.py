"""" Config for registering blueprints"""


from flask_restplus import Api
from flask import Blueprint


version2 = Blueprint('version2', __name__, url_prefix="/api/v2")


from .views.auth import api as auth_ns
from .views.products import api as products_ns
from .views.sales import api as sales_ns
from .views.category import api as category_ns
from .views.users import api as user_ns


#Restplus configurations
authorizations = {'Auth_token': {
	'type': 'apiKey',
	'in': 'header',
	'name': 'Authorization'
}}

api = Api(version2,
          title='Store  Manager Api',
          version='2.0',
          description="An implementation of a store management API",
          authorizations=authorizations)

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(user_ns, path='/users')
api.add_namespace(products_ns, path='/products')
api.add_namespace(category_ns, path='/categories')
api.add_namespace(sales_ns, path='/sales')

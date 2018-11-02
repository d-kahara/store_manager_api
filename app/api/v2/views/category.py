from ..models.category import Category
from flask_restplus import Resource
import json
from flask import request
from ..utils.dto import CategoryDto

api = CategoryDto.category_ns
model = CategoryDto.category_model

@api.route('/')
class CreateCategory(Resource):
    @api.doc(security='Auth_token')
    @api.expect(model, validate=True)
    def post(self):
        """Creates a new category"""
        data = json.loads(request.data.decode().replace("'", '"'))
        category_name = data['category_name']
        new_category = Category()
        return new_category.add_category(category_name)


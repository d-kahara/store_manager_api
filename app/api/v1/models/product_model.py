from flask import request, make_response, jsonify
from werkzeug.exceptions import NotFound

from datetime import datetime
from ....data import Data


class ProductModel():
    """This class encapsulates the functions of the product model"""

    def __init__(self, name, stock, min_q, category, product_id=0):
        """initialize the question model"""
        self.name = name
        self.stock = stock
        self.min_q = min_q
        self.date_created = datetime.now()
        self.category = category
        self.product_id = product_id

    def save_product(self):
        product_id = len(Data.products) + 1
        product = {
            "product_id": product_id,
            "name": self.name,
            "min_q": self.min_q,
            "category": self.category,
            "stock": self.stock,
            "date_created": self.date_created

        }
        #save the product to the products list
        Data.products.append(product)

    @staticmethod
    def edit_product(product_id):
        """method to Edit Product details"""
 
        update_prd = [
            prod for prod in Data.products if prod['product_id'] == product_id]
 
        if update_prd:
            # print(update_prd)
            # update_prd[0]['name'] = name
            # update_prd[0]['stock'] = stock
            # update_prd[0]['category'] = category
            # update_prd[0]['min_q'] = min_q  
            return update_prd
        raise NotFound('Product Not Found')

    @staticmethod
    def delete_product(product_id):
        """Class method to delete products from inventory"""

        deleted_prd = [
            prod for prod in Data.products if prod['product_id'] == product_id]
        if deleted_prd:
            Data.products.remove(deleted_prd[0])
            return deleted_prd
        raise NotFound('Product Not Found')
        

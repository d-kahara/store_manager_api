from datetime import datetime
from werkzeug.exceptions import  NotFound, Forbidden
import psycopg2.extras as extras
from psycopg2 import Error
import psycopg2


from ..utils.db_helper import init_db


class Product():
    """This class encapsulates the functions of the product model"""

    def __init__(self, product_name='wiko', inventory='12', min_quantity='5', category='electronics', price=0):
        """initialize the product model"""
        self.product_name = product_name
        self.inventory = inventory
        self.min_quantity = min_quantity
        self.date_created = datetime.now().replace(second=0, microsecond=0)
        self.date_modified = datetime.now().replace(second=0, microsecond=0)
        self.category = category
        self.price = price
        self.db = init_db()

    def save_product(self):

        new_product = dict(
            product_name=self.product_name.lower(),
            min_quantity=self.min_quantity,
            category=self.category.lower(),
            inventory=self.inventory,
            date_created=self.date_created,
            date_modified=self.date_modified,
            price=self.price
            ) 

        # check if product exists
        if self.check_if_product_exists(new_product['product_name'].lower()):
            raise Forbidden("product already exists.You may Edit or Delete this product")

        curr = self.db.cursor()
        category_name=self.category
        curr.execute(
            "select * from categories where category_name = (%s);", (category_name.lower(),))
        category = curr.fetchone()
        if not category:
            raise Forbidden('Category does not exist.')
        sql = """INSERT INTO products (product_name,min_quantity, category, inventory,date_created,date_modified,price) \
            VALUES ( %(product_name)s, %(min_quantity)s, %(category)s, %(inventory)s, %(date_created)s, %(date_modified)s,%(price)s);
            """
        curr.execute(sql, new_product)
        self.db.commit()
        curr.close()

    def check_if_product_exists(self, product_name):
        database = self.db
        curr = database.cursor()
        curr.execute(
            "select * from products where product_name = (%s);", (product_name.lower(),))
        result = curr.fetchone()
        if result:
            return True

    def check_if_product_exists_by_id(self, product_id):
        database = self.db
        curr = database.cursor()
        curr.execute(
            "select * from products where product_id = (%s);", (product_id,))
        result = curr.fetchone()
        if result:
            return True

    def get_all(self):
        """This function returns a list of all the products"""
        dbconn = self.db
        curr = dbconn.cursor(cursor_factory=extras.DictCursor)
        curr.execute("""SELECT * FROM products;""")
        #returns a python dictionary like interface 
        rows = curr.fetchall()
        resp = []

        for row in rows:
            resp.append(dict(row))
        return resp
        
    def get_single_product(self, product_id):
        """return single product from the db given an product_id"""
        # check if product exists
        if not self.check_if_product_exists_by_id(product_id):
            raise NotFound(
                "Product  does not exist.")
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        curr.execute(
            "SELECT product_name, category, inventory, min_quantity, date_created,date_modified,price, product_id FROM products WHERE product_id = (%s);", (product_id,))
        rows = curr.fetchall()
        curr.close()
        resp = []

        for row in rows:
            resp.append(dict(row))
        return resp
    
    def update_product(self, inventory,min_quantity,price,product_id):
        """update the field of an item given the item_id"""
        dbconn = self.db
        curr = dbconn.cursor(cursor_factory=extras.DictCursor)

        # check if product exists
        if not self.check_if_product_exists_by_id(product_id):
            raise Forbidden(
                "Product  does not exist.")


        try:
            date_modified = datetime.now().replace(second=0, microsecond=0)

            curr.execute("UPDATE products SET inventory= %s, min_quantity= %s,date_modified = %s, price=%s WHERE product_id = %s RETURNING product_name,category, inventory ,min_quantity,date_modified, price",
                         (inventory, min_quantity, date_modified, price, product_id,))
          
            rows = curr.fetchall()
            curr.close()
            dbconn.commit()
            resp = []

            for row in rows:
                resp.append(dict(row))
            return resp
            
        except (Exception, psycopg2.DatabaseError) as error:
            response= dict(
                status="Failed.",
                Message=error
            )
            return response

    def delete_product(self, product_id):
        """Delete product from the db given an product_id"""
        # check if product exists
        if not self.check_if_product_exists_by_id(product_id):
            raise Forbidden(
                "Product  does not exist.")
        dbconn = self.db
        curr = self.db.cursor()
        curr.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        curr.close()
        dbconn.commit()

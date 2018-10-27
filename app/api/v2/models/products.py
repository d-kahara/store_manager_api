from datetime import datetime
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden
import psycopg2.extras as extras
from psycopg2 import Error
import psycopg2


from ..utils.db_helper import init_db


class Product():
    """This class encapsulates the functions of the product model"""

    def __init__(self, product_name='wiko', inventory='12', min_quantity='5', category='electronics'):
        """initialize the product model"""
        self.product_name = product_name
        self.inventory = inventory
        self.min_quantity = min_quantity
        self.date_created = datetime.now()
        self.date_modified = datetime.now()
        self.category = category
        self.db = init_db()

    def save_product(self):

        new_product = dict(
            product_name=self.product_name,
            min_quantity=self.min_quantity,
            category=self.category,
            inventory=self.inventory,
            date_created=self.date_created,
            date_modified=self.date_modified

        ) 
        # check if product exists
        if self.check_if_product_exists(new_product['product_name']):
            raise Forbidden("product already exists.You may Edit or Delete this product")

        curr = self.db.cursor()

        sql = """INSERT INTO products (product_name,min_quantity, category, inventory,date_created,date_modified) \
            VALUES ( %(product_name)s, %(min_quantity)s, %(category)s, %(inventory)s, %(date_created)s, %(date_modified)s);
            """
        curr.execute(sql, new_product)
        self.db.commit()
        curr.close()

    def check_if_product_exists(self, product_name):
        database = self.db
        curr = database.cursor()
        curr.execute(
            "select * from products where product_name = (%s);", (product_name,))
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
        print(rows)
        resp = []

        for row in rows:
            resp.append(dict(row))
        return resp
        
    def get_single_product(self, product_id):
        """return single product from the db given an product_id"""
        # check if product exists
        if not self.check_if_product_exists_by_id(product_id):
            raise Forbidden(
                "Product  does not exist.")
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        curr.execute(
            "SELECT product_name, category, inventory, min_quantity, date_created, product_id FROM products WHERE product_id = (%s);", (product_id,))
        rows = curr.fetchall()
        curr.close()
        resp = []

        for row in rows:
            resp.append(dict(row))
        return resp
    
    def update_product(self, product_name, category,  inventory,min_quantity,product_id):
        """update the field of an item given the item_id"""
        # check if product exists
        if not self.check_if_product_exists_by_id(product_id):
            raise Forbidden(
                "Product  does not exist.")
        try:
            dbconn = self.db
            curr = dbconn.cursor(cursor_factory=extras.DictCursor)
            curr.execute( "UPDATE products SET product_name= %s, category= %s, inventory= %s, min_quantity= %s WHERE product_id = %s RETURNING product_name,category, inventory ,min_quantity",
            (product_name,category,inventory,min_quantity,product_id,))
          
            rows = curr.fetchall()
            print(rows)
            curr.close()
            dbconn.commit()
            resp = []

            for row in rows:
                print(row)
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

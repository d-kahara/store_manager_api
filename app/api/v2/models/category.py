from werkzeug.exceptions import NotFound, Forbidden
from ..utils.db_helper import init_db
import psycopg2.extras as extras
import psycopg2

class Category:

    def __init__(self, category_name='Food'):
        self.category_name = category_name
        self.db = init_db()


    def add_category(self, category_name):
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute(
            "select * from categories where category_name = (%s);", (category_name.lower(),))
        category = curr.fetchone()
        if category:
            raise Forbidden('Category already exists')
        sql = """
                INSERT INTO categories 
                VALUES (%(category_name)s) RETURNING category_name;
                """
        category_name = dict(
            category_name=category_name.lower()
        )
        curr.execute(sql, category_name)
        category_name = curr.fetchone()[0]
        dbconn.commit()
        curr.close()
        response = dict(
            message='Category successfully added.',
            category_name=category_name
        )
        return response

    def get_all(self):
            """This function returns a list of all the categories"""
            dbconn = self.db
            curr = dbconn.cursor(cursor_factory=extras.DictCursor)
            curr.execute("""SELECT * FROM categories;""")
            #returns a python dictionary like interface
            rows = curr.fetchall()
            resp = []
            for row in rows:
                resp.append(dict(row))
            return resp

        # def update_category(self, inventory, min_quantity, price, product_id):
        #     """update the field of an item given the item_id"""
        #     dbconn = self.db
        #     curr = dbconn.cursor(cursor_factory=extras.DictCursor)

        #     # check if product exists
        #     if not self.check_if_product_exists_by_id(product_id):
        #         raise Forbidden(
        #             "Product  does not exist.")

        #     try:
        #         date_modified = datetime.now().replace(second=0, microsecond=0)

        #         curr.execute("UPDATE products SET inventory= %s, min_quantity= %s,date_modified = %s, price=%s WHERE product_id = %s RETURNING product_id, product_name,category, inventory ,min_quantity,date_modified,date_created, price",
        #                     (inventory, min_quantity, date_modified, price, product_id,))

        #         rows = curr.fetchall()
        #         curr.close()
        #         dbconn.commit()
        #         resp = []

        #         for row in rows:
        #             resp.append(dict(row))
        #         return resp

        #     except (Exception, psycopg2.DatabaseError) as error:
        #         response = dict(
        #             status="Failed.",
        #             Message=error
        #         )
        #         return response

        # def delete_product(self, product_id):
        #     """Delete product from the db given an product_id"""
        #     # check if product exists
        #     if not self.check_if_product_exists_by_id(product_id):
        #         raise Forbidden(
        #             "Product  does not exist.")
        #     dbconn = self.db
        #     curr = self.db.cursor()
        #     curr.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        #     curr.close()
        #     dbconn.commit()

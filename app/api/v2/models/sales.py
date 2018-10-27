from datetime import datetime
from ..utils.db_helper import init_db
import psycopg2.extras as extras
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden


class Sales():
    """This class defines the Sales Model and
        the various its methods"""

    def __init__(self, posted_by,  cart_total):
        """Initialize the Sales Model with constructor"""

 
        # self.cart = cart
        self.posted_by = posted_by
        self.cart_total =cart_total
        self.date_created = datetime.now()
        self.date_modified = datetime.now()
        self.db = init_db()

    def post_sale(self):
        """Sale method to make a sale record"""

        new_sale = dict(
            # cart=[],
            posted_by=self.posted_by,
            cart_total=self.cart_total,
            date_created=self.date_created,
            date_modified=self.date_modified
        )
        sql = """INSERT INTO sales (posted_by,cart_total, date_modified,date_created) \
            VALUES ( %(posted_by)s, %(cart_total)s, %(date_modified)s, %(date_created)s);
            """
        # check if sale exists
        if self.check_if_sale_exists(new_sale['posted_by']):
            raise Forbidden(
                "sale already exists.You may Edit or Delete this sale")

        curr = self.db.cursor()


    def check_if_sale_exists(self, posted_by):
        database = self.db
        curr = database.cursor()
        curr.execute(
            "select * from sales where posted_by = (%s);", (posted_by,))
        result = curr.fetchone()
        if result:
            return True

    def get_all(self):
        """This function returns a list of all the sales"""
        dbconn = self.db
        curr = dbconn.cursor(cursor_factory=extras.DictCursor)
        curr.execute("""SELECT * FROM sales;""")
        #returns a python dictionary like interface
        data = curr.fetchall()
        print(data)
        resp = []

        for row in data:
            resp.append(dict(row))
        return resp

    def get_single_sale(self, sale_id):
        """return single sale from the db given an sale_id"""
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        curr.execute(
            "SELECT posted_by,  date_created, sale_id FROM sales WHERE sale_id = (%s);", (sale_id,))
        data = curr.fetchall()
        curr.close()
        resp = []

        for row in data:
            resp.append(dict(row))
        return resp



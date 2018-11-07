from werkzeug.exceptions import NotFound, Forbidden
from ..utils.db_helper import init_db

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

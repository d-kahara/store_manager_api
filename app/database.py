import psycopg2
from instance.config import app_config


class SetupDB(object):
    def __init__(self, config_name):
        #create connection to db
        connection_string = app_config[config_name].DATABASE_URI
        # print(connection_string)
        self.db_connection = psycopg2.connect(connection_string)

        #create cursor
        self.cursor = self.db_connection.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                user_id         SERIAL PRIMARY KEY,
                email           VARCHAR(50) UNIQUE NOT NULL,
                password        VARCHAR(100) UNIQUE NOT NULL,
                role            VARCHAR(50) NOT NULL,
                registered_on   VARCHAR(100) NOT NULL
        );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS blacklist(
                tokens           VARCHAR(500) UNIQUE NOT NULL

        );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products(
                product_id           SERIAL PRIMARY KEY,
                inventory            INTEGER DEFAULT 0,
                min_quantity         INTEGER DEFAULT 0,
                category             VARCHAR(20) NOT NULL,
                date_created         VARCHAR(50) NOT NULL,
                date_modified        VARCHAR(50) NOT NULL,
                product_name         VARCHAR(50) UNIQUE NOT NULL

                );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
                sale_id           SERIAL PRIMARY KEY,
                cart_total            INTEGER DEFAULT 0,
                 date_created         VARCHAR(50) NOT NULL,
                date_modified        VARCHAR(50) NOT NULL,
                posted_by         VARCHAR(50) UNIQUE NOT NULL

                );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS blacklist(

                tokens      VARCHAR(200)   NOT NULL
                );''')

        self.db_connection.commit()
        self.cursor.close()
        self.db_connection.close()

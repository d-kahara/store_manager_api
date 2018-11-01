import os
import psycopg2

from instance.config import app_config

environment = os.environ['APP_SETTINGS']
DATABASE_URI = app_config[environment].DATABASE_URI


def init_db():
    """Open database connections"""
    # conn = psycopg2.connect(DATABASE_URI)
    # return conn

    #create cursor for production on heroku
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

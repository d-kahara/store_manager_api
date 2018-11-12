import os
import psycopg2

from instance.config import app_config

environment = os.environ['FLASK_ENV']
DATABASE_URL = app_config[environment].DATABASE_URL


def init_db():
    """Open database connections"""
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

  
  

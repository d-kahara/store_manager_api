"""Configuration for creating app"""
from flask import Flask

from instance.config import app_config
from app.database import SetupDB


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.app_context().push()
    app.url_map.strict_slashes = False

    #Create database connection and create tables
    db = SetupDB(config_name)
    db.create_tables()

    from .api.v1 import version1 as v1
    app.register_blueprint(v1)

    from .api.v2 import version2 as v2
    app.register_blueprint(v2)

    return app


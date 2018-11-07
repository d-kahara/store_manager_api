"""Configuration for creating app"""
from flask import Flask, jsonify
from flask_cors import CORS

from instance.config import app_config
from app.database import SetupDB


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    CORS(app)

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        return jsonify({"message": "Server error. Contact the admin",
                        "status": 500})

    #Create database connection and create tables
    db = SetupDB(config_name)
    db.create_tables()

    from .api.v1 import version1 as v1
    app.register_blueprint(v1)

    from .api.v2 import version2 as v2
    app.register_blueprint(v2)

    return app


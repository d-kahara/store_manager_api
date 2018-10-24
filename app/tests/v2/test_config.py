import os
import unittest

from flask import current_app
from flask_testing import TestCase

from run import app
from instance.config import app_config


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object(app_config["development"])
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] is 'kaharakey')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object(app_config["testing"])
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] is 'kaharakey')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object(app_config["production"])
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)

import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'kaharakey')
    DEBUG = False


class DevelopmentConfig(Config):
    DATABASE_URI = os.getenv("DATABASE_URI")
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.getenv("DATABASE_TEST_URI")
    PRESERVE_CONTEXT_ON_EXCEPTION = True


class ProductionConfig(Config):
    DEBUG = False


app_config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY

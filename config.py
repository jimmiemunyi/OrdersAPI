import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "development-testing"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH2_CLIENT_ID = os.environ.get("OAUTH2_CLIENT_ID")
    OAUTH2_CLIENT_SECRET = os.environ.get("OAUTH2_CLIENT_SECRET")
    OAUTH2_META_URL = os.environ.get("OAUTH2_META_URL")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("STAGING_DATABASE_URL")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}

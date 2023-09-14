import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def get_env_db_url(env_setting):
    if env_setting == "development":
        SQLALCHEMY_DATABASE_URI = get_env_variable("DEVELOPMENT_DATABASE_URL")
    elif env_setting == "testing":
        SQLALCHEMY_DATABASE_URI = get_env_variable("TESTING_DATABASE_URL")
    elif env_setting == "production":
        SQLALCHEMY_DATABASE_URI = get_env_variable("PRODUCTION_DATABASE_URL")

    return SQLALCHEMY_DATABASE_URI


# DB URLS for each Environment
DEV_DB_URL = get_env_db_url("development")
PROD_DB_URL = get_env_db_url("production")


class Config(object):
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    CONFIG_MODE = get_env_variable("CONFIG_MODE")
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SECRET_KEY = get_env_variable("SECRET_KEY") or "development-testing"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH2_CLIENT_ID = get_env_variable("OAUTH2_CLIENT_ID")
    OAUTH2_CLIENT_SECRET = get_env_variable("OAUTH2_CLIENT_SECRET")
    OAUTH2_META_URL = get_env_variable("OAUTH2_META_URL")
    AFRICASTALKING_USERNAME = get_env_variable("AFRICASTALKING_USERNAME")
    AFRICASTALKING_API_KEY = get_env_variable("AFRICASTALKING_API_KEY")
    AFRICASTALKING_SENDER_ID = get_env_variable("AFRICASTALKING_SENDER_ID")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://"
    )

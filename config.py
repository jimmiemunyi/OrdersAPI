import os

class Config(object):
    # to be removed from production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development-testing'
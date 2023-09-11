import os

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


config_mode = os.environ.get("CONFIG_MODE")
app = Flask(__name__)
app.config.from_object(config[config_mode])
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from backend import routes, models  # code inserted after app Object is created

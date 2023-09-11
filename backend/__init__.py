import os

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

config_mode = os.environ.get("CONFIG_MODE")

app = Flask(__name__)
app.config.from_object(config[config_mode])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

oauth = OAuth(app)
orders_api_auth = oauth.register(
    name="OrdersAPI",
    client_id=app.config.get("OAUTH2_CLIENT_ID"),
    client_secret=app.config.get("OAUTH2_CLIENT_SECRET"),
    server_metadata_url=app.config.get("OAUTH2_META_URL"),
    client_kwargs={
        "scope": "openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/user.phonenumbers.read https://www.googleapis.com/auth/userinfo.email",
    },
)


from backend import routes, models  # code inserted after app Object is created

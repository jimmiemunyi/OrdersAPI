import os
import logging

import africastalking
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from flasgger import Swagger

from config import DevelopmentConfig, ProductionConfig

db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()
swagger = Swagger()


def create_app(config=DevelopmentConfig):
    # use ProductionConfig if we are in production mode
    if os.environ.get("CONFIG_MODE") == "production":
        config = ProductionConfig

    app = Flask(__name__)
    app.config.from_object(config)

    # initializing
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    swagger.init_app(app)

    app.orders_api_auth = oauth.register(
        name="OrdersAPI",
        client_id=app.config.get("OAUTH2_CLIENT_ID"),
        client_secret=app.config.get("OAUTH2_CLIENT_SECRET"),
        server_metadata_url=app.config.get("OAUTH2_META_URL"),
        client_kwargs={
            "scope": "openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/user.phonenumbers.read https://www.googleapis.com/auth/userinfo.email",
        },
    )

    africastalking.initialize(
        username=app.config.get("AFRICASTALKING_USERNAME"),
        api_key=app.config.get("AFRICASTALKING_API_KEY"),
    )
    app.sms_service = africastalking.SMS

    if not app.debug and not app.testing:
        if app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)

    # register the blueprint
    from .routes import bp

    app.register_blueprint(bp)

    return app


from backend import routes, models  # code inserted after app Object is created

import africastalking
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)

    # initializing
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

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

    # register the blueprint
    from .routes import bp

    app.register_blueprint(bp)

    return app


from backend import routes, models  # code inserted after app Object is created

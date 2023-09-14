import pytest

from backend import create_app, db
from config import Config


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://testuser:testpass@localhost:5432/orders_api_db_test"
    )


@pytest.fixture(scope="function")
def app():
    """An application for running tests"""
    _app = create_app(TestingConfig)

    with _app.app_context():
        # always starting with an empty DB
        db.drop_all()
        from backend.models import Order, Customer

        db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app
    db.session.remove()
    if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        db.drop_all()
    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


# @pytest.fixture(scope="function")
# def database(app):
#     return app.db


# @pytest.fixture(scope="function")
# def testapp(app):
#     return TestApp(app)

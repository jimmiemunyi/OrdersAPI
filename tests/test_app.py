from flask import current_app


def test_testing_config(app):
    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"]


def test_app(app):
    assert app is not None
    assert current_app == app

from flask import current_app


def test_testing_config(app):
    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"]


def test_app(app):
    assert app is not None
    assert current_app == app


def test_login(client):
    response = client.get("/login")

    assert response is not None
    assert response.status_code == 302  # redirecting
    assert (
        "<p>You should be redirected automatically to the target URL:" in response.text
    )

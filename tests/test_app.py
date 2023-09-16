from flask import current_app


def test_testing_config(app):
    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"]


def test_app(app):
    assert app is not None
    assert current_app == app


# def test_login(client):
#     response = client.get("/login")

#     assert response is not None
#     assert response.status_code == 302  # redirecting
#     assert (
#         "<p>You should be redirected automatically to the target URL:" in response.text
#     )


def test_logout(client):
    # we have to be logged in
    with client.session_transaction() as session:
        session["user"] = {
            "personData": {
                "phoneNumbers": [
                    {
                        "canonicalForm": "+254712345678",
                    }
                ],
            },
            "userinfo": {
                "email": "dummyname@email.com",
                "name": "dummy name",
            },
        }

    response = client.get("/logout")
    assert response is not None
    assert response.status_code == 302  # redirecting
    assert (
        "<p>You should be redirected automatically to the target URL:" in response.text
    )

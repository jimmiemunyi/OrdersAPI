# from flask import url_for, request
import json

from backend.models import Customer, Order
from backend import db


def test_index(client):
    # data = {"name": "dummy name", "email": "dummy@email.com", "contact": "contact"}
    response = client.get("/")

    assert response is not None
    assert response.status_code == 200
    assert "<title>Home - Orders API</title>" in response.text


def test_index_logged_in(client):
    # assume we have the following session from logged in user
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

    response = client.get("/")

    assert response is not None
    assert response.status_code == 200
    assert "dummy name" in response.text


def test_update_customer_form(client):
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

    data = {
        "name": "dummy name",
        "email": "dummyname@dummy.com",
        "contact": "+254712345678",
    }
    headers = {"Content-Type": "application/json"}
    response = client.post("/", data=json.dumps(data), headers=headers)

    assert response is not None
    assert response.status_code == 302
    assert (
        "<p>You should be redirected automatically to the target URL:" in response.text
    )


def test_update_order_form(client):
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
    db.session.add(c)
    db.session.commit()
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
                "email": "dummy@dummy.com",
                "name": "dummy name",
            },
        }

    data = {
        "item": "dummy item",
        "amount": 100,
    }
    headers = {"Content-Type": "application/json"}
    response = client.post("/orders", data=json.dumps(data), headers=headers)

    assert response is not None
    assert response.status_code == 302
    assert (
        "<p>You should be redirected automatically to the target URL:" in response.text
    )


def test_orders(client):
    response = client.get("/orders")

    assert response is not None
    assert "<title>Orders - Orders API</title>" in response.text


def test_get_customers(client):
    # dummy customer
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
    # add to database
    db.session.add(c)
    db.session.commit()

    response = client.get("/api/v1/customers")
    response_1 = client.get(f"/api/v1/customers/{1}")

    assert response is not None
    # assert that the database has only 1 record
    assert db.session.query(Customer).one()
    # assert that the record name is the one we inserted
    assert db.session.query(Customer).one().name == c.name
    assert c.name in response_1.text


def test_post_customers(client):
    data = {"name": "dummy name", "email": "dummy@email.com", "contact": "contact"}
    headers = {"Content-Type": "application/json"}

    response = client.post("/api/v1/customers", data=json.dumps(data), headers=headers)
    response_2 = client.post("/api/v1/customers", data=json.dumps({}), headers=headers)
    response_3 = client.post(
        "/api/v1/customers",
        data=json.dumps({"name": "dummy name", "email": "dummy@email.com"}),
        headers=headers,
    )

    assert response is not None
    assert response.status_code == 201
    assert data["name"] in response.text

    assert response_2 is not None
    assert response_2.status_code == 400
    assert "No data provided!" in response_2.text

    assert response_3 is not None
    assert response_3.status_code == 400
    assert "Missing contact field in the data provided!" in response_3.text


def test_put_customers(client):
    # dummy customer
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
    # add to database
    db.session.add(c)
    db.session.commit()

    # attempt to update the record
    data = {"name": "new name", "email": "new@email.com", "contact": "new contact"}
    headers = {"Content-Type": "application/json"}

    response = client.put(
        f"/api/v1/customers/{1}", data=json.dumps(data), headers=headers
    )
    response_2 = client.put(
        f"/api/v1/customers/{2}", data=json.dumps(data), headers=headers
    )
    response_3 = client.put(
        f"/api/v1/customers/{2}", data=json.dumps({}), headers=headers
    )
    response_4 = client.put(
        f"/api/v1/customers/{2}",
        data=json.dumps(
            {
                "name": "new name",
                "email": "new@email.com",
            }
        ),
        headers=headers,
    )

    assert response is not None
    assert response.status_code == 201
    assert data["name"] in response.text

    assert response_2 is not None
    assert response_2.status_code == 404
    assert "Customer not found" in response_2.text

    assert response_3 is not None
    assert response_3.status_code == 400
    assert "No data provided!" in response_3.text

    assert response_4 is not None
    assert response_4.status_code == 400
    assert "Missing contact field in the data provided!" in response_4.text


def test_delete_customers(client):
    # dummy customer
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
    # add to database
    db.session.add(c)
    db.session.commit()

    response = client.delete(f"/api/v1/customers/{1}")
    response_2 = client.delete(f"/api/v1/customers/{2}")

    assert response is not None
    assert response.status_code == 201
    assert "Customer deleted" in response.text

    assert response_2 is not None
    assert response_2.status_code == 404
    assert "Customer not found" in response_2.text


def test_get_orders(client):
    # dummy customer
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
    o = Order(customer=c, item="dummy item", amount=100)
    # add to database
    db.session.add(c)
    db.session.add(o)

    db.session.commit()

    response = client.get("/api/v1/orders")
    response_1 = client.get(f"/api/v1/orders/{1}")
    response_2 = client.get(f"/api/v1/orders/{2}")

    assert response is not None
    # # assert that the database has only 1 record
    assert db.session.query(Order).one()
    # # assert that the order record is by our dummy customer
    assert db.session.query(Order).one().customer_id == c.id
    assert "dummy item" in response_1.text
    assert response_2.status_code == 404


def test_post_orders(client):
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")

    db.session.add(c)
    db.session.commit()

    data = {"customer_id": c.id, "item": "dummy item", "amount": 100}
    headers = {"Content-Type": "application/json"}

    response = client.post("/api/v1/orders", data=json.dumps(data), headers=headers)

    # empty
    response_2 = client.post("/api/v1/orders", data=json.dumps({}), headers=headers)

    # missing some parts
    response_3 = client.post(
        "/api/v1/orders",
        data=json.dumps({"customer_id": c.id, "item": "dummy item"}),
        headers=headers,
    )

    assert response is not None
    assert response.status_code == 201
    assert data["item"] in response.text

    assert response_2 is not None
    assert response_2.status_code == 400
    assert "No data provided" in response_2.text

    assert response_3 is not None
    assert response_3.status_code == 400
    assert "Missing name field in the data provided!" in response_3.text


def test_put_orders(client):
    # dummy customer
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
    o = Order(customer=c, item="dummy item", amount=100)
    # add to database
    db.session.add(c)
    db.session.add(o)

    db.session.commit()

    # attempt to update the record
    data = {"customer_id": c.id, "item": "dummy item 2", "amount": 500}
    headers = {"Content-Type": "application/json"}

    response = client.put(f"/api/v1/orders/{1}", data=json.dumps(data), headers=headers)
    response_2 = client.put(
        f"/api/v1/orders/{2}", data=json.dumps(data), headers=headers
    )

    # empty data
    response_3 = client.put(f"/api/v1/orders/{1}", data=json.dumps({}), headers=headers)

    assert response is not None
    assert response.status_code == 201
    assert data["item"] in response.text

    assert response_2 is not None
    assert response_2.status_code == 404
    assert "Order not found" in response_2.text

    assert response_3 is not None
    assert response_3.status_code == 400
    assert "No data provided!" in response_3.text


def test_delete_orders(client):
    # dummy customer
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
    o = Order(customer=c, item="dummy item", amount=100)
    # add to database
    db.session.add(c)
    db.session.add(o)

    db.session.commit()

    response = client.delete(f"/api/v1/orders/{1}")

    # try for an order that doesn't exist
    response_2 = client.delete(f"/api/v1/orders/{2}")

    assert response is not None
    assert response.status_code == 200
    assert "Order deleted" in response.text

    assert response_2 is not None
    assert response_2.status_code == 404
    assert "Order not found" in response_2.text


def test_not_found(client):
    # dummy customer
    c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
    # add to database
    db.session.add(c)
    db.session.commit()

    # attempt to get a different record
    response = client.get(f"/api/v1/customers/{2}")

    assert response is not None
    assert response.status_code == 404
    assert "Not Found" in response.text

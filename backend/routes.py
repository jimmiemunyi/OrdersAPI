import json
import requests

from flask import (
    render_template,
    make_response,
    jsonify,
    abort,
    request,
    url_for,
    session,
    redirect,
)

from backend import app, db, orders_api_auth
from backend.models import Customer, Order


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "jimmie"}
    return render_template(
        "index.html",
        title="Home",
        user=user,
        session=session.get("user"),
        pretty=json.dumps(
            session.get("user"),
            indent=4,
        ),
    )


# login + logout endpoints
@app.route("/login")
def login():
    return orders_api_auth.authorize_redirect(
        redirect_uri=url_for("google_callback", _external=True)
    )


@app.route("/google-login")
def google_callback():
    token = orders_api_auth.authorize_access_token()
    personDataUrl = (
        "https://people.googleapis.com/v1/people/me?personFields=phoneNumbers"
    )
    personData = requests.get(
        personDataUrl, headers={"Authorization": f"Bearer {token['access_token']}"}
    ).json()

    token["personData"] = personData  # handle phone numbers
    session["user"] = token

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("index"))


# Customer Endpoints
@app.route("/api/v1/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customer_list = [
        {"id": c.id, "name": c.name, "email": c.email, "contact": c.contact}
        for c in customers
    ]
    return jsonify(customer_list), 201


@app.route("/api/v1/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return (
            jsonify(
                {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "contact": customer.contact,
                }
            ),
            200,
        )
    abort(404)


@app.route("/api/v1/customers", methods=["POST"])
def create_customer():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided!"}), 400
    required_fields = ["name", "email", "contact"]
    for field in required_fields:
        if field not in data:
            return (
                jsonify({"error": f"Missing {field} field in the data provided!"}),
                400,
            )
    customer = {f"{field}": data.get(f"{field}") for field in required_fields}
    new_customer = Customer(
        name=customer["name"], email=customer["email"], contact=customer["contact"]
    )
    db.session.add(new_customer)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_customer.id,
                "name": new_customer.name,
                "email": new_customer.email,
                "contact": new_customer.contact,
            }
        ),
        201,
    )


@app.route("/api/v1/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided!"}), 400
    required_fields = ["name", "email", "contact"]
    for field in required_fields:
        if field not in data:
            return (
                jsonify({"error": f"Missing {field} field in the data provided!"}),
                400,
            )
    customer = Customer.query.get(customer_id)
    if customer:
        customer.name = data["name"]
        customer.email = data["email"]
        customer.contact = data["contact"]
        db.session.commit()
        return (
            jsonify(
                {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "contact": customer.contact,
                }
            ),
            201,
        )
    return jsonify({"message": "Customer not found"}), 404


@app.route("/api/v1/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted"})
    return jsonify({"message": "Customer not found"}), 404


# Order Endpoints
@app.route("/api/v1/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    order_list = [
        {
            "id": o.id,
            "customer_id": o.customer_id,
            "item": o.item,
            "amount": float(o.amount),
            "time": o.time,
        }
        for o in orders
    ]
    return jsonify(order_list), 201


@app.route("/api/v1/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        return jsonify(
            {
                "id": order.id,
                "customer_id": order.customer_id,
                "item": order.item,
                "amount": float(order.amount),
                "time": order.time,
            }
        )
    return abort(404)


@app.route("/api/v1/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided!"}), 400
    if "customer_id" not in data or "item" not in data or "amount" not in data:
        return jsonify({"error": "Missing name field in the data provided!"}), 400
    new_order = Order(
        customer_id=data["customer_id"],
        item=data["item"],
        amount=data["amount"],
    )
    db.session.add(new_order)
    db.session.commit()
    return (
        jsonify(
            {
                "id": new_order.id,
                "customer_id": new_order.customer_id,
                "item": new_order.item,
                "amount": float(new_order.amount),
                "time": new_order.time,
            }
        ),
        201,
    )


@app.route("/api/v1/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided!"}), 400
    order = Order.query.get(order_id)
    if order:
        order.customer_id = data["customer_id"]
        order.item = data["item"]
        order.amount = data["amount"]
        db.session.commit()
        return jsonify(
            {
                "id": order.id,
                "customer_id": order.customer_id,
                "item": order.item,
                "amount": float(order.amount),
                "time": order.updated,
            }
        )
    return jsonify({"message": "Order not found"}), 404


@app.route("/api/v1/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted"})
    return jsonify({"message": "Order not found"}), 404


# Error Endpoints
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)

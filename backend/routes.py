from flask import render_template, make_response, jsonify, abort, request
from backend import app, db
from backend.models import Customer, Order


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "jimmie"}
    return render_template("index.html", title="Home", user=user)


# Customer Endpoints
@app.route("/api/v1/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customer_list = [{"id": c.id, "name": c.name} for c in customers]
    return jsonify(customer_list), 201


@app.route("/api/v1/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return jsonify({"id": customer.id, "name": customer.name}), 200
    abort(404)


@app.route("/api/v1/customers", methods=["POST"])
def create_customer():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided!"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name field in the data provided!"}), 400
    customer = {"name": data.get("name")}
    new_customer = Customer(name=customer["name"])
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"id": new_customer.id, "name": new_customer.name}), 201


@app.route("/api/v1/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided!"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name field in the data provided!"}), 400
    customer = Customer.query.get(customer_id)
    if customer:
        customer.name = data["name"]
        db.session.commit()
        return jsonify({"id": customer.id, "name": customer.name}), 201
    else:
        abort(404)


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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)

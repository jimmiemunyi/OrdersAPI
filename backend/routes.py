from flask import render_template, make_response, jsonify, abort, request
from backend import app, db
from backend.models import Customer, Order


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "jimmie"}
    return render_template("index.html", title="Home", user=user)


# Customer routes
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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)

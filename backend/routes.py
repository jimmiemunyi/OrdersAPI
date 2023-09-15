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
    flash,
    Blueprint,
    current_app,
)

from backend import db
from backend.models import Customer, Order
from backend.forms import UpdateCustomerForm, MakeOrderForm

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    sesison_info = session.get("user")
    if sesison_info:  # logged in users.
        name = sesison_info["userinfo"]["name"]
        email = sesison_info["userinfo"]["email"]
        contact = "NULL"  # default if we cannot extract the contact from Google
        if "phoneNumbers" in sesison_info["personData"]:
            # attempt to extract contact from Google
            contact = sesison_info["personData"]["phoneNumbers"][0]["canonicalForm"]
            contact = contact.split("+")[-1]

        # database logic
        customer = Customer.query.filter_by(email=email).first()
        if not customer:
            customer = Customer(name=name, email=email, contact=contact)
            db.session.add(customer)
            db.session.commit()

        # update customer
        form = UpdateCustomerForm()
        if form.validate_on_submit():
            # Extract form data
            name = form.name.data
            email = form.email.data
            contact = form.contact.data

            # send PUT request to our API to update the data
            data = {"name": name, "email": email, "contact": contact}
            headers = {"Content-Type": "application/json"}
            response = requests.put(
                f'{url_for("main.update_customer", customer_id=customer.id, _external=True)}',
                data=json.dumps(data),
                headers=headers,
            )
            if response.status_code == 201:
                flash("Records updated successfully")
            else:
                flash("Failed to update customer", category="danger")

            return redirect(url_for("main.index"))

        return render_template(
            "index.html",
            title="Home",
            session=sesison_info,
            customer=customer,
            form=form,
        )
    return render_template("index.html", title="Home", session=sesison_info)


# login + logout endpoints
@bp.route("/login")
def login():
    return current_app.orders_api_auth.authorize_redirect(
        redirect_uri=url_for("main.google_callback", _external=True)
    )


@bp.route("/google-login")
def google_callback():
    token = current_app.orders_api_auth.authorize_access_token()
    personDataUrl = (
        "https://people.googleapis.com/v1/people/me?personFields=phoneNumbers"
    )
    personData = requests.get(
        personDataUrl, headers={"Authorization": f"Bearer {token['access_token']}"}
    ).json()

    token["personData"] = personData  # contacts from Google are located in personData
    session["user"] = token

    return redirect(url_for("main.index"))


@bp.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("main.index"))


@bp.route("/orders", methods=["GET", "POST"])
def orders():
    sesison_info = session.get("user")
    if sesison_info:
        email = sesison_info["userinfo"]["email"]
        customer = Customer.query.filter_by(email=email).first()
        orders = Order.query.filter_by(customer_id=customer.id).all()

        form = MakeOrderForm()
        if form.validate_on_submit():
            # Extract form data
            item = form.item.data
            amount = round(float(form.amount.data), 2)

            # send PUT request to our API to update the data
            data = {"customer_id": customer.id, "item": item, "amount": amount}
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                f'{url_for("main.create_order", _external=True)}',
                data=json.dumps(data),
                headers=headers,
            )
            if response.status_code == 201:
                flash("Order made successfully")
                # try and send the order confirmation SMS
                try:
                    message = f"Thank you {customer.name} for making an order of {item} for amount Ksh.{amount}"
                    contact = f"+{customer.contact}"
                    sender = current_app.config.get("AFRICASTALKING_SENDER_ID")
                    response = current_app.sms_service.send(message, [contact], sender)
                    print(f"[MESSAGE RESPONSE]: {response}")
                except Exception as e:
                    print(f"[MESSAGE ERROR]: {e}")

            else:
                flash("Failed to make order", category="danger")

            return redirect(url_for("main.orders"))

        return render_template(
            "orders.html",
            title="Orders",
            session=sesison_info,
            orders=orders,
            form=form,
        )

    return render_template("orders.html", title="Orders", session=sesison_info)


# API Endpoints
# Customer Endpoints
@bp.route("/api/v1/customers", methods=["GET"])
def get_customers():
    """Get all customers present in the database
    Specifications
    ---
    responses:
      201:
        description: Data for all the customers
    """
    customers = Customer.query.all()
    customer_list = [
        {"id": c.id, "name": c.name, "email": c.email, "contact": c.contact}
        for c in customers
    ]
    return jsonify(customer_list), 201


@bp.route("/api/v1/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Get a specific customer from database
    Specifications
    ---
    parameters:
      - name: customer_id
        in: customer id
        type: int
        required: true
    responses:
      200:
        description: Data for the customer requested
      404:
        description: Customer does not exist in the database
    """
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


@bp.route("/api/v1/customers", methods=["POST"])
def create_customer():
    """Create a customer in the database
    Specifications
    ---
    parameters:
      - name: data
        description: data for the customer
        in: data
        type: json
        required: true
    responses:
      200:
        description: Data for the customer created
      400:
        description: Missing some fields in the data you provided
    """
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


@bp.route("/api/v1/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Update a customer in the database
    Specifications
    ---
    parameters:
      - name: customer_id
        description: id for the customer to update
        in: customer_id
        type: int
        required: true
      - name: data
        description: data for the customer
        in: data
        type: json
        required: true
    responses:
      200:
        description: Data for the customer updated
      400:
        description:  Missing some fields in the data you provided
    """
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


@bp.route("/api/v1/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Delete a customer in the database
    Specifications
    ---
    parameters:
      - name: customer_id
        description: id for the customer to delete
        in: data
        type: int
        required: true
    responses:
      201:
        description: Customer deleted
      400:
        description: Customer not found
    """
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted"}), 201
    return jsonify({"message": "Customer not found"}), 404


# Order Endpoints
@bp.route("/api/v1/orders", methods=["GET"])
def get_orders():
    """Get all customers present in the database
    Specifications
    ---
    responses:
      201:
        description: Data for all the orders
    """
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


@bp.route("/api/v1/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Get a specific order from database
    Specifications
    ---
    parameters:
      - name: order_id
        in: order id
        type: int
        required: true
    responses:
      200:
        description: Data for the order requested
      404:
        description: Order does not exist in the database
    """
    order = Order.query.get(order_id)
    if order:
        return (
            jsonify(
                {
                    "id": order.id,
                    "customer_id": order.customer_id,
                    "item": order.item,
                    "amount": float(order.amount),
                    "time": order.time,
                }
            ),
            200,
        )
    return abort(404)


@bp.route("/api/v1/orders", methods=["POST"])
def create_order():
    """Create an order in the database
    Specifications
    ---
    parameters:
      - name: data
        description: data for the order
        in: data
        type: json
        required: true
    responses:
      201:
        description: Data for the order created
      400:
        description: Missing some fields in the data you provided
    """
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


@bp.route("/api/v1/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    """Update an order in the database
    Specifications
    ---
    parameters:
      - name: order_id
        description: id for the order to update
        in: order_id
        type: int
        required: true
      - name: data
        description: data for the order
        in: data
        type: json
        required: true
    responses:
      200:
        description: Data for the order updated
      400:
        description:  Missing some fields in the data you provided
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided!"}), 400
    order = Order.query.get(order_id)
    if order:
        order.customer_id = data["customer_id"]
        order.item = data["item"]
        order.amount = data["amount"]
        db.session.commit()
        return (
            jsonify(
                {
                    "id": order.id,
                    "customer_id": order.customer_id,
                    "item": order.item,
                    "amount": float(order.amount),
                    "time": order.updated,
                }
            ),
            201,
        )
    return jsonify({"message": "Order not found"}), 404


@bp.route("/api/v1/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    """Delete an order in the database
    Specifications
    ---
    parameters:
      - name: order_id
        description: id for the customer to delete
        in: data
        type: int
        required: true
    responses:
      201:
        description: Order deleted
      400:
        description: Order not found
    """
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted"}), 200
    return jsonify({"message": "Order not found"}), 404


# Error Endpoints
@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)

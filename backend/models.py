from backend import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Define a relationship with orders
    orders = db.relationship("Order", backref="customer", lazy="dynamic")

    def __repr__(self):
        return f"<Customer {self.name}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    item = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(
        db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # The Date of the Instance Update => Changed with Every Update

    def __repr__(self):
        return f"<Order {self.item} by Customer {self.customer}>"

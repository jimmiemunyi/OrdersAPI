from backend.models import Order, Customer
from backend import db


def test_models(app):
    with app.app_context():
        c = Customer(name="dummy name", email="dummy@dummy.com", contact="contact")
        o = Order(customer=c, item="dummy item", amount=100)
        # add to database
        db.session.add(c)
        db.session.add(o)

        db.session.commit()

        assert "dummy name" in repr(c)
        assert "dummy item" in repr(o)

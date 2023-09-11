from backend import app, db
from backend.models import Customer, Order


# make them available in the Shell
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Customer": Customer, "Order": Order}

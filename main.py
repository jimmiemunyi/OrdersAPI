from backend import db, create_app
from backend.models import Customer, Order


app = create_app()


# make them available in the Shell
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Customer": Customer, "Order": Order}

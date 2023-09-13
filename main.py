import os

from config import config
from backend import db, create_app
from backend.models import Customer, Order

configuration = config[os.environ.get("CONFIG_MODE")]
app = create_app(config=configuration)


# make them available in the Shell
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Customer": Customer, "Order": Order}

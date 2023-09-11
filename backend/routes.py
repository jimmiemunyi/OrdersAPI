from flask import render_template
from backend import app


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "jimmie"}
    return render_template("index.html", title="Home", user=user)

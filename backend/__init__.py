from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from backend import routes # routes inserted after app Object is created
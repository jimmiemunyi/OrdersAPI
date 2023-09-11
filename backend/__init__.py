from flask import Flask

app = Flask(__name__)

from backend import routes # to circumnavigate the circular imports

from flask import Flask
from flask_cors import CORS

from lib.db import setup_app


app = Flask(__name__)

CORS(app)

setup_app(app)


# include Blueprints

from products import blueprint as products_bp
from transactions import blueprint as transactions_bp

# register blueprints

app.register_blueprint(products_bp)
app.register_blueprint(transactions_bp)


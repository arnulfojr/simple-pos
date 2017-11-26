
from flask import Flask


app = Flask(__name__)


# import controllers

from controllers import index
from controllers import products
from controllers import transactions

# import blueprints

# register blueprints


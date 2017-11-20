
from flask import Blueprint

blueprint = Blueprint('products', __name__, url_prefix='/products')

# import controllers
from controllers import products


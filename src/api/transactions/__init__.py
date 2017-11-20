
from flask import Blueprint

blueprint = Blueprint('transactions', __name__, url_prefix='/transactions')

# import controllers
from controllers import transactions


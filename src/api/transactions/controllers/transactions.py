
from flask import request, make_response, jsonify
from cerberus import Validator

from core.transactions import Transaction

from lib.request import is_json
from lib.db import session

from .. import blueprint


@blueprint.route('/', methods=['GET'])
def get_transactions():
    delivered = request.args.get('delivered', 'true') == 'true'
    query = session.query(Transaction)
    
    if delivered is not None:
        query = query.filter(Transaction.delivered == delivered)

    transactions = query.all()


    payload = [transaction.to_json() for transaction in transactions]

    return make_response(jsonify(payload), 200)


@blueprint.route('/<uuid:code>/', methods=['GET'])
def get_sale(code):
    transaction = Transaction.get(code)

    if transaction is None:
        return make_response(jsonify({'errors': ['No transaction found']}), 404)

    payload = transaction.to_json()

    return make_response(jsonify(payload), 200)


@blueprint.route('/', methods=['POST'])
@is_json
def save_transaction():
    validator = Validator(Transaction.schema)

    payload = request.get_json()

    if not validator.validate(payload):
        return make_response(jsonify(validator.errors), 400)

    transaction = Transaction.from_json(payload)

    session.add(transaction)

    session.commit()

    session.flush()

    return make_response(jsonify(transaction.to_json()), 201)


@blueprint.route('/<uuid:code>/', methods=['PUT'])
@is_json
def update_transaction(code):
    validator = Validator(Transaction.schema)

    payload = request.get_json()

    if not validator.validate(payload):
        return make_response(jsonify(validator.errors), 400)

    transaction = Transaction.get(code)

    transaction = Transaction.from_json(payload, transaction)

    session.add(transaction)
    session.commit()
    session.flush()

    return make_response(jsonify(transaction.to_json()), 200)


@blueprint.route('/<uuid:code>/deliver/', methods=['PUT'])
def deliver_transaction(code):
    transaction = Transaction.get(code)

    transaction.delivered = True

    session.add(transaction)
    session.commit()
    session.flush()

    return make_response(jsonify(transaction.to_json()), 200)


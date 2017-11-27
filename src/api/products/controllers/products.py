
from flask import request, make_response, jsonify
from cerberus import Validator

from .. import blueprint

from lib.request import is_json
from lib.db import session
from core.products import Product


@blueprint.route('/', methods=['GET'])
def get_products():
    """Returns all products from DB"""
    available = request.args.get('available', None)

    products = Product.find_all(available=available)

    payload = [product.to_json() for product in products]

    response = make_response(jsonify(payload), 200)

    return response


@blueprint.route('/<uuid:code>/', methods=['GET'])
def get_product(code):
    product = Product.get(code)

    code = 200

    if product is None:
        payload = {'errors': ['No product was found for {}'.format(str(code))]}
        code = 404
    else:
        payload = product.to_json()

    response = make_response(jsonify(payload), code)

    return response


@blueprint.route('/', methods=['POST'])
@is_json
def register_product():
    """Registers the product in the database"""
    payload = request.get_json()

    validator = Validator(Product.schema)

    if not validator.validate(payload):
        return make_response(jsonify(validator.errors), 400)

    product = Product.from_json(payload)

    session.add(product)

    session.commit()

    session.flush()

    payload = product.to_json()

    return make_response(jsonify(payload), 201)


@blueprint.route('/<uuid:code>/', methods=['PUT'])
@is_json
def update_product(code):
    """Updates the Product"""

    payload = request.get_json()

    validator = Validator(Product.schema)

    if not validator.validate(payload):
        return make_response(jsonify(validator.errors), 400)

    product = Product.get(code)

    if product is None:
        return make_response(jsonify({'errors': ['No product was found with {}'.format(code)]}), 404)

    product = Product.from_json(payload, product)

    session.add(product)

    session.commit()

    session.flush()

    return make_response(jsonify(product.to_json()), 200)


@blueprint.route('/<uuid:code>/', methods=['DELETE'])
def deactivate_product(code):
    product = Product.get(code)

    if product is None:
        return make_response(jsonify({'errors': ['No product was found with {}'.format(code)]}), 404)

    session.delete(product)

    session.commit()

    session.flush()

    return make_response(jsonify({'message': 'Product was deleted'}), 200)


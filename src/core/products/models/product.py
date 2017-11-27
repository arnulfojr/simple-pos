
import pendulum
from uuid import uuid4

from sqlalchemy import Column, func
from sqlalchemy import DateTime, String, Integer, Numeric, Boolean

from lib.db import Model, MixinModel, session
from lib.db.types import GUID
from lib.utils.cerberus.coercers import datetime_coercer


class Product(MixinModel, Model):
    """Product in the inventory"""

    __tablename__ = 'products'

    code = Column(GUID, primary_key=True, nullable=False, default=uuid4)

    sku = Column(String, nullable=True)

    name = Column(String, nullable=False)

    description = Column(String, nullable=True, default='No description')

    # Availability of the product
    available = Column(Boolean, nullable=False, default=True)

    price = Column(Numeric(10, 2), nullable=False)

    registered_on = Column(DateTime, server_default=func.now())

    # Schema to validate the incoming product
    schema = {
        'sku': {
            'type': 'string',
            'empty': False,
            'required': False
        },
        'name': {
            'type': 'string',
            'empty': False,
            'required': True
        },
        'description': {
            'type': 'string',
            'required': False,
            'empty': True
        },
        'available': {
            'type': 'boolean',
            'required': False,
            'empty': False
        },
        'price': {
            'type': 'float',
            'required': True,
            'empty': False
        },
        'code': {
            'type': 'string',
            'required': False,
            'empty': False
        },
        'registered_on': {
            'type': 'datetime',
            'required': False,
            'empty': False,
            'coerce': datetime_coercer
        }
    }


    @classmethod
    def find_all(cls, available=None):
        query = session.query(cls)

        if available is not None:
            query = query.filter(cls.available == available)

        return query.all()


    @classmethod
    def from_json(cls, json, product=None):
        if product is None:
            product = cls()

        product.name = json['name']
        product.price = json['price']

        if 'sku' in json:
            product.sku = json['sku']
        if 'description' in json:
            product.description = json['description']
        if 'available' in json:
            product.available = json['available']

        return product


    def to_json(self):
        """Returns the product in a seriable JSON friendly way"""
        product = {}

        product['code'] = self.code
        product['sku'] = self.sku
        product['name'] = self.name
        product['description'] = self.description
        product['available'] = self.available
        product['price'] = float(self.price)
        product['registered_on'] = pendulum.instance(self.registered_on).to_iso8601_string()

        return product



import pendulum

from uuid import uuid4
from decimal import Decimal

from sqlalchemy import Column, func
from sqlalchemy import DateTime, String, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from lib.db import Model, MixinModel
from lib.db.types import GUID
from lib.utils.cerberus.coercers import datetime_coercer

from items import Item
from core.products import Product


class Transaction(MixinModel, Model):
    """Transaction Entity"""

    __tablename__ = 'transactions'

    code = Column(GUID, primary_key=True, nullable=False, default=uuid4)

    number = Column(Integer, autoincrement=True, unique=True, nullable=True)

    registered_on = Column(DateTime, server_default=func.now())

    delivered = Column(Boolean, default=False)

    tax = Column(Numeric(10, 2), nullable=False, default=19.0)

    total = Column(Numeric(10, 2), nullable=False)

    items = relationship('Item', back_populates='transaction')

    schema = {
        'tax': {
            'type': 'float',
            'required': False,
            'empty': False
        },
        'delivered': {
            'type': 'boolean',
            'required': True,
            'empty': False
        },
        'items': {
            'type': 'list',
            'required': True,
            'empty': False,
            'schema': Item.schema
        },
        'total': {
            'type': 'float',
            'required': False,
            'empty': False
        },
        'registered_on': {
            'type': 'datetime',
            'required': False,
            'empty': False,
            'coerce': datetime_coercer
        },
        'code': {
            'type': 'string',
            'required': False,
            'empty': False
        },
        'number': {
            'type': 'integer',
            'required': False,
            'empty': False
        }
    }

    @classmethod
    def from_json(cls, json, transaction=None):
        if transaction is None:
            transaction = cls()

        total = Decimal(0.0)
        items = []

        for raw_item in json['items']:
            item = Item.from_json(raw_item)
            total = total + item.total
            items.append(item)

        transaction.total = total
        transaction.items = items
        transaction.delivered = json['delivered']

        if 'tax' in json:
            transaction.tax = json['tax']

        return transaction

    def to_json(self):
        json = {}

        json['code'] = self.code
        json['number'] = self.number
        json['registered_on'] = pendulum.instance(self.registered_on).to_iso8601_string()
        json['delivered'] = self.delivered
        json['tax'] = float(self.tax)
        json['total'] = float(self.total)
        json['items'] = [item.to_json() for item in self.items]

        return json


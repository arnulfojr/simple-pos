
from uuid import uuid4
from decimal import Decimal

from sqlalchemy import Column, func
from sqlalchemy import DateTime, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from lib.db import Model, MixinModel
from lib.db.types import GUID

from items import Item
from core.products import Product


class Transaction(MixinModel, Model):
    """Transaction Entity"""

    __tablename__ = 'transactions'

    code = Column(GUID, primary_key=True, nullable=False, default=uuid4)

    registered_on = Column(DateTime, server_default=func.now())

    tax = Column(Numeric(10, 2), nullable=False, default=19.0)

    total = Column(Numeric(10, 2), nullable=False)

    items = relationship('Item', back_populates='transaction')

    schema = {
        'tax': {
            'type': 'float',
            'required': False,
            'empty': False
        },
        'items': {
            'type': 'list',
            'required': True,
            'empty': False,
            'schema': Item.schema
        }
    }

    @classmethod
    def from_json(cls, json):
        transaction = cls()

        total = Decimal(0.0)
        items = []

        for raw_item in json['items']:
            item = Item.from_json(raw_item)
            total = total + item.total
            items.append(item)

        transaction.total = total
        transaction.items = items

        return transaction

    def to_json(self):
        json = {}

        json['code'] = self.code
        json['registered_on'] = self.registered_on.isoformat()
        json['tax'] = float(self.tax)
        json['total'] = float(self.total)
        json['items'] = [item.to_json() for item in self.items]

        return json


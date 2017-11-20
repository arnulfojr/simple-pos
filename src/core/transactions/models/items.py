
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from lib.db import Model
from lib.db.types import GUID

from core.products import Product


class Item(Model):
    """Transaction Item"""
    __tablename__ = 'transaction_items'

    code = Column(GUID, primary_key=True, nullable=False, default=uuid4)

    transaction = relationship('Transaction', back_populates='items')
    transaction_code = Column(GUID, ForeignKey('transactions.code'))

    quantity = Column(Integer, nullable=False, default=1)

    total = Column(Numeric(10, 2), nullable=False)

    product = relationship('Product')
    product_code = Column(GUID, ForeignKey('products.code'))

    schema = {
        'quantity': {
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'product': {
            'type': 'dict',
            'required': True,
            'empty': False,
            'allow_unknown': True,
            'schema': {
                'code': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                }
            }
        }
    }


    @classmethod
    def from_json(cls, json):
        item = cls()

        item.quantity = json['quantity']

        product = Product.get(json['product']['code'])
        item.product = product

        item.total = product.price * item.quantity

        return item

    def to_json(self, transaction=False, product=True):
        json = {}

        json['code'] = self.code
        json['quantity'] = self.quantity
        json['total'] = float(self.total)
        
        if transaction:
            json['transaction'] = self.transaction.to_json()
        
        if product:
            json['product'] = self.product.to_json()

        return json


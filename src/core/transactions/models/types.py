
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship

from lib.db import MixinModel, Model


class Type(MixinModel, Model):
    """Transaction Type"""

    __tablename__ = 'transaction_type'

    name = Column(String, primary_key=True, nullable=False)

    multiplier = Column(Integer, nullable=False, default=1)

    transactions = relationship('Transaction', back_populates='type')

    registered_on = Column(DateTime, nullable=False, server_default=func.now())

    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'multiplier': {
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'registered_on': {
            'type': 'datetime',
            'required': False,
            'empty': True
        }
    }


    @classmethod
    def from_json(cls, json, instance=None):
        if instance is None:
            instance = cls()

        instance.name = json['name']
        instance.multiplier = json['multiplier']

        return instance
        
    def to_json(self):
        json = {}

        json['name'] = self.name
        json['multiplier'] = self.multiplier
        json['registered_on'] = self.registered_on.isoformat()

        return json


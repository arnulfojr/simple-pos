
from .. import Model
from .. import engine


def drop_all():
    """Drop all Tables attached to the model"""
    Model.metadata.drop_all(engine)


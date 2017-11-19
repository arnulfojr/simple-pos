
from .. import engine
from .. import Model


def create_all():
    """
    Creates the schema for the models
    """
    Model.metadata.create_all(engine)


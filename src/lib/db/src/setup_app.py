
from .. import session


def setup_app(app):
    """Set up SQLAlchemy to work with Flask"""
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()


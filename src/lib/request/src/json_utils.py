
from functools import wraps

from flask import request, abort


def is_json(fn):
    """
    Validates the request to have a JSON Body, else aborts with 400

    Usage:
    @blueprint.route(...)
    @is_json
    def some_handler():
        pass

    """
    @wraps(fn)
    def _wrap(*args, **kwargs):
        if not request.is_json:
            abort(400)
        return fn(*args, **kwargs)
    return _wrap


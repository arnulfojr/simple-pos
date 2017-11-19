
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask import Flask

from settings import HOSTNAME, PORT, USE_RELOADER, USE_DEBUGGER


app = Flask(__name__)

application = DispatcherMiddleware(app, {})


if __name__ == '__main__':
    run_simple(HOSTNAME, PORT, application,
            use_reloader=USE_RELOADER, use_debugger=USE_DEBUGGER)


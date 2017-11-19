
import os

from db import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_ECHO, DB_URI


PORT = os.getenv('PORT', 5000)

HOSTNAME = os.getenv('HOST', '0.0.0.0')

IS_DEV = os.getenv('IS_DEV', 'True') == 'True'

USE_RELOADER = IS_DEV and (os.getenv('USE_RELOADER', 'True') == 'True')

USE_DEBUGGER = IS_DEV and (os.getenv('USE_DEBUGGER', 'True') == 'True')


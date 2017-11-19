
import os

from db import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


PORT = os.getenv('PORT', 5000)

HOST = os.getenv('HOST', '0.0.0.0')

IS_DEV = os.getenv('DEV', 'True') == 'True'



import os


DB_NAME = os.getenv('DB_NAME', 'business')

DB_USER = os.getenv('DB_USER', 'pos_user')

DB_PASSWORD = os.getenv('DB_PASSWORD', False)

DB_HOST = os.getenv('DB_HOST', 'db')

DB_PORT = os.getenv('DB_PORT', 5432)

DB_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT, database=DB_NAME)

DB_ECHO = os.getenv('DB_ECHO', 'False') == 'True'


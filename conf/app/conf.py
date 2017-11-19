
import multiprocessing

from settings import HOSTNAME, PORT


workers = multiprocessing.cpu_count() * 2

worker_class = 'sync'

bind = '{}:{}'.format(HOSTNAME, PORT)

threads = 2

access_log = '-'

error_log = '-'



import multiprocessing

from settings import HOSTNAME, PORT


workers = multiprocessing.cpu_count() * 2 - 1

worker_class = 'sync'

bind = '{}:{}'.format(HOSTNAME, PORT)

threads = 2

accesslog = '-'

errorlog = '-'

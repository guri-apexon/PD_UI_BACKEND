#__version__ = '0.1.0'

from pkg_resources import get_distribution, DistributionNotFound

__release__ = 1.0
__build__ = 20201210.1

import threading
# import gevent.local
# from flask import g
import socket

class Constants:
    LOGGING_NAME = 'comparator'
    MICROSERVICE_NAME = "comparator"
    PROCESS = 'comparator'
    PREFIX = 'CMP_'

class Globals:
    HOST_NAME = socket.gethostname()
    THREAD_LOCAL = threading.local()
    # GEVENT_LOCAL = gevent.local.local()
    # FLASK_LOCAL = g








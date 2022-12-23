import socket
import threading

import gevent.local
from flask import g
from pkg_resources import DistributionNotFound, get_distribution


class Constants:
    MICROSERVICE_NAME = "finalization"
    DEFAULT_NEXUS_REPO_HOST = "usadc-vsnext01:8443"



class Globals:
    HOST_NAME = socket.gethostname()
    THREAD_LOCAL = threading.local()
    GEVENT_LOCAL = gevent.local.local()
    FLASK_LOCAL = g

    CORE_VERSION = get_distribution("etmfa-core").version

    try:
        VERSION = get_distribution("pd-finalizer").version
    except DistributionNotFound:
        VERSION = 'debug'

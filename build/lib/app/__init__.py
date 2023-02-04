from pkg_resources import get_distribution, DistributionNotFound

__release__ = 1.0
__build__ = 20201210.1

import threading
import socket

class Constants:
    MICROSERVICE_NAME = "pd-ui-backend"
    PROCESS = "pd-ui-backend"
    ENV_FILE_VAR_NAME = "PD_UI_BACKEND_ENV_FILE"


class Globals:
    HOST_NAME = socket.gethostname()
    THREAD_LOCAL = threading.local()
    # GEVENT_LOCAL = gevent.local.local()
    # FLASK_LOCAL = g








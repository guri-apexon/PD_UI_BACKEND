import logging
import os
from logstash_async.handler import AsynchronousLogstashHandler
from etmfa_finalization import Constants
from etmfa_finalization import Globals
from etmfa_finalization import configuration

DB_DIR = os.path.join("logs")
DB_FILE = os.path.join(DB_DIR, "logstash.db")


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.aidocid = None

        try:
            record.aidocid = Globals.FLASK_LOCAL.aidocid
        except (RuntimeError, AttributeError):
            # Not in Flask app context or missing attribute
            pass

        try:
            record.aidocid = Globals.GEVENT_LOCAL.aidocid
        except AttributeError:
            # Not in gevent context or missing attribute
            pass

        try:
            record.aidocid = Globals.THREAD_LOCAL.aidocid
        except AttributeError:
            pass

        return True


def initialize_logger(module_name=Constants.MICROSERVICE_NAME):
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    logger = logging.getLogger(module_name)
    if configuration.localConfig["debug"]:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    elkHandler = AsynchronousLogstashHandler(configuration.localConfig["elk"]["host"],
                                             configuration.localConfig["elk"]["port"], database_path=DB_FILE)
    logger.addHandler(elkHandler)

    if configuration.localConfig["debug"]:
        consoleHandler = logging.StreamHandler()
        consoleFormatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s-%(process)d] [%(aidocid)s] %(message)s')
        consoleHandler.setFormatter(consoleFormatter)
        logger.addHandler(consoleHandler)
    logger.addFilter(ContextFilter())

import logging
import os

from logstash_async.handler import AsynchronousLogstashHandler

from app import Constants, Globals
from app.utilities.config import settings

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
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    elk_handler = AsynchronousLogstashHandler(settings.LOGSTASH_HOST, settings.LOGSTASH_PORT, database_path=DB_FILE)
    logger.addHandler(elk_handler)

    if settings.DEBUG:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s-%(process)d] [%(aidocid)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    logger.addFilter(ContextFilter())

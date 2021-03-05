import logging
import os

from logstash_async.handler import AsynchronousLogstashHandler

from app.utilities.config import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def initialize_logger():
    project_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_path)
    logger.setLevel(logging.INFO)
    logger.addHandler(AsynchronousLogstashHandler(
        settings.LOGSTASH_HOST, settings.LOGSTASH_PORT, database_path='logstash.db'))

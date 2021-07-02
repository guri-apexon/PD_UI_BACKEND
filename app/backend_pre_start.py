"""
Checks statuses of all the services required for initialization of service
"""
from app import Constants
import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.session import SessionLocal
from app.logger_config import initialize_logger

from app.utilities.config import settings, ENV_FILE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(settings.LOGGER_NAME)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def db_status() -> None:
    """
    Checks status of DB
    """
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        # Command can be changed according to the DB server used
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    initialize_logger(settings.LOGGER_NAME)
    logger.info("pd-ui-backend: Logger Initialized")
    logger.info("pd-ui-backend: Initializing service")
    db_status()
    logger.info(f"[{ENV_FILE}] env file is used  \n** Note: Searched in system env variable[{Constants.ENV_FILE_VAR_NAME}] on the system ")
    logger.info("pd-ui-backend: Service finished initializing")

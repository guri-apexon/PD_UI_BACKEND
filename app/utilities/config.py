import logging
import os

from app import Constants
from pydantic import BaseSettings

logger = logging.getLogger(Constants.MICROSERVICE_NAME)


class Settings(BaseSettings):
    PROJECT_NAME: str
    LOGGER_NAME: str
    API: str
    APPLICATION_PORT: int
    SQLALCHEMY_DATABASE_URI: str
    PROTOCOL_FOLDER: str

    PROCESSING_DIR: str
    PROCESSING_USERPROTOCOL_BULK_DIR:str
    PROTOCOL_DATA_API_URL: str
    COMPARE_PROCESSING_DIR: str
    # Added for elastic soft delete integration in backend
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_INDEX: str
    # Logstash for Kibana
    LOGSTASH_HOST: str
    LOGSTASH_PORT: int
    LOGSTASH_ENABLED: bool
    PD_UI_BACKEND_URL:str
    MANAGEMENT_SERVICE_URL: str
    MANAGEMENT_SERVICE_HEALTH_URL:str

    # Authentication
    AUTH_ENDPOINT: str
    USERS_CRED: dict
    UNIT_TEST_CRED: list
    MGMT_CRED_HEADERS: dict
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str

    DEBUG: bool

    # Protocol alerts
    ALERT_FROM_DAYS: int

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'

ENV_FILE = os.getenv(Constants.ENV_FILE_VAR_NAME)
if ENV_FILE is None:
    logger.warning(f"PD_UI_BACKEND_ENV_FILE env variable is not set. Searching the .env file in PATH location")
    ENV_FILE='.env'
else:
    logger.info(f"Using PD_UI_BACKEND_ENV_FILE env file [{ENV_FILE}]")

settings = Settings(_env_file=ENV_FILE, _env_file_encoding='utf-8')

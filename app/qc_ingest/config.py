import logging
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    LOGGER_NAME: str
    API: str
    APPLICATION_PORT: int
    SQLALCHEMY_DATABASE_URI: str
    DEV_DB_URL : str
    TEST_DB_URL : str
    LOCAL_DB_URL : str
    PROTOCOL_FOLDER: str

    # PostgreSQL DB
    PostgreSQL_DATABASE: str
    PostgreSQL_USER: str
    PostgreSQL_PASSWORD: str
    PostgreSQL_HOST: str
    PostgreSQL_PORT: str

    DFS_UPLOAD_FOLDER: str
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

    # Ldap Configuration
    LDAP_SERVER: str
    LDAP_PORT: int
    LDAP_USERNAME: str
    LDAP_PWD: str

    # Legacy Protocol Configuration
    LEGACY_PROTOCOL_UPLOAD_DATE: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'



ENV_FILE = '.env'
settings = Settings(_env_file=ENV_FILE, _env_file_encoding='utf-8')

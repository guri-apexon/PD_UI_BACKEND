from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    API: str 
    SQLALCHEMY_DATABASE_URI: str 
    PROTOCOL_FOLDER : str
    # Added for elastic soft delete integration in backend
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_INDEX: str
    # Logstash for Kibana
    LOGSTASH_HOST: str
    LOGSTASH_PORT: int
    LOGSTASH_ENABLED: bool

    DEBUG: bool
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

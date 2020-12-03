from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    API: str = "/api"
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

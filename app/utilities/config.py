from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "PROTOCOL DIGITALIZATION"
    API: str = "/api"
    SQLALCHEMY_DATABASE_URI: str = 'mssql+pyodbc://APP_TMSDEV:app$tmsdev@USADC-VSSQLA0\SSQL03/PD_UI?driver=SQL+Server'

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

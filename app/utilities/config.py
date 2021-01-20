from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "PROTOCOL DIGITALIZATION"
    API: str = "/api"
    SQLALCHEMY_DATABASE_URI: str = 'mssql+pyodbc://pd_dev_dbo:$1457abxd@CA2SPDSQL01Q\PDSSQL001D/PD_Dev?driver=ODBC+Driver+17+for+SQL+Server'
    PROTOCOL_FOLDER : str = '//CA2SPDML06D/protocols'
    # Added for elastic soft delete integration in backend
    ELASTIC_HOST = 'ca2spdml04q'
    ELASTIC_PORT = 9200
    ELASTIC_INDEX = "pd-index-3"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

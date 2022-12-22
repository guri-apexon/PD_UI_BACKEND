from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utilities.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, connect_args={"check_same_thread": False},
                       pool_size=20, max_overflow=-1)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


POSTGRES_DB = settings.PostgreSQL_DATABASE
POSTGRES_USER = settings.PostgreSQL_USER
POSTGRES_PASSWORD = settings.PostgreSQL_PASSWORD
POSTGRES_SERVER = settings.PostgreSQL_HOST
POSTGRES_PORT = settings.PostgreSQL_PORT

PSQL_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"  
psqlengine = create_engine(PSQL_URL)

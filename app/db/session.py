from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utilities.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, connect_args={"check_same_thread": False},
                       pool_size=20, max_overflow=-1)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

PSQL_URL = f"postgresql://{settings.PostgreSQL_USER}:{settings.PostgreSQL_PASSWORD}@{settings.PostgreSQL_HOST}:{settings.PostgreSQL_PORT}/{settings.PostgreSQL_DATABASE}"  
psqlengine = create_engine(PSQL_URL)
SessionPSQL = sessionmaker(autocommit=False, autoflush=False, bind=psqlengine)

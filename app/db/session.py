from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utilities.config import settings


psqlengine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True,
                       pool_size=15, max_overflow=-1, echo=False)

SessionPSQL = sessionmaker(autocommit=False, autoflush=False, bind=psqlengine)
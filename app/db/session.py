from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utilities.config import settings


psqlengine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True,
                           pool_size=5, max_overflow=-1, echo=False,
                           pool_use_lifo=True, pool_recycle=1800)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=psqlengine)
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from datetime import datetime
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    email = Column(String, nullable=True)
    username = Column(String, nullable=True)
    date_of_registration = Column(DateTime(timezone=True), default=datetime.utcnow)
    user_type = Column(String, nullable=True)
    login_id = Column(Integer, ForeignKey("login.id"))
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=True)

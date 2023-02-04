from sqlalchemy import Column, DateTime, Integer, String, Boolean
from datetime import datetime
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Login(Base):
    __tablename__ = "login"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    system_pwd = Column(String, nullable=False)
    last_password_changed = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    internal_user = Column(Boolean)
    active_user = Column(Boolean)
    incorrect_attempts = Column(Integer, nullable=True)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=True)
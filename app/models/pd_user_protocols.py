from sqlalchemy import Column, DateTime, Integer, String, Boolean
from datetime import datetime
from app.db.base_class import Base


class PD_User_Protocols(Base):
    __tablename__ = "pd_user_protocols"

    isActive = Column(Boolean)
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String, primary_key=True)
    protocol = Column(String, nullable=True)
    projectId = Column(String, nullable=False)
    #sponsor = Column(String, nullable=False)
    follow = Column(Boolean, default=False)
    userRole = Column(String, default="primary")
    timeCreated = Column(DateTime(timezone=True), default=datetime.utcnow)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow)
    userCreated = Column(String, nullable=True)
    userUpdated = Column(String, nullable=True)

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from datetime import datetime
from app.db.base_class import Base


class PD_User_Protocols(Base):

    __tablename__ = "pd_user_protocols"

    isActive = Column(Boolean, default=True)
    id = Column(String, primary_key=True)
    userId = Column(String, primary_key=True)
    protocol = Column(String, nullable=False)
    follow = Column(Boolean, default=False)
    userRole = Column(String, default="primary")
    timeCreated = Column(DateTime(timezone=True), nullable=True)
    lastUpdated = Column(DateTime(timezone=True), nullable=True)
    userCreated = Column(String, nullable=True)
    userUpdated = Column(String, nullable=True)

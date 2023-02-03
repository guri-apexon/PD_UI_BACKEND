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
    follow = Column(Boolean, default=False)
    userRole = Column(String, default="primary")
    redactProfile = Column(String, nullable=True)
    timeCreated = Column(DateTime(timezone=True), default=datetime.utcnow)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow)
    userCreated = Column(String, nullable=True)
    userUpdated = Column(String, nullable=True)

    def __init__(self, **kwargs):
        self.isActive = kwargs.get("isActive", True)
        self.userId = kwargs.get("userId", None)
        self.protocol = kwargs.get("protocol", None)
        self.projectId = kwargs.get("projectId", None)
        self.follow = kwargs.get("follow", None)
        self.userRole = kwargs.get("userRole", None)
        self.redactProfile = kwargs.get("redactProfile", None)
        self.timeCreated = kwargs.get("timeCreated", datetime.utcnow())
        self.lastUpdated = kwargs.get("lastUpdated", datetime.utcnow())
        self.userCreated = kwargs.get("userCreated", None)
        self.userUpdated = kwargs.get("userUpdated", None)

    def as_dict(self):
        obj = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return obj

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from datetime import datetime
from app.db.base_class import Base


class PDUserAccessChangeLog(Base):
    __tablename__ = "pd_user_access_change_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String)
    protocol = Column(String, nullable=True)
    projectId = Column(String, nullable=False)
    follow = Column(Boolean, default=False)
    userRole = Column(String, default="primary")
    redactProfile = Column(String, nullable=True)
    userUpdated = Column(String, nullable=True)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow)
    reason_for_change = Column(String, nullable=True)
    access_level_change = Column(String, nullable=True)

    def as_dict(self):
        obj = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return obj

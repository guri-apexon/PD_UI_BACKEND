from sqlalchemy import Column, String, Boolean,DateTime
from app.db.base_class import Base
from datetime import datetime


class PdUserNotificationType(Base):
    __tablename__ = "pd_user_notification_type"

    id = Column(String, primary_key=True, autoincrement=True)
    userId = Column(String, nullable=True)
    content = Column(String, nullable=True)
    read_flag = Column(Boolean, default=False)
    notification_delete = Column(Boolean, default=False)
    created_time = Column(DateTime(timezone=True), default=datetime.utcnow)

    def as_dict(self):
        obj = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return obj

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from datetime import datetime
from app.db.base_class import Base


class UserAlertSetting(Base):
    __tablename__ = "pd_user_alert"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, nullable=True)
    new_document_version = Column(Boolean, nullable=True)
    edited = Column(Boolean, nullable=True)
    QC_complete = Column(Boolean, nullable=True)
    created_time = Column(DateTime(timezone=True), default=datetime.utcnow,
                          nullable=True)
    updated_time = Column(DateTime(timezone=True), default=datetime.utcnow,
                          nullable=True)

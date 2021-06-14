import datetime

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Date, DateTime, String


class ProtocolAlert(Base):
    __tablename__ = "pd_protocol_alert"

    id = Column(String(100), primary_key=True)
    aidocId = Column(String(100), primary_key=True)
    protocol = Column(String(500))
    shortTitle = Column(String(1500))
    readFlag = Column(Boolean(), default=False)
    readTime = Column(DateTime(timezone=True))
    emailSentFlag = Column(Boolean(), default=False)
    emailSentTime = Column(DateTime(timezone=True))
    alertGeneratedTime = Column(DateTime(timezone=True))
    approvalDate = Column(Date())
    isActive = Column(Boolean(), default=True)
    timeCreated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    timeUpdated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

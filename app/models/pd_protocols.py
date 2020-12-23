from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class PD_Protocols(Base):

    __tablename__ = "pd_protocols"

    id = Column(Integer, primary_key=True, index=True)
    protocol = Column(String, nullable=True)
    protocolTitle = Column(String, nullable=True)
    projectCode = Column(String, nullable=True)
    phase = Column(Integer, nullable=True)
    indication = Column(String, nullable=True)
    protocolStatus = Column(Integer, nullable=True)
    protocolVersion = Column(String, nullable=True)
    protocolSponsor = Column(Integer, nullable=True)
    isActive = Column(Boolean, default=True)
    userCreated = Column(String, nullable=True)
    timeCreated = Column(DateTime(timezone=True), default=datetime.utcnow)
    userUpdated = Column(String, nullable=True)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow)

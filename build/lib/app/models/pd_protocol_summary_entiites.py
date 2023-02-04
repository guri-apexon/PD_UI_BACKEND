import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.db.base_class import Base


class PDProtocolSummaryEntities(Base):
    __tablename__ = "pd_protocol_summary_entities"

    aidocId = Column(String(128), primary_key=True, index=True)
    source = Column(String(50), primary_key=True, index=True)
    runId = Column(Integer, primary_key=True, index=True)
    iqvdataSummaryEntities = Column(String(4096))
    isActive = Column(Boolean(), default=True)
    timeCreated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    timeUpdated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

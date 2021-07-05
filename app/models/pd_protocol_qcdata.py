import datetime
from sqlalchemy import Column, String, Boolean, DateTime

from app.db.base_class import Base


class PD_Protocol_QCData(Base):
    __tablename__ = "pd_protocol_qcdata"

    id = Column(String, primary_key=True)
    userId = Column(String, primary_key=True)
    fileName = Column(String, nullable=True)
    documentFilePath = Column(String, nullable=True)
    iqvdataToc = Column(String, nullable=True)
    iqvdataSoa = Column(String, nullable=True)
    iqvdataSoaStd = Column(String, nullable=True)
    iqvdataSummary = Column(String, nullable=True)
    iqvdata = Column(String, nullable=True)
    isActive = Column(Boolean, default=True)
    timeCreated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    timeUpdated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)



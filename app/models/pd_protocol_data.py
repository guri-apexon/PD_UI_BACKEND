from sqlalchemy import Column, DateTime, Integer, String, Boolean
from datetime import datetime
from app.db.base_class import Base


class PD_Protocol_Data(Base):

    __tablename__ = "pd_protocol_data"

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

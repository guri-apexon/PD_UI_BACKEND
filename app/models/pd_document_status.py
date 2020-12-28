from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime
from app.db.base_class import Base


class PD_Document_Status(Base):

    __tablename__ = "pd_document_process"

    id = Column(String, primary_key=True)
    userId = Column(String, nullable=True)
    isProcessing = Column(Integer, nullable=True)
    fileName = Column(String, nullable=True)
    documentFilePath = Column(String, nullable=True)
    percentComplete = Column(String, nullable=True)
    status = Column(String, nullable=True)
    feedback = Column(String, nullable=True)
    errorCode = Column(Integer, nullable=True)
    errorReason = Column(String, nullable=True)
    timeCreated = Column(DateTime(timezone=True), default=datetime.utcnow)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow)

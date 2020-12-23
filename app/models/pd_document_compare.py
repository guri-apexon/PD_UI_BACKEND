from sqlalchemy import Column, DateTime, Integer, String, VARCHAR
from datetime import datetime
from app.db.base_class import Base


class PD_Document_Compare(Base):

    __tablename__ = "pd_document_compare"

    
    compareId = Column(String, primary_key=True)
    id1 = Column(String, primary_key=True)
    protocolNumber = Column(String, nullable=True)
    projectId = Column(String, nullable=True)
    versionNumber = Column(String, nullable=True)
    amendmentNumber = Column(String, nullable=True)
    documentStatus = Column(String, nullable=True)
    id2 = Column(String, primary_key=True)
    protocolNumber2 = Column(String, nullable=True)
    projectId2 = Column(String, nullable=True)
    versionNumber2 = Column(String, nullable=True)
    amendmentNumber2 = Column(String, nullable=True)
    documentStatus2 = Column(String, nullable=True)
    environment = Column(String, nullable=True)
    sourceSystem = Column(String, nullable=True)
    userId = Column(String, nullable=True)
    requestType = Column(String, nullable=True)
    iqvdata = Column(VARCHAR, nullable=True)
    baseIqvXmlPath = Column(String, nullable=True)
    compareIqvXmlPath = Column(String, nullable=True)
    updatedIqvXmlPath = Column(String, nullable=True)
    similarityScore = Column(Integer, nullable=True)

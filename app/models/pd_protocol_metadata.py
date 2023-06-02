from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float

from app.db.base_class import Base


class PD_Protocol_Metadata(Base):

    __tablename__ = "pd_protocol_metadata"

    id = Column(String, primary_key=True, index=True)
    userId = Column(String, primary_key=True, index=True)
    fileName = Column(String, nullable=True)
    documentFilePath = Column(String, nullable=True)
    protocol = Column(String, nullable=True)
    projectId = Column(String, nullable=False)
    sponsor = Column(String, nullable=False)
    indication = Column(String, nullable=False)
    moleculeDevice = Column(String, nullable=False)
    amendment = Column(String, nullable=True)
    versionNumber = Column(String, nullable=True)
    documentStatus = Column(String, nullable=False)
    draftVersion = Column(String, nullable=True)
    errorCode = Column(Integer, nullable=True)
    errorReason = Column(String, nullable=True)
    status = Column(String, nullable=True)
    qcStatus = Column(String, nullable=True)
    runId = Column(Integer, default=0)
    isProcessing = Column(Boolean, default=False)
    percentComplete = Column(String, nullable=True)
    compareStatus = Column(String, nullable=True)
    iqvXmlPathProc = Column(String, nullable=True)
    iqvXmlPathComp = Column(String, nullable=True)
    phase = Column(String, nullable=True)
    digitizedConfidenceInterval = Column(String, nullable=True)
    completenessOfDigitization = Column(String, nullable=True)
    protocolTitle = Column(String, nullable=True)
    shortTitle = Column(String, nullable=True)
    studyStatus = Column(String, nullable=True)
    sourceSystem = Column(String, nullable=True)
    environment = Column(String, nullable=True)
    uploadDate = Column(DateTime(timezone=True), nullable=True)
    timeCreated = Column(DateTime(timezone=True), nullable=True)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    userCreated = Column(String, nullable=True)
    userUpdated = Column(String, nullable=True)
    approvalDate = Column(DateTime(timezone=True), nullable=True)
    isActive = Column(Boolean, default=True)
    nctId = Column(String, nullable=True)
    source = Column(String, nullable=True)
    lastQcUpdated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    def as_dict(self):
        obj = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        return obj    

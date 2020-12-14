from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float

from app.db.base_class import Base


class PD_User_Protocol_Documents(Base):

    __tablename__ = "pd_user_protocol_documents"

    id = Column(String, nullable=False)
    userId = Column(String, primary_key=True, index=True)
    fileName = Column(String, nullable=True)
    filePath = Column(String, nullable=True)
    Protocol = Column(String, nullable=False)
    ProtocolName = Column(String, nullable=True)
    ProjectId = Column(String, nullable=True)
    Sponser = Column(String, nullable=False)
    Indication = Column(String, nullable=True)
    Molecule = Column(String, nullable=True)
    Amendment = Column(String, nullable=True)
    VersionNumber = Column(Float, nullable=True)
    DocumentStatus = Column(String, nullable=True)
    DraftVersion = Column(Float, nullable=True)
    errorCode = Column(Integer, nullable=True)
    errorReason = Column(String, nullable=True)
    Status = Column(String, nullable=True)
    phase = Column(String, nullable=True)
    DigitizedConfidenceInterval = Column(String, nullable=True)
    CompletenessOfDigitization = Column(String, nullable=True)
    protocolTitle = Column(String, nullable=True)
    studyStatus = Column(String, nullable=True)
    sourceSystem = Column(String, nullable=True)
    environment = Column(String, nullable=True)
    uploadDate = Column(DateTime(timezone=True), nullable=True)
    timeCreated = Column(DateTime(timezone=True), nullable=True)
    timeUpdated = Column(DateTime(timezone=True), nullable=True)
    userCreated = Column(String, nullable=True)
    userModified = Column(String, nullable=True)
    ApprovalDate = Column(DateTime(timezone=True), nullable=True)
    isActive = Column(Boolean, default=True)
    iqvxmlpath = Column(String, nullable=True)
    NctId = Column(String, nullable=True)

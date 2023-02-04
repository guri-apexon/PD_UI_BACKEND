import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date

from app.db.base_class import Base


class PDProtocolQCSummaryData(Base):
    __tablename__ = "pd_protocol_qc_summary_data"

    aidocId = Column(String(128), primary_key=True, index=True)
    source = Column(String(32), primary_key=True, index=True)
    sponsor = Column(String(256))
    protocolNumber = Column(String(64))
    trialPhase = Column(String(16))
    versionNumber = Column(String(64))
    isAmendment = Column(String(8))
    amendmentNumber = Column(String(64))
    approvalDate = Column(Date)
    versionDate = Column(Date)
    protocolTitle = Column(String(1024))
    protocolShortTitle = Column(String(512))
    indications = Column(String(1024))
    moleculeDevice = Column(String(128))
    investigator = Column(String(128))
    blinded = Column(String(64))
    drug = Column(String(256))
    compoundNumber = Column(String(256))
    control = Column(String(512))
    endPoints = Column(String(4096))
    trialTypeRandomized = Column(String(2048))
    regulatoryIdNctId = Column(String(256))
    sponsorAddress = Column(String(512))
    numberOfSubjects = Column(String(32))
    participantAge = Column(String(64))
    participantSex = Column(String(16))
    studyPopulation = Column(String(128))
    inclusionCriteria = Column(String(4096))
    exclusionCriteria = Column(String(4096))
    primaryObjectives = Column(String(4096))
    secondaryObjectives = Column(String(4096))
    runId = Column(Integer, default=0)

    isActive = Column(Boolean(), default=True)
    qcApprovedBy = Column(String(16))
    userCreated = Column(String(64))
    timeCreated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    userUpdated = Column(String(64))
    timeUpdated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


from typing import Optional
from datetime import datetime
from pydantic import BaseModel



# Shared properties
class ProtocolQCSummaryDataBase(BaseModel):
    id: Optional[str] = None
    source: Optional[str] = None
    sponsor: Optional[str] = None
    protocolNumber: Optional[str] = None
    trialPhase: Optional[str] = None
    versionNumber: Optional[str] = None
    amendmentNumber: Optional[str] = None
    approvalDate: Optional[datetime] = None
    versionDate: Optional[datetime] = None
    protocolTitle: Optional[str] = None
    protocolShortTitle: Optional[str] = None
    indications: Optional[str] = None
    moleculeDevice: Optional[str] = None
    investigator: Optional[str] = None
    blinded: Optional[str] = None
    drug: Optional[str] = None
    compoundNumber: Optional[str] = None
    control: Optional[str] = None
    endPoints: Optional[str] = None
    trialTypeRandomized: Optional[str] = None
    regulatoryIdNctId: Optional[str] = None
    sponsorAddress: Optional[str] = None
    numberOfSubjects: Optional[str] = None
    participantAge: Optional[str] = None
    participantSex: Optional[str] = None
    studyPopulation: Optional[str] = None
    inclusionCriteria: Optional[str] = None
    exclusionCriteria: Optional[str] = None
    primaryObjectives: Optional[str] = None
    secondaryObjectives: Optional[str] = None
    isActive: Optional[bool] = None
    qcApprovedBy: Optional[str] = None


# Properties to receive via API on creation
class ProtocolQCSummaryDataCreate(ProtocolQCSummaryDataBase):
    id: str
    source: str
    sponsor: str
    protocolNumber: str
    trialPhase: str
    versionNumber: str
    amendmentNumber: str
    approvalDate: datetime
    versionDate: datetime
    protocolTitle: str
    protocolShortTitle: str
    indications: str
    moleculeDevice: str
    investigator: str
    blinded: str
    drug: str
    compoundNumber: str
    control: str
    endPoints: str
    trialTypeRandomized: str
    regulatoryIdNctId: str
    sponsorAddress: str
    numberOfSubjects: str
    participantAge: str
    participantSex: str
    studyPopulation: str
    inclusionCriteria: str
    exclusionCriteria: str
    primaryObjectives: str
    secondaryObjectives: str
    isActive: bool
    qcApprovedBy: str


# Properties to receive via API on update
class ProtocolQCSummaryDataUpdate(ProtocolQCSummaryDataBase):
    pass


class ProtocolQCSummaryDataInDBBase(ProtocolQCSummaryDataBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProtocolQCSummaryData(ProtocolQCSummaryDataInDBBase):
    pass


class ProtocolQCSummaryDataReadIqvdataBase(BaseModel):
    iqvdata: Optional[str] = None


class ProtocolQCSummaryDataReadIqvdataInDBBase(ProtocolQCSummaryDataReadIqvdataBase):
    pass

    class Config:
        orm_mode = True


# Iqvdata to return via API
class ProtocolQCSummaryDataReadIqvdata(ProtocolQCSummaryDataReadIqvdataInDBBase):
    pass




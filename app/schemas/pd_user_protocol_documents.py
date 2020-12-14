from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class UserProtocolDocumentsBase(BaseModel):
    id: Optional[str] = None
    userId: Optional[str] = None
    fileName: Optional[str] = None
    filePath: Optional[str] = None
    Protocol: Optional[str] = None
    ProtocolName: Optional[str] = None
    ProjectId: Optional[int] = None
    Sponser: Optional[str] = None
    Indication: Optional[str] = None
    Molecule: Optional[str] = None
    Amendment: Optional[str] = None
    VersionNumber: Optional[float] = None
    DocumentStatus: Optional[str] = None
    DraftVersion: Optional[float] = None
    errorCode: Optional[int] = None
    errorReason: Optional[str] = None
    Status: Optional[str] = None
    phase: Optional[str] = None
    DigitizedConfidenceInterval: Optional[str] = None
    CompletenessOfDigitization : Optional[str] = None
    protocolTitle: Optional[str] = None
    studyStatus: Optional[str] = None
    sourceSystem: Optional[str] = None
    environment: Optional[str] = None
    uploadDate: Optional[datetime] = None
    timeCreated: Optional[datetime] = None
    timeUpdated: Optional[datetime] = None
    userCreated: Optional[str] = None
    userModified: Optional[str] = None
    ApprovalDate: Optional[datetime] = None
    isActive: Optional[bool] = None
    iqvxmlpath: Optional[str] = None
    NctId: Optional[str] = None



# Properties to receive via API on creation
class UserProtocolDocumentsCreate(UserProtocolDocumentsBase):
    id: str
    userId: str
    fileName: str  
    filePath: str  
    Protocol: str
    ProtocolName: str  
    ProjectId: int  
    Sponser: str 
    Indication: str  
    Molecule: str  
    Amendment: str 
    VersionNumber: float
    DocumentStatus: str  
    DraftVersion: float 
    errorCode: int  
    errorReason: str  
    Status: str 
    phase: str  
    DigitizedConfidenceInterval: str  
    CompletenessOfDigitization : str  
    protocolTitle: str
    studyStatus: str  
    sourceSystem: str  
    environment: str  
    uploadDate: datetime  
    timeCreated: datetime  
    timeUpdated: datetime 
    userCreated: str
    userModified: str  
    ApprovalDate: datetime  
    isActive: bool
    iqvxmlpath: str  
    NctId: int


# Properties to receive via API on update
class UserProtocolDocumentsUpdate(UserProtocolDocumentsBase):
    #sponsor_abbreviation: Optional[str] = None
    pass

class UserProtocolDocumentsInDBBase(UserProtocolDocumentsBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserProtocolDocuments(UserProtocolDocumentsInDBBase):
    pass

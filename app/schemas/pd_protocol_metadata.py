from typing import Optional, List
from datetime import datetime, date

from pydantic import BaseModel, constr


# Shared properties
class ProtocolMetadataBase(BaseModel):
    id: Optional[str] = None
    userId: Optional[str] = None
    fileName: Optional[str] = None
    documentFilePath: Optional[str] = None
    protocol: Optional[str] = None
    projectId: Optional[str] = None
    sponsor: Optional[str] = None
    indication: Optional[str] = None
    moleculeDevice: Optional[str] = None
    amendment: Optional[str] = None
    isProcessing: Optional[bool] = None
    percentComplete: Optional[str] = None
    compareStatus: Optional[str] = None
    iqvXmlPathProc: Optional[str] = None
    iqvXmlPathComp: Optional[str] = None
    shortTitle: Optional[str] = None
    versionNumber: Optional[str] = None
    documentStatus: Optional[str] = None
    draftVersion: Optional[str] = None
    errorCode: Optional[int] = None
    errorReason: Optional[str] = None
    status: Optional[str] = None
    qcStatus: Optional[str] = None
    phase: Optional[str] = None
    digitizedConfidenceInterval: Optional[str] = None
    completenessOfDigitization : Optional[str] = None
    protocolTitle: Optional[str] = None
    studyStatus: Optional[str] = None
    sourceSystem: Optional[str] = None
    environment: Optional[str] = None
    uploadDate: Optional[datetime] = None
    timeCreated: Optional[datetime] = None
    lastUpdated: Optional[datetime] = None
    userCreated: Optional[str] = None
    userUpdated: Optional[str] = None
    approvalDate: Optional[datetime] = None
    isActive: Optional[bool] = None
    nctId: Optional[str] = None



# Properties to receive via API on creation
class ProtocolMetadataCreate(ProtocolMetadataBase):
    id: str
    userId: str
    fileName: str  
    documentFilePath: str  
    protocol: str 
    projectId: str
    sponsor: str 
    indication: str  
    moleculeDevice: str  
    amendment: str 
    versionNumber: str
    documentStatus: str  
    draftVersion: str 
    isProcessing: bool
    percentComplete: str 
    compareStatus: str 
    iqvXmlPathProc: str 
    iqvXmlPathComp: str 
    shortTitle: str 
    errorCode: int  
    errorReason: str  
    status: str 
    qcStatus: str
    phase: str  
    digitizedConfidenceInterval: str  
    completenessOfDigitization : str  
    protocolTitle: str
    studyStatus: str  
    sourceSystem: str  
    environment: str  
    uploadDate: datetime  
    timeCreated: datetime  
    lastUpdated: datetime 
    userCreated: str
    userUpdated: str  
    approvalDate: datetime  
    isActive: bool
    nctId: str

class ProtocolMetadataUserId(ProtocolMetadataBase):
    amendmentNumber: Optional[str] = None
    approvalDate: Optional[date] = None
    redactProfile: Optional[str] = None
    userUploadedFlag: bool = False
    userPrimaryRoleFlag: bool = False
    userFollowingFlag: bool = False

# Properties to receive via API on update
class ProtocolMetadataUpdate(ProtocolMetadataBase):
    pass

class ProtocolMetadataInDBBase(ProtocolMetadataBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProtocolMetadata(ProtocolMetadataInDBBase):
    pass

# Additional properties to return via API
class ProtocolMetadataUploadUser(ProtocolMetadataInDBBase):
    uploadedBy: str = ''
    userRole: str = ''

class ProtocolMetadataDuplicateBase(BaseModel):   
    protocol: Optional[str] = None
    sponsor: Optional[str] = None
    versionNumber: Optional[str] = None
    amendment: Optional[str] = None
    Duplicate: str = "This protocol document cannot be added to the library because it already exists."

class ProtocolMetadataDuplicateInDBBase(ProtocolMetadataDuplicateBase):
    pass

    class Config:
        orm_mode = True

# Additional properties to return via Duplicate check API
class ProtocolMetadataDuplicateCheck(ProtocolMetadataDuplicateInDBBase):
    pass

class ProtocolStatusBase(BaseModel):   
    id: Optional[str] = None
    userId: Optional[str] = None
    fileName: Optional[str] = None
    documentFilePath: Optional[str] = None
    percentComplete: Optional[str] = None
    status: Optional[str] = None
    qcStatus: Optional[str] = None
    errorCode: Optional[int] = None
    errorReason: Optional[str] = None
    timeCreated: Optional[datetime] = None
    lastUpdated: Optional[datetime] = None

class ProtocolStatusInDBBase(ProtocolStatusBase):
    pass

    class Config:
        orm_mode = True

# Additional properties to return via Duplicate check API
class ProtocolStatus(ProtocolStatusInDBBase):
    pass

class ChangeQcStatus(BaseModel):
    docIdArray: List[constr(min_length=10, strip_whitespace=True)]
    targetStatus: constr(regex='^QC_NOT_STARTED|QC1|QC2$', strip_whitespace=True)

class ProtocolLatestRecordBase(BaseModel):   
    protocol: Optional[str] = None
    sponsor: Optional[str] = None
    versionNumber: Optional[str] = None
    documentStatus: Optional[str] = None

class ProtocolLatestRecordInDBBase(ProtocolLatestRecordBase):
    pass

    class Config:
        orm_mode = True

# Additional properties to return latest protocol API
class ProtocolLatestRecord(ProtocolLatestRecordInDBBase):
    pass

# Soft delete
class ProtocolMetadataSoftDelete(BaseModel):
    id: Optional[str] = None
    userId: Optional[str] = None
    protocol: Optional[str] = None
    projectId: Optional[str] = None
    #Opportunity no: Optional[str] = None
    sponsor: Optional[str] = None
    indication: Optional[str] = None
    moleculeDevice: Optional[str] = None
    amendment: Optional[str] = None
    versionNumber: Optional[str] = None
    documentStatus: Optional[str] = None
    isActive:Optional[bool] = None
# Properties to receive via API on creation
class ProtocolMetadataSoftDeleteCreate(ProtocolMetadataSoftDelete):
    id: str
    userId: str
    protocol: str
    projectId: str
    #Opportunity no: Optional[str] = None
    sponsor: str
    indication: str
    moleculeDevice: str
    amendment: str
    versionNumber: str
    documentStatus: str
    isActive:bool
# Properties to receive via API on creati

class UpdateMetadataSoftdelete(ProtocolMetadataSoftDelete):
    pass

    class Config:
        orm_mode = True

# Additional properties to return latest protocol API
class MetadataSoftdelete(UpdateMetadataSoftdelete):
    pass
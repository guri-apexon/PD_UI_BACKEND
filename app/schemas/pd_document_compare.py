from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class DocumentCompareBase(BaseModel):
    compareId: Optional[str] = None
    id1: Optional[str] = None
    protocolNumber: Optional[str] = None
    projectId: Optional[str] = None
    versionNumber: Optional[str] = None
    amendmentNumber: Optional[str] = None
    documentStatus: Optional[str] = None
    id2: Optional[str] = None
    protocolNumber2: Optional[str] = None
    projectId2: Optional[str] = None
    versionNumber2: Optional[str] = None
    amendmentNumber2: Optional[str] = None
    documentStatus2: Optional[str] = None
    environment: Optional[str] = None
    sourceSystem: Optional[str] = None
    userId: Optional[str] = None
    requestType: Optional[str] = None
    iqvdata: Optional[str] = None
    baseIqvXmlPath: Optional[str] = None
    compareIqvXmlPath: Optional[str] = None
    updatedIqvXmlPath: Optional[str] = None
    similarityScore: Optional[int] = None


# Properties to receive via API on creation
class DocumentCompareCreate(DocumentCompareBase):
    compareId: str
    id1: str
    protocolNumber: str
    projectId: str
    versionNumber: str
    amendmentNumber: str
    documentStatus: str
    id2: str
    protocolNumber2: str
    projectId2: str
    versionNumber2: str
    amendmentNumber2: str
    documentStatus2: str
    environment: str
    sourceSystem: str
    userId: str
    requestType: str
    iqvdata: str
    baseIqvXmlPath: str
    compareIqvXmlPath: str
    updatedIqvXmlPath: str
    similarityScore: int

# Properties to receive via API on update
class DocumentCompareUpdate(DocumentCompareBase):
    pass
    

class DocumentCompareInDBBase(DocumentCompareBase):
    id1: Optional[str] = None
    id2: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class DocumentCompare(DocumentCompareInDBBase):
    pass

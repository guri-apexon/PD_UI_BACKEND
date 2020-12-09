from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class DocumentProcessBase(BaseModel):
    id: Optional[str] = None
    userId: Optional[str] = None
    isProcessing: Optional[bool] = None
    fileName: Optional[str] = None
    documentFilePath: Optional[str] = None
    percentComplete: Optional[str] = None
    status: Optional[str] = None
    feedback: Optional[str] = None
    errorCode: Optional[int] = None
    errorReason: Optional[str] = None
    timeCreated: Optional[datetime] = None
    lastUpdated: Optional[datetime] = None


# Properties to receive via API on creation
class DocumentProcessCreate(DocumentProcessBase):
    id: str
    userId: str
    isProcessing: bool
    fileName: str
    documentFilePath: str
    percentComplete: str
    status: str
    feedback: str
    errorCode: int
    errorReason: str
    timeCreated: datetime
    lastUpdated: datetime


# Properties to receive via API on update
class DocumentProcessUpdate(DocumentProcessBase):
    pass
    

class DocumentProcessInDBBase(DocumentProcessBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class DocumentProcess(DocumentProcessInDBBase):
    pass

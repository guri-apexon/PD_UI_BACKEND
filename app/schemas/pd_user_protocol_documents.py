from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class UserProtocolDocumentsBase(BaseModel):
    protocol_id: Optional[int] = None
    user_id: Optional[int] = None
    protocol_document_name: Optional[str] = None
    protocol_document_status_id: Optional[int] = None
    protocol_source_document_id: Optional[int] = None
    is_active: Optional[bool] = None
    created_by: Optional[str] = None
    created_on: Optional[datetime] = None
    modified_by: Optional[str] = None
    modified_on: Optional[datetime] = None



# Properties to receive via API on creation
class UserProtocolDocumentsCreate(UserProtocolDocumentsBase):
    protocol_id: int
    user_id: int
    protocol_document_name: str
    protocol_document_status_id: int
    protocol_source_document_id: int
    is_active: bool
    created_by: str
    created_on: datetime
    modified_by: str
    modified_on: datetime


# Properties to receive via API on update
class UserProtocolDocumentsUpdate(UserProtocolDocumentsBase):
    #sponsor_abbreviation: Optional[str] = None
    pass

class UserProtocolDocumentsInDBBase(UserProtocolDocumentsBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserProtocolDocuments(UserProtocolDocumentsInDBBase):
    pass

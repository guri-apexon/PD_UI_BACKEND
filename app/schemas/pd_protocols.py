from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class ProtocolBase(BaseModel):
    protocol_number: Optional[str] = None
    protocol_title: Optional[str] = None
    project_code: Optional[str] = None
    phase: Optional[int] = None
    indication: Optional[str] = None
    protocol_status: Optional[int] = None
    protocol_version: Optional[str] = None
    protocol_sponsor: Optional[int] = None
    is_active: Optional[bool] = None
    created_by: Optional[str] = None
    created_on: Optional[datetime] = None
    modified_by: Optional[str] = None
    modified_on: Optional[datetime] = None



# Properties to receive via API on creation
class ProtocolCreate(ProtocolBase):
    protocol_number: str
    protocol_title: str
    project_code: str
    phase: int
    indication: str
    protocol_status: int
    protocol_version: str
    protocol_sponsor: int
    is_active: bool
    created_by: str
    created_on: datetime
    modified_by: str
    modified_on: datetime


# Properties to receive via API on update
class ProtocolUpdate(ProtocolBase):
    #sponsor_abbreviation: Optional[str] = None
    pass

class ProtocolInDBBase(ProtocolBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Protocol(ProtocolInDBBase):
    pass

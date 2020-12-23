from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class ProtocolBase(BaseModel):
    protocol: Optional[str] = None
    protocolTitle: Optional[str] = None
    projectCode: Optional[str] = None
    phase: Optional[str] = None
    indication: Optional[str] = None
    protocolStatus: Optional[str] = None
    protocolVersion: Optional[str] = None
    protocolSponsor: Optional[str] = None
    isActive: Optional[bool] = None
    userCreated: Optional[str] = None
    timeCreated: Optional[datetime] = None
    userUpdated: Optional[str] = None
    lastUpdated: Optional[datetime] = None



# Properties to receive via API on creation
class ProtocolCreate(ProtocolBase):
    protocol: str
    protocolTitle: str
    projectCode: str
    phase: str
    indication: str
    protocolStatus: str
    protocolVersion: str
    protocolSponsor: str
    isActive: bool
    userCreated: str
    timeCreated: datetime
    userUpdated: str
    lastUpdated: datetime


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

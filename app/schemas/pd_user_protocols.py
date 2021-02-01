from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class UserProtocolBase(BaseModel):
    userId: Optional[str] = None
    protocol: Optional[str] = None
    userRole: Optional[str] = None
    userCreated: Optional[str] = None
    userUpdated: Optional[str] = None


# Properties to receive via API on creation
class UserProtocolCreate(UserProtocolBase):
    isActive: bool
    userId: str
    protocol: str
    follow: bool = True
    userRole: str = "secondary"
    userCreated: str
    userCreated: str
    timeCreated: datetime
    lastUpdated: datetime
    userUpdated: str 


class UserProtocolAdd(UserProtocolBase):
    userId: str
    protocol: str
    projectId: str
    userRole: str
    userCreated: str
    userUpdated: str




# Properties to receive via API on update
class UserProtocolUpdate(UserProtocolBase):
    pass
    

class UserProtocolInDBBase(UserProtocolBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserProtocol(UserProtocolInDBBase):
    pass


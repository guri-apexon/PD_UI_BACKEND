from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class UserProtocolBase(BaseModel):
    isActive: Optional[bool] = None
    id: Optional[str] = None
    userId: Optional[str] = None
    protocol: Optional[str] = None
    follow: Optional[bool] = None
    userRole: Optional[str] = None
    userCreated: Optional[str] = None
    timeCreated: Optional[datetime] = None
    lastUpdated: Optional[datetime] = None
    userUpdated: Optional[str] = None


# Properties to receive via API on creation
class UserProtocolCreate(UserProtocolBase):
    isActive: bool
    id: str
    userId: str
    userId: str
    protocol: str
    follow: bool
    userCreated: str
    userCreated: str
    timeCreated: datetime  
    lastUpdated: datetime 
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


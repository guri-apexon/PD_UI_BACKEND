from typing import Optional
from pydantic import BaseModel


class UserProtocolAccessBase(BaseModel):
    userId: Optional[str] = None
    protocol: Optional[str] = None
    projectId: Optional[str] = None
    follow: Optional[str] = None
    userRole: Optional[str] = None
    userUpdated: Optional[str] = None
    accessReason: Optional[str] = None


# Properties to receive via API on creation
class UserProtocolAccessCreate(UserProtocolAccessBase):
    follow: bool


# Properties to receive via API on update
class UserProtocolAccessUpdate(UserProtocolAccessBase):
    pass



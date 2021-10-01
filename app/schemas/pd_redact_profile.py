from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class RedactProfileBase(BaseModel):
    isActive: Optional[str] = None
    subCategory: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    profile_0: Optional[str] = None
    profile_1: Optional[str] = None


# Properties to receive via API on creation
class RedactProfileCreate(RedactProfileBase):
    pass


# Properties to receive via API on update
class RedactProfileUpdate(RedactProfileBase):
    pass
    

class RedactProfileInDBBase(RedactProfileBase):

    class Config:
        orm_mode = True

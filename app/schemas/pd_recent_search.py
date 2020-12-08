from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class RecentSearchBase(BaseModel):
    keyword: Optional[str] = None
    user: Optional[str] = None
    timeCreated: Optional[datetime] = None
    lastUpdated: Optional[datetime] = None


# Properties to receive via API on creation
class RecentSearchCreate(RecentSearchBase):
    keyword: str
    user: str
    timeCreated : datetime
    lastUpdated : datetime


# Properties to receive via API on update
class RecentSearchUpdate(RecentSearchBase):
    lastUpdated: Optional[datetime] = None
    

class RecentSearchInDBBase(RecentSearchBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class RecentSearch(RecentSearchInDBBase):
    pass

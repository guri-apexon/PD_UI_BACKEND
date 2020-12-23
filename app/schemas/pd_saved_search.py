from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class SavedSearchBase(BaseModel):                   
    keyword: Optional[str] = None
    userId: Optional[str] = None
    timeCreated: Optional[datetime] = None
    lastUpdated: Optional[datetime] = None


# Properties to receive via API on creation
class SavedSearchCreate(SavedSearchBase):
    keyword: str
    userId: str
    timeCreated : datetime
    lastUpdated : datetime


# Properties to receive via API on update
class SavedSearchUpdate(SavedSearchBase):
    lastUpdated: Optional[datetime] = None


class SavedSearchInDBBase(SavedSearchBase):
    saveId: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class SavedSearch(SavedSearchInDBBase):
    pass

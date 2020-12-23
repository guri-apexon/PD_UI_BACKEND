from typing import Optional

from pydantic import BaseModel


# Shared properties
class IndicationsBase(BaseModel):
    indicationName: Optional[str] = None


# Properties to receive via API on creation
class IndicationsCreate(IndicationsBase):
    indicationName: str


# Properties to receive via API on update
class IndicationsUpdate(IndicationsBase):
    pass

class IndicationsInDBBase(IndicationsBase):
    indId: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Indications(IndicationsInDBBase):
    pass

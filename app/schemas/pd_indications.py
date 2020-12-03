from typing import Optional

from pydantic import BaseModel


# Shared properties
class IndicationsBase(BaseModel):
    indication_name: Optional[str] = None
    indication_description: Optional[str] = None


# Properties to receive via API on creation
class IndicationsCreate(IndicationsBase):
    indication_name: str
    indication_description: str


# Properties to receive via API on update
class IndicationsUpdate(IndicationsBase):
    indication_description: Optional[str] = None

class IndicationsInDBBase(IndicationsBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Indications(IndicationsInDBBase):
    pass

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class DocumentCompareBase(BaseModel):

    compareCSVPath: Optional[str] = None
    numChangesTotal: Optional[int] = None





# Properties to receive via API on creation
class DocumentCompareCreate(DocumentCompareBase):

    compareCSVPath: str
    numChangesTotal: int

# Properties to receive via API on update
class DocumentCompareUpdate(DocumentCompareBase):
    pass
    

class DocumentCompareInDBBase(DocumentCompareBase):

    class Config:
        orm_mode = True


# Additional properties to return via API
class DocumentCompare(DocumentCompareInDBBase):
    pass
    
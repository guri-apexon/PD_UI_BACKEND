from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class ProtocolQcDataBase(BaseModel):
    id: Optional[str] = None
    userId: Optional[str] = None
    fileName: Optional[str] = None
    documentFilePath: Optional[str] = None
    iqvdataToc: Optional[str] = None
    iqvdataSoa: Optional[str] = None
    iqvdataSoaStd: Optional[str] = None
    iqvdataSummary: Optional[str] = None
    iqvdata: Optional[str] = None
    isActive: Optional[bool] = None


# Properties to receive via API on creation
class ProtocolQcDataCreate(ProtocolQcDataBase):
    id: str
    userId: str
    fileName: str
    documentFilePath: str
    iqvdataToc: str
    iqvdataSoa: str
    iqvdataSoaStd: str
    iqvdataSummary: str
    iqvdata: str
    isActive: bool


# Properties to receive via API on update
class ProtocolQcDataUpdate(ProtocolQcDataBase):
    pass
    

class ProtocolQcDataInDBBase(ProtocolQcDataBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProtocolQcData(ProtocolQcDataInDBBase):
    pass

class ProtocolQcDataReadIqvdataBase(BaseModel):
    iqvdata: Optional[str] = None

class ProtocolQcDataReadIqvdataInDBBase(ProtocolQcDataReadIqvdataBase):
    pass

    class Config:
        orm_mode = True

# Iqvdata to return via API
class ProtocolQcDataReadIqvdata(ProtocolQcDataReadIqvdataInDBBase):
    pass


    

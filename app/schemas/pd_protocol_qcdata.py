from typing import Optional

from pydantic import BaseModel


# Shared properties
class ProtocolQCDataBase(BaseModel):
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
class ProtocolQCDataCreate(ProtocolQCDataBase):
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
class ProtocolQCDataUpdate(ProtocolQCDataBase):
    pass


class ProtocolQCDataInDBBase(ProtocolQCDataBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProtocolQCData(ProtocolQCDataInDBBase):
    pass


class ProtocolQCDataReadIqvdataBase(BaseModel):
    iqvdata: Optional[str] = None


class ProtocolQCDataReadIqvdataInDBBase(ProtocolQCDataReadIqvdataBase):
    pass

    class Config:
        orm_mode = True


# Iqvdata to return via API
class ProtocolQCDataReadIqvdata(ProtocolQCDataReadIqvdataInDBBase):
    pass

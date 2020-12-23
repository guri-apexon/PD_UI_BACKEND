from typing import Optional

from pydantic import BaseModel


# Shared properties
class ProtocolSponsorBase(BaseModel):
    sponsorName: Optional[str] = None


# Properties to receive via API on creation
class ProtocolSponsorCreate(ProtocolSponsorBase):
    sponsorName: str


# Properties to receive via API on update
class ProtocolSponsorUpdate(ProtocolSponsorBase):
    pass

class ProtocolSponsorInDBBase(ProtocolSponsorBase):
    sponsorId: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProtocolSponsor(ProtocolSponsorInDBBase):
    pass

from typing import Optional
from pydantic import BaseModel, Field

class RolesBase(BaseModel):
    roleName: Optional[str] = None
    roleDescription: Optional[str] = None
    roleLevel: Optional[str] = None
class RolesBaseInDBBase(RolesBase):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class RolesUpdate(RolesBase):
    pass

class RolesCreate(RolesBase):
    roleName: str = Field(...)
    roleDescription: str = Field(...)
    roleLevel: str = Field(...)

class Roles(RolesBaseInDBBase):
    pass
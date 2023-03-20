from typing import Optional
from pydantic import BaseModel, Field


# The Following Below Details will be displayed in Swagger UI
class UserBase(BaseModel):
    username: Optional[str] = None
    first_name:Optional[str]=None
    last_name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    user_type : Optional[str]=None


class UserBaseInDBBase(UserBase):
    username: Optional[str] = None
    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    user_type: Optional[str] = None


class UserCreate(UserBase):
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    country: str = Field(...)
    user_type: str = Field(...)


class User(UserBaseInDBBase):
    pass


class UserAlertSettingUpdate(BaseModel):
    userId: Optional[str] = None
    options: Optional[dict] = None


class UserAlertSettingData(BaseModel):
    data: UserAlertSettingUpdate

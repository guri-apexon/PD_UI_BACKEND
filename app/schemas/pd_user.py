from typing import Optional
from datetime import datetime
from pydantic import BaseModel


#The Following Below Details will be displayed in Swagger UI
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
    username: str
    first_name: str
    last_name: str
    email: str
    country: str
    user_type: str

class User(UserBaseInDBBase):
    pass
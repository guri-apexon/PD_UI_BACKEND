from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.pd_user import User

#Below To Be Displayed In the ui
class LoginBase(BaseModel):
    username: Optional[str] = None
    internal_user: Optional[bool] = None
    active_user: Optional[bool] = None

class Soft_Delete(LoginBase):
    username: Optional[str] = None
    internal_user: Optional[bool] = None

class User_Soft_Delete(Soft_Delete):
    pass

class LoginBaseInDBBase(LoginBase):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class Login(LoginBaseInDBBase):
    pass

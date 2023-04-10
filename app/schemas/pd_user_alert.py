from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserAlertBase(BaseModel):
    id: Optional[str] = None
    protocol: Optional[str] = None
    aidocId: Optional[str] = None
    readFlag: Optional[bool] = False
    protocolTitle: Optional[str] = None
    timeCreated: Optional[datetime] = None
    alert_id: Optional[str] = None
    event: Optional[str] = None
    status: Optional[str] = None


class UserAlert(UserAlertBase):
    class Config:
        orm_mode = True

class UserAlertInput(BaseModel):
    userId: str

class UserAlertTestUpdate(UserAlertBase):
    timeUpdated: Optional[datetime] = None

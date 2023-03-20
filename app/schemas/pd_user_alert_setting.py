from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserAlertSettingBase(BaseModel):
    id: Optional[str] = None
    userId: Optional[str] = None
    new_document_version: Optional[bool] = None
    edited: Optional[bool] = None
    QC_complete: Optional[bool] = None
    created_time: Optional[datetime] = datetime.utcnow()
    updated_time: Optional[datetime] = datetime.utcnow()


class UserAlertSettingCreate(UserAlertSettingBase):
    pass


class UserAlertSettingUpdate(BaseModel):
    userId: Optional[str] = None
    options: Optional[dict] = None


class UserAlertSettingData(BaseModel):
    data:UserAlertSettingUpdate
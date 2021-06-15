from typing import Optional
from pydantic import BaseModel


class NotificationReadBase(BaseModel):
    id: Optional[str] = None
    protocol: Optional[str] = None
    aidocId: Optional[str] = None
    readFlag: Optional[bool] = False


class NotificationRead(NotificationReadBase):
    id: Optional[str] = None
    protocol: Optional[str] = None
    aidocId: Optional[str] = None
    readFlag: Optional[bool] = False
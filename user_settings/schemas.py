from pydantic import BaseModel
from datetime import datetime


class UserSettingsUpdate(BaseModel):
    phone_visibility: str | None = None   
    photo_visibility: str | None = None   
    who_can_message: str | None = None    
    notifications: bool | None = None


class UserSettingsResponse(BaseModel):
    id: int
    user_id: int
    phone_visibility: str
    photo_visibility: str
    who_can_message: str
    notifications: bool
    updated_at: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class NotificationResponse(BaseModel):
    id: int
    from_user: UserShort
    type: str 
    entity_id: int | None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationCount(BaseModel):
    unread_count: int
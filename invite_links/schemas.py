from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class InviteLinkCreate(BaseModel):
    expires_at: datetime | None = None


class InviteLinkResponse(BaseModel):
    id: int
    chat_id: int
    created_by: UserShort
    link: str
    is_active: bool
    expires_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
        
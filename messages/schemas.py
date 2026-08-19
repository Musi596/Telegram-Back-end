from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class MessageCreate(BaseModel):
    text: str | None = None
    media_id: int | None = None
    reply_to_id: int | None = None


class MessageUpdate(BaseModel):
    text: str


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    user: UserShort
    text: str | None
    media_id: int | None
    reply_to_id: int | None
    forward_from_id: int | None
    is_edited: bool
    is_deleted: bool
    created_at: datetime
    edited_at: datetime | None

    class Config:
        from_attributes = True
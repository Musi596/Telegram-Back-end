from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class MediaCreate(BaseModel):
    type: str 
    url: str
    file_name: str | None = None
    file_size: int | None = None
    duration: int | None = None


class MediaResponse(BaseModel):
    id: int
    chat_id: int
    user: UserShort
    type: str
    url: str
    file_name: str | None
    file_size: int | None
    duration: int | None
    created_at: datetime

    class Config:
        from_attributes = True
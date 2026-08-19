from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class ChatCreate(BaseModel):
    type: str 
    name: str | None = None
    description: str | None = None
    photo: str | None = None
    is_public: bool = False
    username: str | None = None
    member_ids: list[int] = []


class ChatUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    photo: str | None = None
    username: str | None = None


class ChatResponse(BaseModel):
    id: int
    type: str
    name: str | None
    description: str | None
    photo: str | None
    owner: UserShort
    is_public: bool
    username: str | None
    members_count: int = 0
    last_message: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
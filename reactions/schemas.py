from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class ReactionCreate(BaseModel):
    emoji: str


class ReactionResponse(BaseModel):
    id: int
    message_id: int
    user: UserShort
    emoji: str
    created_at: datetime

    class Config:
        from_attributes = True
        
from pydantic import BaseModel
from datetime import datetime
from messages.schemas import MessageResponse
from users.schemas import UserShort


class PinResponse(BaseModel):
    id: int
    chat_id: int
    message: MessageResponse
    pinned_by: UserShort
    pinned_at: datetime

    class Config:
        from_attributes = True
        
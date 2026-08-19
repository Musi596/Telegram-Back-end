from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class BlockCreate(BaseModel):
    blocked_id: int


class BlockResponse(BaseModel):
    id: int
    blocked: UserShort
    created_at: datetime

    class Config:
        from_attributes = True